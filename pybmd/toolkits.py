from dataclasses import dataclass
import logging
from pathlib import Path
import time
import re
from typing import Dict, Iterable, List, Optional

from pybmd.gallery_still import GalleryStill
from pybmd.gallery_still_album import GalleryStillAlbum, StillFormat
from pybmd.folder import Folder
from pybmd.media_pool_item import MediaPoolItem
from pybmd.project import Project
from pybmd.timeline import Timeline, TrackType
from pybmd.media_pool import MediaPool
from dftt_timecode import DfttTimecode


def change_timeline_resolution(timeline: Timeline, width, height) -> bool:
    """change timeline resolution.

    Args:
        timeline (Timeline): timeline object to change resolution
        width (_type_): timeline width
        height (_type_): timeline height

    Returns:
        bool: True if successful.
    """
    timeline.set_setting(
        "useCustomSettings", "1"
    )  # Special thanks to @thomjiji for this setting!
    return timeline.set_setting(
        "timelineResolutionWidth", str(width)
    ) & timeline.set_setting("timelineResolutionHeight", str(height))


def get_all_timeline(project: Project) -> List[Timeline]:
    """Returns all timeline in the project."""
    if project.get_timeline_count() == 0:
        return None
    else:
        return [
            project.get_timeline_by_index(timeline_index)
            for timeline_index in range(1, project.get_timeline_count() + 1, 1)
        ]


def get_timeline(project: Project, timeline_name: str) -> Timeline:
    """get timeline by name.

    Args:
        project (Project): project to get timeline
        timeline_name (str): timeline name

    Returns:
        Timeline: timeline object matching the name, None if not found.
    """
    all_timeline = get_all_timeline(project)
    if bool(all_timeline):
        timeline_dict = {timeline.get_name(): timeline for timeline in all_timeline}
        return timeline_dict.get(timeline_name)
    else:
        return None


def get_subfolder(folder: Folder, subfolder_name: str) -> Folder:
    """go to sub folder by name.

    Args:
        media_pool (MediaPool): media pool object
        folder_name (str): sub folder name

    Returns:
        bool: True if successful.
    """
    subfolder_list = {
        folder.get_name(): folder for folder in folder.get_sub_folder_list()
    }

    return subfolder_list.get(subfolder_name)


# TODO get_folder_by_path(check path before get ,if folder not exist,create or raise error)


def add_subfolders(media_pool: MediaPool, folder: Folder, subfolder_path: str) -> bool:
    """add subfolder by given path string

    Args:
        media_pool (MediaPool): media pool object to operate
        folder (Folder): folder to add subfolder
        subfolder_path (str): subfolder path

    Returns:
        bool: Return True if successful
    """

    # inner function for recursion
    def _add_folder(_media_pool: MediaPool, _folder: Folder, _path_list: list):
        if len(_path_list) == 0:
            return True
        else:
            __folder = _media_pool.add_sub_folder(_folder, _path_list[0])
            _path_list.pop(0)
            return _add_folder(_media_pool, __folder, _path_list)

    if folder is None:
        folder = media_pool.get_current_folder()
    path_spilt_list = re.findall(r"([^\/]+)\/", subfolder_path)

    return _add_folder(media_pool, folder, path_spilt_list)


# TODO render_timeline


