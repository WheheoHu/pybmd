from dataclasses import dataclass
import logging
import pybmd.logging_config
import os
import time
import re
from typing import Dict, List

from pybmd.gallery_still import GalleryStill
from pybmd.gallery_still_album import StillFormat
from pybmd.folder import Folder
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
    timeline.set_setting('useCustomSettings',
                         '1')  # Special thanks to @thomjiji for this setting!
    return timeline.set_setting('timelineResolutionWidth', str(width)) & timeline.set_setting('timelineResolutionHeight', str(height))


def get_all_timeline(project: Project) -> List[Timeline]:
    """Returns all timeline in the project."""
    if project.get_timeline_count() == 0:
        return None
    else:
        return [project.get_timeline_by_index(timeline_index) for timeline_index in range(1, project.get_timeline_count() + 1, 1)]


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
        timeline_dict = {
            timeline.get_name(): timeline for timeline in all_timeline}
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
        folder.get_name(): folder for folder in folder.get_sub_folder_list()}

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
    """MarkerStill object contains still and it's properties"""
    still_obj: GalleryStill
    reel_name: str
    reel_number: int
    file_name: str
    frames: int
    clip_frame_count: int

    def get_property(self):
        return {
            'reel_name': self.reel_name,
            'reel_number': self.reel_number,
            'file_name': self.file_name,
            'frames': self.frames,
            'clip_frame_count': self.clip_frame_count
        }


logger = logging.getLogger(__name__)


