from ast import Dict
from dataclasses import dataclass
import logging
import os
import time
import re
from typing import List

from pybmd.gallery_still import GalleryStill
from pybmd.gallery_still_album import StillFormat
from pybmd.folder import Folder
from pybmd.media_pool_item import MediaPoolItem
from pybmd.project import Project
from pybmd.timeline import Timeline
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
    """all about stills from timeline markers"""

    STILL_NAME_WILDCARD_MAPPING = {
        "file_name": "File Name",
        "reel_name": "Reel Name",
        "frames": "Frames",
    }

    def __init__(self, project: Project, timeline_framerate=24):

        super(StillManager, self).__init__()
        self._project = project
        self._timeline = self._project.get_current_timeline()
        self._gallery = self._project.get_gallery()
        self._still_album = self._gallery.get_current_still_album()

        if self._timeline.get_setting("timelinePlaybackFrameRate"):
            self._timeline_framerate = float(
                self._timeline.get_setting("timelinePlaybackFrameRate")
            )
            logger.info(f"Timeline Framerate:{self._timeline_framerate}")
        else:
            self._timeline_framerate = timeline_framerate
            logger.warning(
                f"CAN NOT get timeline framerate because this timeline use custom timeline settings, use timeline_framerate :{self._timeline_framerate} instead "
            )
        self.marker_still_list: List[MarkerStill] = list()

    def __repr__(self):
        temp_list = [
            marker_still.get_property() for marker_still in self.marker_still_list
        ]
        return str(temp_list)

    def grab_still_from_timeline_markers(
        self, timeline: Timeline = None, grab_sleep_time: float = 0.5
    ) -> List[MarkerStill]:
        """grab stills from timeline markers.

        Args:
            timeline (Timeline, optional): timeline to grab stills. Defaults to None.
            grab_sleep_time (float, optional): time to sleep between grab. Defaults to 0.5.

        Returns:
            List[MarkerStill]: _description_
        """
        if isinstance(timeline, Timeline) is False:
            timeline = self._timeline
        marker_list = timeline.get_markers()
        logger.info(f"Timeline Marke:{marker_list}")
        logger.info(f"Timeline Marker Count:{len(marker_list)}")
        timeline_df_flag = bool(
            int(self._timeline.get_setting("timelineDropFrameTimecode"))
        )
        timeline_start_timecode = DfttTimecode(
            timeline.get_start_timecode(),
            "auto",
            self._timeline_framerate,
            drop_frame=timeline_df_flag,
        )
        logger.debug(f"timeline_start_timecode: {timeline_start_timecode}")
        # grab stills for every marker
        for marker_frameid, marker_info in marker_list.items():

            marker_record_tc: DfttTimecode = timeline_start_timecode + marker_frameid
            timeline.set_current_timecode(marker_record_tc.timecode_output())
            timeline_item = timeline.get_current_video_item()

            # get source tc for the marker
            clip_df_flag = bool(
                int(timeline_item.get_media_pool_item().get_clip_property("Drop frame"))
            )
            clip_fps = timeline_item.get_media_pool_item().get_clip_property("FPS")

            clip_start_timecode = DfttTimecode(
                timeline_item.get_media_pool_item().get_clip_property("Start TC"),
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

            marker_still = MarkerStill(
                still,
                timeline_item.get_media_pool_item(),
                marker_record_tc,
                marker_source_tc,
                marker_info,
            )
            self.marker_still_list.append(marker_still)
            time.sleep(grab_sleep_time)

    def _get_metadata(self, marker_still: MarkerStill, wildcard: str) -> str:
        if wildcard == "clip_frame_tc":
            source_frame_tc = int(
                marker_still.marker_source_tc.timecode_output("frame")
            )
            return f"{source_frame_tc:08d}"
        if wildcard == "reel_number":
            reel_name = marker_still.clip_obj.get_clip_property("Reel Name")
            if reel_name == "":
                logger.warning(f"Can not get reel name from clip property")
                return ""
            else:
                try:
                    return re.findall(r"(^[a-z0-9A-Z_]{6})", reel_name)[0]
                except Exception as e:
                    raise e.add_note("Reel name is not valid,Can not get reel number")
        if wildcard == "marker_note":
            return marker_still.marker_info.get("note")
        if wildcard == "marker_name":
            return marker_still.marker_info.get("name")
        property_key = (
            self.STILL_NAME_WILDCARD_MAPPING.get(wildcard)
            if self.STILL_NAME_WILDCARD_MAPPING.get(wildcard)
            else wildcard
        )

        result = marker_still.clip_obj.get_clip_property(property_key)
        if not result:
            result = marker_still.clip_obj.get_metadata(property_key)
        if isinstance(result, dict):
            result = ""
            logger.warning(
                f"Can not get {wildcard} from clip property,return empty string"
            )
        return result

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

        if export_base_path.startswith("~"):
            export_base_path = os.path.expanduser(export_base_path)
        else:
            export_base_path = os.path.abspath(export_base_path)

        if subfolder != "":
            use_subfolder = True

        if use_subfolder:
            if subfolder == "":
                subfolder = self._timeline.get_name()
                logger.info(
                    f" Input subfolder is empty, use timeline name : {subfolder} as subfolder name to export"
                )
            export_path = os.path.join(export_base_path, subfolder)
        else:
            export_path = export_base_path

        try:
            os.makedirs(export_path)
        except Exception as e:
            logger.info(f"Folder {export_path} already exist,skip create")
        else:
            logger.info(f"Create folder : {export_path}")
        wildcard_pattern = re.compile(r"\$(.*?)\$")
        wildcard_matchs = wildcard_pattern.findall(file_name_format)
        file_name_template = re.sub(wildcard_pattern, r"{\1}", file_name_format)
        logger.debug(f"file_name_template : {file_name_template}")
        export_folder_contain_list = [os.listdir(export_path)]

        existed_file_name_list = [
            os.path.splitext(f.name) for f in os.scandir(export_path) if f.is_file()
        ]

        _skip_count = 0
        for marker_still in self.marker_still_list:
            media_pool_item_obj = marker_still.clip_obj
            _file_prefix = file_name_template.format(
                **{
                    var: self._get_metadata(marker_still, var)
                    for var in wildcard_matchs
                }
            )
            target_file_name_ext = (_file_prefix, "." + format.value)
            logger.debug(f"target file name:{target_file_name_ext}")
            if any(
                exist_file == target_file_name_ext
                for exist_file in existed_file_name_list
            ):
                logger.info(
                    f"File :{_file_prefix} Type: {format.value} exists! Skip export"
                )
                _skip_count += 1
                continue
            else:
                self._still_album.export_stills(
                    gallery_stills=[marker_still.still_obj],
                    folder_path=export_path,
                    file_prefix=_file_prefix,
                    format=format,
                )

        # check export folder
        exported_stills_count = len(
            [
                os.path.splitext(f.name)[0]
                for f in os.scandir(export_path)
                if f.is_file()
            ]
        ) - len(existed_file_name_list)

        # clear album
        stills = self._still_album.get_stills()
        self._still_album.delete_stills(stills)

        if (
            exported_stills_count == 0
            and len(self.marker_still_list) != 0
            and _skip_count < len(self.marker_still_list)
        ):
            logger.warning(
                f"No stills exported to folder {export_path}. Please check if you open the [gallery] in color page or not"
            )
            return
        self.rename_still(export_path, clean_drx, export_folder_contain_list)

    def rename_still(
        self,
        still_file_path: str,
        clean_drx: bool = True,
        export_folder_exist_file_list: List = list(),
    ):
        remove_count = 0

        for f in os.listdir(still_file_path):

            if f == ".DS_Store":
                continue
            if f in export_folder_exist_file_list:
                continue
            file_name = os.path.splitext(f)[0]
            file_extention = os.path.splitext(f)[1]

            # remove drx file
            if file_extention == ".drx" and clean_drx:
                os.remove(os.path.join(still_file_path, f))
                remove_count += 1
                continue

            _f = re.findall(r"(.*)_[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}", file_name)
            if bool(_f):
                _file_name = _f[0]
                os.rename(
                    os.path.join(still_file_path, f),
                    os.path.join(still_file_path, _file_name) + file_extention,
                )
                logger.info(f"{_file_name}{file_extention} export sucessfully!")
            else:
                continue

        if remove_count != 0:
            logger.info(f"Delete {remove_count} drx files")