@dataclass
class MarkerStill(object):
    still_obj: GalleryStill
    clip_obj: MediaPoolItem
    marker_record_tc: DfttTimecode
    marker_source_tc: DfttTimecode
    marker_info: Dict

    def get_property(self):
        return [
            self.clip_obj.get_name(),
            self.marker_record_tc.timecode_output(),
            self.marker_source_tc.timecode_output("smpte"),
            self.marker_info,
        ]


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class StillManager(object):
    """all about stills from timeline"""

    STILL_NAME_WILDCARD_MAPPING = {
        "file_name": "File Name",
        "reel_name": "Reel Name",
        "frames": "Frames",
    }

    def __init__(self, project: Project, timeline_framerate=24):
        super(StillManager, self).__init__()
        self._project: Project = project
        self._timeline: Timeline = self._project.get_current_timeline()
        if self._timeline is None:
            raise ValueError("Project does not have an active timeline selected.")

        self._gallery = self._project.get_gallery()
        if self._gallery is None:
            raise ValueError("Project does not have an available gallery.")

        timeline_name = self._timeline.get_name() or "Timeline"
        album_label = f"StillManager_{timeline_name}"
        self._still_album = self._initialize_still_album(album_label)

        timeline_fps_setting = self._timeline.get_setting("timelineFrameRate")
        if timeline_fps_setting:
            self._timeline_framerate = float(timeline_fps_setting)
            logger.info("Timeline Framerate:%s", self._timeline_framerate)
        else:
            self._timeline_framerate = float(timeline_framerate)
            logger.warning(
                "Unable to read timelineFrameRate; falling back to %.2f",
                self._timeline_framerate,
            )

        drop_frame_setting = self._timeline.get_setting("timelineDropFrameTimecode")
        self._timeline_df_flag = bool(int(drop_frame_setting)) if drop_frame_setting else False
        self.marker_still_list: List[MarkerStill] = []

    def __repr__(self):
        temp_list = [
            marker_still.get_property() for marker_still in self.marker_still_list
        ]
        return str(temp_list)

    @staticmethod
    def _clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
        return max(minimum, min(value, maximum))

    def _resolve_timeline(self, timeline: Optional[Timeline]) -> Timeline:
        if isinstance(timeline, Timeline):
            return timeline
        if self._timeline is None:
            raise ValueError("StillManager does not have a timeline to operate on.")
        return self._timeline

    @staticmethod
    def _coerce_bool(value: Optional[str], default: bool = False) -> bool:
        if value in (None, ""):
            return default
        try:
            return bool(int(value))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _coerce_float(value: Optional[str], default: float) -> float:
        if value in (None, ""):
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _safe_clip_property(
        clip: MediaPoolItem, property_key: str, default: Optional[str] = None
    ) -> Optional[str]:
        if clip is None:
            return default
        value = clip.get_clip_property(property_key)
        if value in ("", None):
            return default
        return value

    def _initialize_still_album(self, album_name: str) -> GalleryStillAlbum:
        """Create (if supported) or reuse a still album for this manager."""
        create_album = getattr(self._gallery, "create_gallery_still_album", None)
        if callable(create_album):
            try:
                new_album = create_album()
            except AttributeError:
                logger.info(
                    "create_gallery_still_album not available; using existing still album."
                )
            except Exception as exc:
                logger.warning("Failed to create still album: %s", exc)
            else:
                if new_album is not None:
                    if not self._gallery.set_album_name(new_album, album_name):
                        logger.warning(
                            "Unable to set still album name to %s", album_name
                        )
                    if not self._set_current_still_album(new_album):
                        logger.warning(
                            "Unable to select newly created still album %s as current.",
                            album_name,
                        )
                    else:
                        logger.info("Using dedicated still album %s.", album_name)
                    return new_album
        fallback_album = self._gallery.get_current_still_album()
        if fallback_album is None:
            raise ValueError("Project gallery does not have an active still album.")
        return fallback_album

    def _set_current_still_album(self, album: GalleryStillAlbum) -> bool:
        try:
            result = self._gallery.set_current_still_album(album)
        except AttributeError:
            logger.info("Gallery object does not support selecting still albums.")
            return False
        return bool(result)

    def grab_still_from_timeline_markers(
        self, timeline: Timeline = None, grab_sleep_time: float = 0.5
    ) -> List[MarkerStill]:
        """Grab stills at each marker location on the requested timeline.

        Args:
            timeline (Timeline, optional): Timeline to evaluate. Defaults to the manager timeline.
            grab_sleep_time (float, optional): Seconds to sleep between grabs, allowing Resolve to update the gallery.

        Returns:
            List[MarkerStill]: Still metadata accumulated so far.
        """
        timeline = self._resolve_timeline(timeline)
        marker_list = timeline.get_markers() or {}
        logger.info("Timeline Marker Count:%d", len(marker_list))

        if not marker_list:
            return self.marker_still_list

        timeline_start_timecode = DfttTimecode(
            timeline.get_start_timecode(),
            "auto",
            self._timeline_framerate,
            drop_frame=self._timeline_df_flag,
        )
        logger.debug("timeline_start_timecode: %s", timeline_start_timecode)

        sleep_interval = max(0.0, grab_sleep_time or 0.0)

        for marker_frameid, marker_info in sorted(marker_list.items()):
            marker_record_tc: DfttTimecode = timeline_start_timecode + marker_frameid
            timeline.set_current_timecode(marker_record_tc.timecode_output())
            timeline_item = timeline.get_current_video_item()
            if timeline_item is None:
                logger.warning(
                    "No timeline item available at marker frame %s. Skipping.", marker_frameid
                )
                continue

            # get source tc for the marker
            clip = timeline_item.get_media_pool_item()
            if clip is None:
                logger.warning(
                    "Timeline item at frame %s has no media pool item. Skipping.",
                    marker_frameid,
                )
                continue

            clip_df_flag = self._coerce_bool(clip.get_clip_property("Drop frame"))
            clip_fps = self._coerce_float(
                clip.get_clip_property("FPS"), self._timeline_framerate
            )

            clip_start_tc = self._safe_clip_property(clip, "Start TC")
            if clip_start_tc is None:
                logger.warning(
                    "Clip %s has no Start TC metadata; skipping marker %s.",
                    clip.get_name(),
                    marker_frameid,
                )
                continue

            clip_start_timecode = DfttTimecode(
                clip_start_tc,
                "auto",
                clip_fps,
                drop_frame=clip_df_flag,
            )
            clip_tc_frame_offset = (
                int(timeline_start_timecode.timecode_output("frame"))
                + marker_frameid
                - timeline_item.get_start()
            )

            marker_source_tc = clip_start_timecode + clip_tc_frame_offset

            still = timeline.grab_still()
            if still is None:
                logger.warning(
                    "Failed to grab still for clip %s at marker %s.",
                    clip.get_name(),
                    marker_frameid,
                )
                continue

            marker_still = MarkerStill(
                still,
                clip,
                marker_record_tc,
                marker_source_tc,
                marker_info,
            )
            self.marker_still_list.append(marker_still)
            if sleep_interval:
                time.sleep(sleep_interval)

        return self.marker_still_list

    def grab_all_still(
        self,
        timeline: Timeline = None,
        grab_sleep_time: float = 0.5,
        still_position: float = 0.5,
    ):
        """Grab a still for each clip in the first video track and store metadata.

        Args:
            timeline (Timeline, optional): Timeline to scan; defaults to the manager's current timeline.
            grab_sleep_time (float, optional): Delay inserted after each grab so Resolve can finish writing the still.
            still_position (float, optional): Normalized position within each clip (0=start, 1=end); values outside the range are clamped.

        Returns:
            List[MarkerStill]: Still metadata accumulated so far.
        """

        clamped_position = self._clamp(still_position, 0.0, 1.0)
        if clamped_position != still_position:
            logger.warning(
                "still_position %.3f is out of range [0,1]; clamping to %.3f",
                still_position,
                clamped_position,
            )
        still_position = clamped_position

        timeline = self._resolve_timeline(timeline)

        timelineitem_list = timeline.get_item_list_in_track(TrackType.VIDEO_TRACK, 1) or []
        if not timelineitem_list:
            logger.info("No clips found on VIDEO_TRACK 1; nothing to grab.")
            return self.marker_still_list

        timeline_start_timecode = DfttTimecode(
            timeline.get_start_timecode(),
            "auto",
            self._timeline_framerate,
            drop_frame=self._timeline_df_flag,
        )

        sleep_interval = max(0.0, grab_sleep_time or 0.0)

        for timeline_item in timelineitem_list:
            clip = timeline_item.get_media_pool_item()
            if clip is None:
                logger.warning("Timeline item has no media pool clip; skipping.")
                continue

            timelineitem_start_timecode = (
                timeline_start_timecode + timeline_item.get_start()
            )
            still_position_frame_offset = int(
                timeline_item.get_duration() * still_position
            )

            timelineitem_still_timecode = (
                timelineitem_start_timecode + still_position_frame_offset
            )
            timeline.set_current_timecode(
                timelineitem_still_timecode.timecode_output("smpte")
            )

            clip_df_flag = self._coerce_bool(clip.get_clip_property("Drop frame"))
            clip_fps = self._coerce_float(
                clip.get_clip_property("FPS"), self._timeline_framerate
            )
            clip_start_tc = self._safe_clip_property(clip, "Start TC")
            if clip_start_tc is None:
                logger.warning(
                    "Clip %s is missing Start TC metadata; skipping.", clip.get_name()
                )
                continue

            clip_start_timecode = DfttTimecode(
                clip_start_tc,
                "auto",
                clip_fps,
                drop_frame=clip_df_flag,
            )
            clip_tc_frame_offset = (
                int(timeline_start_timecode.timecode_output("frame"))
                + int(timelineitem_still_timecode.timecode_output("frame"))
                - timeline_item.get_start()
            )

            marker_source_tc = clip_start_timecode + clip_tc_frame_offset

            still = timeline.grab_still()
            if still is None:
                logger.warning("Failed to grab still for clip %s.", clip.get_name())
                continue

            marker_still = MarkerStill(
                still,
                clip,
                timelineitem_still_timecode,
                marker_source_tc,
                {},
            )
            self.marker_still_list.append(marker_still)
            if sleep_interval:
                time.sleep(sleep_interval)

        return self.marker_still_list

    def _get_metadata(self, marker_still: MarkerStill, wildcard: str) -> str:
        """Resolve wildcard placeholders used while formatting filenames."""

        handlers = {
            "clip_frame_tc": lambda: f"{int(marker_still.marker_source_tc.timecode_output('frame')):08d}",
            "reel_number": lambda: self._extract_reel_number(marker_still),
            "marker_note": lambda: marker_still.marker_info.get("note", ""),
            "marker_name": lambda: marker_still.marker_info.get("name", ""),
        }

        if wildcard in handlers:
            return handlers[wildcard]() or ""

        property_key = self.STILL_NAME_WILDCARD_MAPPING.get(wildcard, wildcard)
        result = marker_still.clip_obj.get_clip_property(property_key)
        if not result:
            result = marker_still.clip_obj.get_metadata(property_key)
        if isinstance(result, dict):
            logger.warning(
                "Can not get %s from clip property, returning empty string", wildcard
            )
            return ""
        return result or ""

    def _extract_reel_number(self, marker_still: MarkerStill) -> str:
        reel_name = marker_still.clip_obj.get_clip_property("Reel Name")
        if not reel_name:
            logger.warning("Cannot get reel name from clip property")
            return ""
        try:
            return re.findall(r"(^[a-z0-9A-Z_]{6})", reel_name)[0]
        except (IndexError, re.error) as exc:
            raise ValueError("Reel name is not valid; cannot get reel number") from exc

    def export_stills(
        self,
        export_base_path: str,
        file_name_format: str = "$file_name$_$clip_frame_tc$",
        format: StillFormat = StillFormat.TIF,
        clean_drx: bool = True,
        use_subfolder: bool = False,
        subfolder: str = "",
    ):
        """export stills to given path

        Args:
            export_path (str): stills export path
            file_name_format (str, optional): file name format. accept $file_name$,$reel_name$,$reel_number$,$frames$,$clip_frame_tc$ and all clip property keys show at Davinci Resolve GUI as wildcard. Defaults to "$file_name$_$clip_frame_tc$".
            format (StillFormat, optional): exported stills format. Defaults to StillFormat.TIF.
            clean_drx (bool, optional): clean drx files after stills exported. Defaults to True.
            use_subfolder (bool, optional): use subfolder to export stills. Defaults to False.
            subfolder (str, optional): subfolder name to export stills. Defaults to "".
        """

        base_path = Path(export_base_path).expanduser()
        base_path = base_path if base_path.is_absolute() else base_path.resolve()

        if subfolder:
            use_subfolder = True

        if use_subfolder:
            folder_name = subfolder or self._timeline.get_name()
            if not subfolder:
                logger.info(
                    "Input subfolder is empty, using timeline name %s as export folder",
                    folder_name,
                )
            export_path = base_path / folder_name
        else:
            export_path = base_path

        export_path.mkdir(parents=True, exist_ok=True)

        wildcard_pattern = re.compile(r"\$(.*?)\$")
        wildcard_matches = wildcard_pattern.findall(file_name_format)
        file_name_template = re.sub(wildcard_pattern, r"{\1}", file_name_format)
        logger.debug("file_name_template : %s", file_name_template)

        existing_files = {entry.name for entry in export_path.iterdir() if entry.is_file()}
        original_contents = set(existing_files)

        skip_count = 0
        for marker_still in self.marker_still_list:
            try:
                _file_prefix = file_name_template.format(
                    **{var: self._get_metadata(marker_still, var) for var in wildcard_matches}
                ).strip()
            except KeyError as exc:
                logger.warning("Missing wildcard %s in metadata. Skipping still.", exc)
                continue

            if not _file_prefix:
                _file_prefix = marker_still.clip_obj.get_name()

            target_file_name = f"{_file_prefix}.{format.value}"
            logger.debug("target file name:%s", target_file_name)

            if target_file_name in existing_files:
                logger.info("File %s exists. Skipping export.", target_file_name)
                skip_count += 1
                continue

            self._still_album.export_stills(
                gallery_stills=[marker_still.still_obj],
                folder_path=str(export_path),
                file_prefix=_file_prefix,
                format=format,
            )
            existing_files.add(target_file_name)

        # check export folder
        exported_files = {entry.name for entry in export_path.iterdir() if entry.is_file()}
        exported_stills_count = len(exported_files - original_contents)

        # clear album
        stills = self._still_album.get_stills()
        self._still_album.delete_stills(stills)

        if (
            exported_stills_count == 0
            and len(self.marker_still_list) != 0
            and skip_count < len(self.marker_still_list)
        ):
            logger.warning(
                f"No stills exported to folder {export_path}. Please check if you open the [gallery] in color page or not"
            )
            return
        self.rename_still(str(export_path), clean_drx, original_contents)

    def rename_still(
        self,
        still_file_path: str,
        clean_drx: bool = True,
        export_folder_exist_file_list: Optional[Iterable[str]] = None,
    ):
        """Normalize exported still names and optionally clean up DRX files."""
        existing_files = set(export_folder_exist_file_list or [])
        target_path = Path(still_file_path).expanduser()
        target_path = target_path if target_path.is_absolute() else target_path.resolve()

        remove_count = 0

        for entry in target_path.iterdir():
            if not entry.is_file():
                continue
            if entry.name == ".DS_Store":
                continue
            if entry.name in existing_files:
                continue

            if entry.suffix == ".drx" and clean_drx:
                try:
                    entry.unlink()
                except FileNotFoundError:
                    pass
                remove_count += 1
                continue

            match = re.match(r"(.*)_[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}", entry.stem)
            if not match:
                continue

            new_name = f"{match.group(1)}{entry.suffix}"
            destination = entry.with_name(new_name)
            entry.rename(destination)
            logger.info("%s export successfully!", destination.name)

        if remove_count != 0:
            logger.info("Deleted %d drx files", remove_count)
