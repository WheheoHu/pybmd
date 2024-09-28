from dataclasses import asdict
from typing import TYPE_CHECKING, Any, Dict, List
from pybmd import color_group
from pybmd.color_group import ColorGroup
from pybmd.gallery import Gallery
from pybmd.media_pool import MediaPool

from pybmd.timeline import Timeline

if TYPE_CHECKING:
    from pybmd.settings import RenderSetting

RenderResolution = List[dict]




class Project():
    """Project Object"""


    def __init__(self, project):
        self._project = project

    def __repr__(self) -> str:
        return f'Project:{self.get_name()}'

    def get_self_project(self):
        return self._project

    def add_render_job(self) -> str:
        """Adds a render job based on current render settings to the render queue. 

        Returns:
            str: A unique job id (string) for the new render job.
        """
        return self._project.AddRenderJob()

    def delete_all_render_jobs(self) -> bool:
        """Deletes all render jobs in the render queue."""
        return self._project.DeleteAllRenderJobs()

    def delete_render_job(self, job_id: str) -> bool:
        """Deletes render job for input job id (string)."""
        return self._project.DeleteRenderJob(job_id)

    def get_current_render_format_and_codec(self) -> dict:
        """Returns a dict with currently selected format 'format' and render codec 'codec'."""
        return self._project.GetCurrentRenderFormatAndCodec()

    def get_current_render_mode(self) -> int:
        """Returns the render mode: 0 - Individual clips, 1 - Single clip."""
        return self._project.GetCurrentRenderMode()

    def get_current_timeline(self) -> Timeline:
        """Returns the currently loaded Timeline."""
        current_timeline = self._project.GetCurrentTimeline()
        if current_timeline is not None:
            return Timeline(self._project.GetCurrentTimeline())
        else:
            raise TypeError("No current timeline,Please open a timeline")
        

    def get_gallery(self) -> Gallery:
        """Returns the Gallery object."""
        return Gallery(self._project.GetGallery())

    def get_media_pool(self) -> MediaPool:
        """Returns the MediaPool object."""
        return MediaPool(self._project.GetMediaPool())

    def get_name(self) -> str:
        """Return project name"""
        return self._project.GetName()

    def get_preset_list(self) -> list:
        """Returns a list of presets and their information."""
        return self._project.GetPresetList()

    def get_render_codecs(self, render_format: str) -> dict:
        """returns a dict with render codecs for a given render format.

        Args:
            render_format (str): render format

        Returns:
            dict: codec description -> codec name
        """
        return self._project.GetRenderCodecs(render_format)

    def get_render_formats(self) -> dict:
        """Returns a dict (format -> file extension) of available render formats."""
        return self._project.GetRenderFormats()

    def get_render_job_list(self) -> list:
        """Returns a list of render jobs and their information."""
        return self._project.GetRenderJobList()

    def get_render_job_status(self, job_id: str) -> dict:
        """Returns a dict with job status and completion percentage of the job by given jobId (string)."""
        return self._project.GetRenderJobStatus(job_id)

    def get_render_preset_list(self):
        """Returns a list of render presets and their information."""
        return self._project.GetRenderPresetList()

    def get_render_resolutions(self, format: str, codec: str) -> RenderResolution:
        """Returns list of resolutions applicable for the given render format (string) and render codec (string). 

        Args:
            format (str): format
            codec (str): codec

        Returns:
            RenderResolution: Returns full list of resolutions if no argument is provided. Each element in the list is a dictionary with 2 keys "Width" and "Height".
        """
        # Sample: current_project.get_render_resolutions(format='mp4',codec='h264')
        return self._project.GetRenderResolutions(format, codec)

    def get_setting(self, setting_name: str = "") -> str:
        """Returns value of project setting (indicated by setting_name, string). """
        # call *without parameters/NoneType * to get a snapshot of all queryable properties
        return self._project.GetSetting(setting_name)

    def get_timeline_by_index(self, idx) -> Timeline:
        """Returns Timeline at the given index, 1 <= idx <= project.get_timeline_count()"""
        return Timeline(timeline=self._project.GetTimelineByIndex(idx))

    def get_timeline_count(self) -> int:
        """Returns the number of timelines currently present in the project."""
        return self._project.GetTimelineCount()

    def is_rendering_in_progress(self) -> bool:
        """Returns True if rendering is in progress."""
        return self._project.IsRenderingInProgress()

    def load_render_preset(self, preset_name) -> bool:
        """Sets a preset as current preset for rendering if preset_name (string) exists."""
        return self._project.LoadRenderPreset(preset_name)

    def refresh_lut_list(self) -> bool:
        """Refreshes LUT List"""
        return self._project.RefreshLUTList()

    def save_as_new_render_preset(self, preset_name) -> bool:
        """Creates new render preset by given name if preset_name(string) is unique."""
        return self._project.SaveAsNewRenderPreset(preset_name)

    def set_current_render_format_and_codec(self, format: str, codec: str) -> bool:
        """Sets given render format (string) and render codec (string) as options for rendering."""
        return self._project.SetCurrentRenderFormatAndCodec(format, codec)

    def set_current_render_mode(self, render_mode: int) -> bool:
        """Sets the render mode. 

        Args:
            render_mode (int): Specify renderMode = 0 for Individual clips, 1 for Single clip.

        Returns:
            bool: True if successful.
        """
        return self._project.SetCurrentRenderMode(render_mode)

    def set_current_timeline(self, timeline: Timeline) -> bool:
        """Sets given Timeline as current timeline for the project. Returns True if successful."""
        return self._project.SetCurrentTimeline(timeline._timeline)

    def set_name(self, project_name) -> bool:
        """Sets project name if given project_name (string) is unique."""
        return self._project.SetName(project_name)

    def set_preset(self, preset_name: str) -> bool:
        """Sets preset by given preset_name (string) into project."""
        return self._project.SetPreset(preset_name)

    def set_render_settings(self, render_setting: "RenderSetting") -> bool:
        """Sets given settings for rendering.

        Args:
            render_setting (RenderSetting): RenderSetting object

        Returns:
            bool: True if successful.
        """
        if type(render_setting) is dict:
            return self._project.SetRenderSettings(render_setting)
        else:
            return self._project.SetRenderSettings(asdict(render_setting))

    def set_setting(self, setting_name: str, setting_value: str):
        """Sets value of project setting (indicated by setting_name, string).

        Args:
            setting_name (str): Setting name
            setting_value (str): Setting value

        Returns:
            _type_: True if successful.
        """
        return self._project.SetSetting(setting_name, setting_value)

    def start_rendering(self, job_ids: list, is_interactive_mode=False) -> bool:
        """Start rendering. Returns True if successful.
        if job_ids==None render all queued render jobs.
        """
        return self._project.StartRendering(job_ids, is_interactive_mode)

    def stop_rendering(self):
        """Stops rendering."""
        return self._project.StopRendering()

    ##############################################################################################################################
    # Add at DR18.0.0

    def get_unique_id(self) -> str:
        """Returns unique id of the project Object."""
        return self._project.GetUniqueId()

    ##############################################################################################################################
    # Add at DR18.1.3

    def insert_audio_to_current_track_at_playhead(self, media_path: str, start_offset_in_samples: int, duration_in_samples: int) -> bool:
        """Inserts the media specified by mediaPath (string) with startOffsetInSamples (int) and durationInSamples (int) at the playhead on a selected track on the Fairlight page. 
        
        Args:
            media_path (str)
            start_offset_in_samples (int)
            duration_in_samples (int)

        Returns:
            bool: Returns True if successful, otherwise False.
        """        
        return self._project.InsertAudioToCurrentTrackAtPlayhead(media_path, start_offset_in_samples, duration_in_samples)

    ##############################################################################################################################
    # Add at DR18.5.0 Beta
    
    def load_burn_in_preset(self,preset_name:str) -> bool:
        """Loads user defined data burn in preset for project when supplied presetName (string). 

        Args:
            preset_name (str): preset name

        Returns:
            bool: Returns true if successful.
        """        
        return self._project.LoadBurnInPreset(preset_name)
    ##############################################################################################################################
    # Add at DR18.5.0 
    
    def export_current_frame_as_still(self,file_path:str) -> bool:
        """Exports current frame as still to supplied filePath. 

        Args:
            file_path (str): exported still path.filePath must end in valid export file format. 

        Returns:
            bool: Returns True if succssful, False otherwise.
        """
        return self._project.ExportCurrentFrameAsStill(file_path)
       
    ##############################################################################################################################
    # Add at DR 19.0.0 
    def get_color_groups_list(self) -> List[ColorGroup]:
        """Returns a list of all group objects in the timeline.

        Returns:
            List[ColorGroup]: a list of all group objects
        """
        color_group_list = list()
        for color_group in self._project.GetColorGroupsList():
            color_group_list.append(ColorGroup(color_group))
        return color_group_list
    
    def add_color_group(self,group_name:str) -> ColorGroup:
        """Creates a new ColorGroup. 

        Args:
            group_name (str): groupName must be a unique string.

        Returns:
            ColorGroup: ColorGroup object if successful, otherwise None.
        """
        return ColorGroup(self._project.AddColorGroup(group_name)  )
    
    def delete_color_group(self,color_group:ColorGroup) -> bool:
        """Deletes the given color group and sets clips to ungrouped.

        Args:
            color_group (ColorGroup): color group object to delete

        Returns:
            bool: Return True if successful, otherwise False.
        """
        return self._project.DeleteColorGroup(color_group) 
    