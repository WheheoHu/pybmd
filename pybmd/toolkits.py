from typing import List
from pybmd.project import Project
from pybmd.timeline import Timeline


def change_timeline_resolution(timeline:Timeline,width,height)->bool:
    """change timeline resolution.

    Args:
        timeline (Timeline): timeline object to change resolution
        width (_type_): timeline width
        height (_type_): timeline height

    Returns:
        bool: True if successful.
    """
    timeline.set_setting('useCustomSettings','1')
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

#TODO add go_to_folder function

#TODO add render_timeline function




