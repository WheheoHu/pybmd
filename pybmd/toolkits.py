from typing import List
from .folder import Folder
from pybmd.project import Project
from pybmd.timeline import Timeline
from pybmd.media_pool import MediaPool

def change_timeline_resolution(timeline:Timeline,width,height)->bool:
    """change timeline resolution.

    Args:
        timeline (Timeline): timeline object to change resolution
        width (_type_): timeline width
        height (_type_): timeline height

    Returns:
        bool: True if successful.
    """
    timeline.set_setting('useCustomSettings','1') #Special thanks to @thomjiji for this setting!
    return timeline.set_setting('timelineResolutionWidth',str(width)) & timeline.set_setting('timelineResolutionHeight',str(height))

def get_all_timeline(project:Project)->List[Timeline]:
    """Returns all timeline in the project."""
    return[project.get_timeline_by_index(timeline_index) for timeline_index in range(1,project.get_timeline_count()+1,1)]

def get_timeline(project:Project,timeline_name:str)->Timeline:
    """get timeline by name.

    Args:
        project (Project): project to get timeline
        timeline_name (str): timeline name

    Returns:
        Timeline: timeline object matching the name, None if not found.
    """
    all_timeline=get_all_timeline(project)
    timeline_dict={timeline.get_name():timeline for timeline in all_timeline}
    return timeline_dict.get(timeline_name)

def get_subfolder(folder: Folder,subfolder_name:str)->Folder:
    """go to sub folder by name.

    Args:
        media_pool (MediaPool): media pool object 
        folder_name (str): sub folder name

    Returns:
        bool: True if successful.
    """
    subfolder_list={folder.get_name():folder for folder in folder.get_sub_folder_list()}

    return subfolder_list.get(subfolder_name)

#TODO get_folder_by_path

#TODO add_subfolders (by path) MediaPool->add_subfolder

#TODO render_timeline 




