

from dataclasses import asdict
from dataclasses import dataclass
from typing import Any, List
from pybmd.gallery import Gallery
from pybmd.media_pool import MediaPool

from pybmd.timeline import Timeline


RenderResolution = List[dict]


@dataclass
class RenderSetting():
    """Docstring for RenderSetting."""
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
    VideoQuality: Any
    #  possible values for current codec (if applicable):

    #  0(int) - will set quality to automatic

    # [1 -> MAX] (int) - will set input bit rate

    # ["Least", "Low", "Medium", "High", "Best"] (String) - will set input quality level
    AudioCodec: str
    AudioBitDepth: int
    AudioSampleRate: int
    ColorSpaceTag: str  # example: "Same as Project", "AstroDesign"
    GammaTag: str  # example: "Same as Project", "ACEScct"
    ExportAlpha: bool
    # (example: "Main10"). Can only be set for H.264 and H.265.
    EncodingProfile: str
    MultiPassEncode: bool  # Can onlt be set for H.264.
    AlphaMode: int
    # 0 - Premultipled, 1 - Straight. Can only be set if "ExportAlpha" is true.
    NetworkOptimization: bool  # Only supported by QuickTime and MP4 formats.


class Project():
    """docstring for Project."""

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
        return self.project.DeleteAllRenderJobs()

    def delete_render_job(self, job_id: str) -> bool:
        return self.project.DeleteRenderJob(job_id)

    def get_current_render_format_and_codec(self) -> dict:
        return self.project.GetCurrentRenderFormatAndCodec()

    def get_current_render_mode(self) -> int:
        return self.project.GetCurrentRenderMode()

    def get_current_timeline(self):
        return Timeline(timeline=self.project.GetCurrentTimeline())

    def get_gallery(self,) -> Gallery:
        return Gallery(self.project.GetGallery())

    def get_media_pool(self) -> MediaPool:
        return MediaPool(self.project.GetMediaPool())

    def get_name(self) -> str:
        return self.project.GetName()

    def get_preset_list(self) -> list:
        return self.project.GetPresetList()

    def get_render_codecs(self, render_format: str) -> dict:
        return self.project.GetRenderCodecs(render_format)

    def get_render_formats(self) -> dict:
        return self.project.GetRenderFormats()

    def get_render_job_list(self) -> list:
        return self.project.GetRenderJobList()

    def get_render_job_status(self, job_id: str) -> dict:
        return self.project.GetRenderJobStatus(job_id)

    def get_render_preset_list(self):
        return self.project.GetRenderPresetList()

    def get_render_resolutions(self, format: str, codec: str) -> RenderResolution:
        #Sample: current_project.get_render_resolutions(format='mp4',codec='h264')
        return self.project.GetRenderResolutions(format, codec)

    def get_setting(self, setting_name: str) -> str:
        # call *without parameters/NoneType * to get a snapshot of all queryable properties
        return self.project.GetSetting(setting_name)

    def get_timeline_by_index(self, idx):
        return Timeline(timeline=self.project.GetTimelineByIndex(idx))

    def get_timeline_count(self) -> int:
        return self.project.GetTimelineCount()

    def is_rendering_in_progress(self) -> bool:
        return self.project.IsRenderingInProgress()

    def load_render_preset(self, preset_name) -> bool:
        return self.project.LoadRenderPreset(preset_name)

    def refresh_lut_list(self) -> bool:
        return self.project.RefreshLUTList()

    def save_as_new_render_preset(self, preset_name) -> bool:
        return self.project.SaveAsNewRenderPreset(preset_name)

    def set_current_render_format_and_codec(self, format: str, codec: str) -> bool:
        return self.project.SetCurrentRenderFormatAndCodec(format, codec)

    def set_current_render_mode(self, render_mode: int) -> bool:
        return self.project.SetCurrentRenderMode(render_mode)

    def set_current_timeline(self, timeline: Timeline) -> bool:
        return self.project.SetCurrentTimeline(timeline.timeline)

    def set_name(self, project_name) -> bool:
        return self.project.SetName(project_name)

    def set_preset(self, preset_name: str) -> bool:
        return self.project.SetPreset(preset_name)

    def set_render_setting(self, render_setting: RenderSetting) -> bool:
        return self.project.SetRenderSetting(asdict(render_setting))

    def set_setting(self, setting_name: str, setting_value: str):
        return self.project.SetSetting(setting_name, setting_value)

    def start_rendering(self, job_ids: list, is_interactive_mode=False) -> bool:
        # if job_ids==None render all queued render jobs.
        return self.project.StartRendering(job_ids, is_interactive_mode)

    def stop_rendering(self):
        return self.project.StopRendering()

