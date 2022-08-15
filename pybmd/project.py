

from dataclasses import asdict
from dataclasses import dataclass
from typing import Any, List
from pybmd.gallery import Gallery
from pybmd.media_pool import MediaPool

from pybmd.timeline import Timeline


RenderResolution = List[dict]


@dataclass
class RenderSetting():
    """RenderSetting Object to store render setting."""
    SelectAllFrames: bool
    MarkIn: int
    MarkOut: int
    TargetDir: str
    CustomName: str
    UniqueFilenameStyle: int  # 0 for prefix, 1 for suffix
    ExportVideo: bool
    ExportAudio: bool
    FormatWidth: int
    FormatHeight: int
    FrameRate: float
    
    # (for SD resolution: "16_9" or "4_3") (other resolutions: "square" or "cinemascope")
    PixelAspectRatio: str
    
    #  possible values for current codec (if applicable):
    #  0(int) - will set quality to automatic
    # [1 -> MAX] (int) - will set input bit rate
    # ["Least", "Low", "Medium", "High", "Best"] (String) - will set input quality level
    VideoQuality: Any

    AudioCodec: str
    AudioBitDepth: int
    AudioSampleRate: int
    
    # example: "Same as Project", "AstroDesign"
    ColorSpaceTag: str  
    
    # example: "Same as Project", "ACEScct"
    GammaTag: str  
    ExportAlpha: bool
    
    # (example: "Main10"). Can only be set for H.264 and H.265.
    EncodingProfile: str
    
    # Can onlt be set for H.264.
    MultiPassEncode: bool  
    
    # 0 - Premultipled, 1 - Straight. Can only be set if "ExportAlpha" is true.
    AlphaMode: int

    # Only supported by QuickTime and MP4 formats.
    NetworkOptimization: bool 