class StillManager(object):
    """all about stills from timeline markers"""
    _timeline: Timeline = None
    _stills: Dict = dict()

    def __init__(self, project: Project, default_timeline_framerate=24):

        super(StillManager, self).__init__()
        self._project = project
        self._timeline = self._project.get_current_timeline()
        self._gallery = self._project.get_gallery()
        self._still_album = self._gallery.get_current_still_album()

        self._default_timeline_framerate = default_timeline_framerate

        self.marker_still_list: List[MarkerStill] = list()

    def __repr__(self):
        temp_list = [marker_still.get_property()
                     for marker_still in self.marker_still_list]
        return str(temp_list)

    def grab_still_from_timeline_markers(self, timeline: Timeline = None, grab_sleep_time: float = 0.5) -> List[MarkerStill]:
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
        logger.info(f'Timeline Marker Count:{len(marker_list)}')

        if timeline.get_setting('timelinePlaybackFrameRate'):
            timeline_framerate = int(
                timeline.get_setting('timelinePlaybackFrameRate'))
            logger.info(f'Timeline Framerate:{timeline_framerate}')
        else:
            timeline_framerate = self._default_timeline_framerate
            logger.info(
                f'CAN NOT get timeline framerate because this timeline use custom timeline settings, use default_timeline_framerate :{timeline_framerate} instead ')

        timeline_start_timecode = DfttTimecode(
            timeline.get_start_timecode(), 'auto', timeline_framerate)

        # grab stills for every marker
        for marker_frameid in marker_list:

            marker_timecode: DfttTimecode = timeline_start_timecode+marker_frameid
            timeline.set_current_timecode(marker_timecode.timecode_output())
            timeline_item = timeline.get_current_video_item()
            # pro=timeline_item.get_media_pool_item().get_clip_property()

            # get frame count for the marker
            clip_start_timecode = DfttTimecode(timeline_item.get_media_pool_item(
            ).get_clip_property('Start TC'), 'auto', timeline_framerate)
            clip_frame_count = marker_frameid-(timeline_item.get_start()-int(
                timeline_start_timecode.timecode_output('frame')))+int(clip_start_timecode.timecode_output('frame'))

            reel_name = timeline_item.get_media_pool_item().get_clip_property('Reel Name')
            if reel_name == '':
                reel_number = ''
                logger.warning(f'Can not get reel name from clip property')
            else:
                try:
                    reel_number = re.findall(
                        r'(^[a-z0-9A-Z_]{6})', reel_name)[0]
                except Exception as e:
                    raise e.add_note(
                        "Reel name is not valid,Can not get reel number")

            file_name = timeline_item.get_media_pool_item().get_clip_property('File Name')
            frames = timeline_item.get_media_pool_item().get_clip_property('Frames')

            still = timeline.grab_still()

            marker_still = MarkerStill(
                still, reel_name, reel_number, file_name, frames, f"{clip_frame_count:08d}")
            self.marker_still_list.append(marker_still)
            time.sleep(grab_sleep_time)

    def export_stills(self, export_base_path: str, file_name_format: str = "$file_name$_$clip_frame_count$", format: StillFormat = StillFormat.TIF, clean_drx: bool = True, use_subfolder: bool = False, subfolder: str = ""):
        """export stills to given path

        Args:
            export_path (str): stills export path
            file_name_format (str, optional): file name format. accept $file_name$,$reel_name$,$reel_number$,$frames$,$clip_frame_count$ as wildcard. Defaults to "$file_name$_$clip_frame_count$".
            format (StillFormat, optional): exported stills format. Defaults to StillFormat.TIF.
            clean_drx (bool, optional): clean drx files after stills exported. Defaults to True.
            use_subfolder (bool, optional): use subfolder to export stills. Defaults to False.
            subfolder (str, optional): subfolder name to export stills. Defaults to "".
        """

        if export_base_path.startswith('~'):
            export_base_path = os.path.expanduser(export_base_path)
        else:
            export_base_path = os.path.abspath(export_base_path)

        if subfolder != "":
            use_subfolder = True

        if use_subfolder:
            if subfolder == "":
                subfolder = self._timeline.get_name()
                logger.info(
                    f" Input subfolder is empty, use timeline name : {subfolder} as subfolder name to export")
            export_path = os.path.join(export_base_path, subfolder)
        else:
            export_path = export_base_path

        try:
            os.makedirs(export_path)
        except Exception as e:
            logger.info(f"Folder {export_path} already exist")
        else:
            logger.info(f"Create folder : {export_path}")
        wildcard_pattern = re.compile(r"\$(\w+)\$")
        wildcard_matchs = wildcard_pattern.findall(file_name_format)
        file_name_template = re.sub(
            wildcard_pattern, r'{\1}', file_name_format)

        export_folder_contain_list = [os.listdir(export_path)]

        existed_file_name_list = [os.path.splitext(
            f.name) for f in os.scandir(export_path) if f.is_file()]

        _skip_count = 0
        for marker_still in self.marker_still_list:
            still_property = marker_still.get_property()
            _file_prefix = file_name_template.format(
                **{var: still_property.get(var) for var in wildcard_matchs})
            target_file_name_ext = (_file_prefix, '.'+format.value)
            logger.debug(f"target file name:{target_file_name_ext}")
            if any(exist_file == target_file_name_ext for exist_file in existed_file_name_list):
                logger.info(
                    f"File :{_file_prefix} Type: {format.value} exists! Skip export")
                _skip_count += 1
                continue
            else:
                self._still_album.export_stills(gallery_stills=[
                                                marker_still.still_obj], folder_path=export_path, file_prefix=_file_prefix, format=format)

        # check export folder
        exported_stills_count = len([os.path.splitext(f.name)[0] for f in os.scandir(
            export_path) if f.is_file()])-len(existed_file_name_list)

        # clear album
        stills = self._still_album.get_stills()
        self._still_album.delete_stills(stills)

        if exported_stills_count == 0 and len(self.marker_still_list) != 0 and _skip_count < len(self.marker_still_list):
            logger.warning(
                f"No stills exported to folder {export_path}. Please check if you open the [gallery] in color page or not")
            return
        self.rename_still(export_path, clean_drx, export_folder_contain_list)

    def rename_still(self, still_file_path: str, clean_drx: bool = True, export_folder_exist_file_list: List = list()):
        remove_count = 0

        for f in os.listdir(still_file_path):

            if f == '.DS_Store':
                continue
            if f in export_folder_exist_file_list:
                continue
            file_name = os.path.splitext(f)[0]
            file_extention = os.path.splitext(f)[1]

            # remove drx file
            if file_extention == '.drx' and clean_drx:
                os.remove(os.path.join(still_file_path, f))
                remove_count += 1
                continue

            _f = re.findall(r"(.*)_[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}", file_name)
            if bool(_f):
                _file_name = _f[0]
                os.rename(os.path.join(still_file_path, f), os.path.join(
                    still_file_path, _file_name)+file_extention)
                logger.info(
                    f'{_file_name}{file_extention} export sucessfully!')
            else:
                continue

        if remove_count != 0:
            logger.info(f'Delete {remove_count} drx files')