class Project():
    """Project Object"""

    project = None
    project_name = None

    def __init__(self, _project, _project_name: str):
        self.project_name = _project_name
        self.project = _project

    def get_self_project(self):
        return self.project

    def add_render_job(self) -> str:
        """Adds a render job based on current render settings to the render queue. 

        Returns:
            str: A unique job id (string) for the new render job.
        """
        return self.project.AddRenderJob()

    def delete_all_render_jobs(self) -> bool:
        """Deletes all render jobs in the render queue."""
        return self.project.DeleteAllRenderJobs()

    def delete_render_job(self, job_id: str) -> bool:
        """Deletes render job for input job id (string)."""
        return self.project.DeleteRenderJob(job_id)

    def get_current_render_format_and_codec(self) -> dict:
        """Returns a dict with currently selected format 'format' and render codec 'codec'."""
        return self.project.GetCurrentRenderFormatAndCodec()

    def get_current_render_mode(self) -> int:
        """Returns the render mode: 0 - Individual clips, 1 - Single clip."""
        return self.project.GetCurrentRenderMode()

    def get_current_timeline(self) -> Timeline:
        """Returns the currently loaded Timeline."""
        return Timeline(timeline=self.project.GetCurrentTimeline())

    def get_gallery(self) -> Gallery:
        """Returns the Gallery object."""
        return Gallery(self.project.GetGallery())

    def get_media_pool(self) -> MediaPool:
        """Returns the MediaPool object."""
        return MediaPool(self.project.GetMediaPool())

    def get_name(self) -> str:
        """Return project name"""
        return self.project.GetName()

    def get_preset_list(self) -> list:
        """Returns a list of presets and their information."""
        return self.project.GetPresetList()

    def get_render_codecs(self, render_format: str) -> dict:
        """returns a dict with render codecs for a given render format.

        Args:
            render_format (str): render format

        Returns:
            dict: codec description -> codec name
        """
        return self.project.GetRenderCodecs(render_format)

    def get_render_formats(self) -> dict:
        """Returns a dict (format -> file extension) of available render formats."""
        return self.project.GetRenderFormats()

    def get_render_job_list(self) -> list:
        """Returns a list of render jobs and their information."""
        return self.project.GetRenderJobList()

    def get_render_job_status(self, job_id: str) -> dict:
        """Returns a dict with job status and completion percentage of the job by given jobId (string)."""
        return self.project.GetRenderJobStatus(job_id)

    def get_render_preset_list(self):
        """Returns a list of render presets and their information."""
        return self.project.GetRenderPresetList()

    def get_render_resolutions(self, format: str, codec: str) -> RenderResolution:
        """Returns list of resolutions applicable for the given render format (string) and render codec (string). 

        Args:
            format (str): format
            codec (str): codec

        Returns:
            RenderResolution: Returns full list of resolutions if no argument is provided. Each element in the list is a dictionary with 2 keys "Width" and "Height".
        """
        #Sample: current_project.get_render_resolutions(format='mp4',codec='h264')
        return self.project.GetRenderResolutions(format, codec)

    def get_setting(self, setting_name: str="") -> str:
        """Returns value of project setting (indicated by setting_name, string). """
        # call *without parameters/NoneType * to get a snapshot of all queryable properties
        return self.project.GetSetting(setting_name)

    def get_timeline_by_index(self, idx) ->Timeline:
        """Returns Timeline at the given index, 1 <= idx <= project.get_timeline_count()"""
        return Timeline(timeline=self.project.GetTimelineByIndex(idx))

    def get_timeline_count(self) -> int:
        """Returns the number of timelines currently present in the project."""
        return self.project.GetTimelineCount()

    def is_rendering_in_progress(self) -> bool:
        """Returns True if rendering is in progress."""
        return self.project.IsRenderingInProgress()

    def load_render_preset(self, preset_name) -> bool:
        """Sets a preset as current preset for rendering if preset_name (string) exists."""
        return self.project.LoadRenderPreset(preset_name)

    def refresh_lut_list(self) -> bool:
        """Refreshes LUT List"""
        return self.project.RefreshLUTList()

    def save_as_new_render_preset(self, preset_name) -> bool:
        """Creates new render preset by given name if preset_name(string) is unique."""
        return self.project.SaveAsNewRenderPreset(preset_name)

    def set_current_render_format_and_codec(self, format: str, codec: str) -> bool:
        """Sets given render format (string) and render codec (string) as options for rendering."""
        return self.project.SetCurrentRenderFormatAndCodec(format, codec)

    def set_current_render_mode(self, render_mode: int) -> bool:
        """Sets the render mode. 

        Args:
            render_mode (int): Specify renderMode = 0 for Individual clips, 1 for Single clip.

        Returns:
            bool: True if successful.
        """
        return self.project.SetCurrentRenderMode(render_mode)

    def set_current_timeline(self, timeline: Timeline) -> bool:
        """Sets given Timeline as current timeline for the project. Returns True if successful."""
        return self.project.SetCurrentTimeline(timeline.timeline)

    def set_name(self, project_name) -> bool:
        """Sets project name if given project_name (string) is unique."""
        return self.project.SetName(project_name)

    def set_preset(self, preset_name: str) -> bool:
        """Sets preset by given preset_name (string) into project."""
        return self.project.SetPreset(preset_name)

    def set_render_setting(self, render_setting: RenderSetting) -> bool:
        """Sets given settings for rendering.

        Args:
            render_setting (RenderSetting): RenderSetting object

        Returns:
            bool: True if successful.
        """       
        return self.project.SetRenderSetting(asdict(render_setting))

    def set_setting(self, setting_name: str, setting_value: str):
        """Sets value of project setting (indicated by setting_name, string).

        Args:
            setting_name (str): Setting name
            setting_value (str): Setting value

        Returns:
            _type_: True if successful.
        """        
        return self.project.SetSetting(setting_name, setting_value)

    def start_rendering(self, job_ids: list, is_interactive_mode=False) -> bool:
        """Start rendering. Returns True if successful.
        if job_ids==None render all queued render jobs.
        """
        return self.project.StartRendering(job_ids, is_interactive_mode)

    def stop_rendering(self):
        """Stops rendering."""
        return self.project.StopRendering()
    
    ##############################################################################################################################
    #Add at DR18.0.0

    def get_unique_id(self) -> str:
        """Returns unique id of the project Object."""
        return self.project.GetUniqueId()


    