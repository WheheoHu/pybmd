from typing import TYPE_CHECKING, Any, Dict, List
from pybmd._wrapper_base import WrapperBase
from pybmd.color_group import ColorGroup
from pybmd.decorators import requires_resolve_version
from pybmd.gallery import Gallery
from pybmd.media_pool import MediaPool
from pybmd.media_pool_item import MediaPoolItem

from pybmd.timeline import Timeline

if TYPE_CHECKING:
    from pybmd.settings import (
        ProjectSettingsPresetInfo,
        RenderSetting,
        SpeechGenerationSettings,
    )

RenderResolution = List[dict]


class Project(WrapperBase):
    """Project Object"""

    def __init__(self, project):
        super(Project, self).__init__(project)
        self._project = self._object

    def __repr__(self) -> str:
        return f"Project: {self.get_name()}"

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

    @requires_resolve_version(
        deprecated_in="21.1.0",
        moved_to="Project.get_project_settings_preset_list",
        notes="Use get_project_settings_preset_list() instead",
    )
    def get_preset_list(self) -> list:
        """Returns a list of presets and their information.

        Deprecated:
            Deprecated since DaVinci Resolve 21.1.0, use
            :meth:`get_project_settings_preset_list` instead.
        """
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

    @requires_resolve_version(
        deprecated_in="21.1.0",
        moved_to="Project.get_settings",
        notes="Use get_settings() and index into the returned dict instead",
    )
    def get_setting(self, setting_name: str = "") -> str:
        """Returns value of project setting (indicated by setting_name, string).

        Deprecated:
            Deprecated calling convention since DaVinci Resolve 21.1.0, use
            :meth:`get_settings` and index into the returned dict instead.
        """
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

    @requires_resolve_version(
        deprecated_in="21.1.0",
        moved_to="Project.set_project_settings_preset",
        notes="Use set_project_settings_preset() instead",
    )
    def set_preset(self, preset_name: str) -> bool:
        """Sets preset by given preset_name (string) into project.

        Deprecated:
            Deprecated since DaVinci Resolve 21.1.0, use
            :meth:`set_project_settings_preset` instead.
        """
        return self._project.SetPreset(preset_name)

    def set_render_settings(self, render_setting: "RenderSetting | dict") -> bool:
        """Sets given settings for rendering.

        Only fields explicitly provided by the user are sent to DaVinci Resolve;
        any unset field keeps its current value in DR (partial update).

        Args:
            render_setting: A RenderSetting object or a dict of setting overrides.

        Returns:
            bool: True if successful.
        """
        if isinstance(render_setting, dict):
            return self._project.SetRenderSettings(render_setting)
        return self._project.SetRenderSettings(
            render_setting.model_dump(exclude_unset=True)
        )

    @requires_resolve_version(
        deprecated_in="21.1.0",
        moved_to="Project.set_settings",
        notes='Use set_settings({setting_name: setting_value}) instead',
    )
    def set_setting(self, setting_name: str, setting_value: str):
        """Sets value of project setting (indicated by setting_name, string).

        Args:
            setting_name (str): Setting name
            setting_value (str): Setting value

        Returns:
            _type_: True if successful.

        Deprecated:
            Deprecated calling convention since DaVinci Resolve 21.1.0, use
            ``set_settings({setting_name: setting_value})`` instead.
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

    @requires_resolve_version(added_in="18.0.0")
    def get_unique_id(self) -> str:
        """Returns unique id of the project Object.

        Returns:
            str: Unique project ID

        Raises:
            APIVersionError: If Resolve version < 18.0.0

        Version:
            Added in DaVinci Resolve 18.0.0
        """
        return self._project.GetUniqueId()

    ##############################################################################################################################
    # Add at DR18.1.3

    @requires_resolve_version(added_in="18.1.3")
    def insert_audio_to_current_track_at_playhead(
        self, media_path: str, start_offset_in_samples: int, duration_in_samples: int
    ) -> bool:
        """Inserts the media specified by mediaPath (string) with startOffsetInSamples (int) and durationInSamples (int) at the playhead on a selected track on the Fairlight page.

        Args:
            media_path (str)
            start_offset_in_samples (int)
            duration_in_samples (int)

        Returns:
            bool: Returns True if successful, otherwise False.

        Raises:
            APIVersionError: If Resolve version < 18.1.3

        Version:
            Added in DaVinci Resolve 18.1.3
        """
        return self._project.InsertAudioToCurrentTrackAtPlayhead(
            media_path, start_offset_in_samples, duration_in_samples
        )

    ##############################################################################################################################
    # Add at DR18.5.0 Beta

    @requires_resolve_version(added_in="18.5.0")
    def load_burn_in_preset(self, preset_name: str) -> bool:
        """Loads user defined data burn in preset for project when supplied presetName (string).

        Args:
            preset_name (str): preset name

        Returns:
            bool: Returns true if successful.

        Raises:
            APIVersionError: If Resolve version < 18.5.0

        Version:
            Added in DaVinci Resolve 18.5.0 Beta
        """
        return self._project.LoadBurnInPreset(preset_name)

    ##############################################################################################################################
    # Add at DR18.5.0

    @requires_resolve_version(added_in="18.5.0")
    def export_current_frame_as_still(self, file_path: str) -> bool:
        """Exports current frame as still to supplied filePath.

        Args:
            file_path (str): exported still path.filePath must end in valid export file format.

        Returns:
            bool: Returns True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 18.5.0

        Version:
            Added in DaVinci Resolve 18.5.0
        """
        return self._project.ExportCurrentFrameAsStill(file_path)

    ##############################################################################################################################
    # Add at DR 19.0.0
    @requires_resolve_version(added_in="19.0.0")
    def get_color_groups_list(self) -> List[ColorGroup]:
        """Returns a list of all group objects in the timeline.

        Returns:
            List[ColorGroup]: a list of all group objects

        Raises:
            APIVersionError: If Resolve version < 19.0.0

        Version:
            Added in DaVinci Resolve 19.0.0
        """
        color_group_list = list()
        for color_group in self._project.GetColorGroupsList():
            color_group_list.append(ColorGroup(color_group))
        return color_group_list

    @requires_resolve_version(added_in="19.0.0")
    def add_color_group(self, group_name: str) -> ColorGroup:
        """Creates a new ColorGroup.

        Args:
            group_name (str): groupName must be a unique string.

        Returns:
            ColorGroup: ColorGroup object if successful, otherwise None.
        """
        return ColorGroup(self._project.AddColorGroup(group_name))

    def delete_color_group(self, color_group: ColorGroup) -> bool:
        """Deletes the given color group and sets clips to ungrouped.

        Args:
            color_group (ColorGroup): color group object to delete

        Returns:
            bool: Return True if successful, otherwise False.
        """
        return self._project.DeleteColorGroup(color_group._color_group)

    ##############################################################################################################################
    # Add at DR 19.1.0

    @requires_resolve_version(added_in="19.1.0")
    def delete_render_preset(self, preset_name: str) -> bool:
        """Delete render preset by provided name

        Args:
            preset_name (str): preset name

        Returns:
            bool: Returns True if successful, otherwise False.

        Raises:
            APIVersionError: If Resolve version < 19.1.0

        Version:
            Added in DaVinci Resolve 19.1.0
        """
        return self._project.DeleteRenderPreset(preset_name)

    @requires_resolve_version(added_in="19.1.0")
    def get_quick_export_render_presets(self) -> List[str]:
        """
        Returns a list of names of all Quick Export render presets.
        """
        return self._project.GetQuickExportRenderPresets()

    @requires_resolve_version(added_in="19.1.0")
    def render_with_quick_export(
        self, preset_name: str, param_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Starts a Quick Export render using the specified preset name and parameter dictionary.

        Args:
            preset_name (str): The name of the Quick Export render preset.
            param_dict (Dict[str, Any]): Dictionary of render settings, supported keys include "TargetDir", "CustomName", "VideoQuality", and "EnableUpload".("EnableUpload" key enables direct upload for supported web presets.)

        Returns:
            Dict[str, Any]: A dictionary containing the job status and render time, or an error string if the render failed or was not attempted.
        """
        return self._project.RenderWithQuickExport(preset_name, param_dict)

    ##############################################################################################################################
    # Add at DR 20.3.0

    @requires_resolve_version(added_in="20.3.0")
    def apply_fairlight_preset_to_current_timeline(self, preset_name: str) -> bool:
        """Applies a Fairlight preset to the current timeline.

        Args:
            preset_name (str): Name of the Fairlight preset to apply.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 20.3.0

        Version:
            Added in DaVinci Resolve 20.3.0
        """
        return self._project.ApplyFairlightPresetToCurrentTimeline(preset_name)

    ##############################################################################################################################
    # Add at DR 21.0.2

    @requires_resolve_version(added_in="21.0.2")
    def reset_intellisearch_analysis(self) -> bool:
        """Clears Intellisearch analysis data.

        Studio-only. Refer to DaVinci Resolve's "Studio and AI Scripting APIs"
        prerequisites; returns False if requirements are not met.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.0.2

        Version:
            Added in DaVinci Resolve 21.0.2
        """
        return self._project.ResetIntellisearchAnalysis()

    @requires_resolve_version(added_in="21.0.2")
    def generate_speech(
        self,
        speech_generation_settings: "SpeechGenerationSettings | dict",
        timecode: str,
    ) -> MediaPoolItem:
        """Generates an audio MediaPoolItem from the given speech generation settings.

        Adds the generated clip to the timeline at ``timecode`` when the settings'
        ``AddToTimeline`` is True. Studio-only (requires the AI Speech Generator
        Extras download); returns the API's result unwrapped if requirements are not met.

        Args:
            speech_generation_settings (SpeechGenerationSettings | dict): Speech
                generation settings. A ``SpeechGenerationSettings`` model or a raw dict.
            timecode (str): Timecode at which to add the generated clip to the timeline.

        Returns:
            MediaPoolItem: The newly generated audio MediaPoolItem.

        Raises:
            APIVersionError: If Resolve version < 21.0.2

        Version:
            Added in DaVinci Resolve 21.0.2
        """
        if isinstance(speech_generation_settings, dict):
            settings_dict = speech_generation_settings
        else:
            settings_dict = speech_generation_settings.model_dump(exclude_none=True)
        return MediaPoolItem(self._project.GenerateSpeech(settings_dict, timecode))

    ##############################################################################################################################
    # Add at DR 21.1.0

    @requires_resolve_version(added_in="21.1.0")
    def get_settings(self) -> Dict:
        """Returns a dict with all project settings.

        This is the dict-based replacement for the single-key
        :meth:`get_setting`. Refer to DaVinci Resolve's "Project and Clip
        Properties" documentation for the supported keys.

        Returns:
            Dict: all project settings

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.GetSettings()

    @requires_resolve_version(added_in="21.1.0")
    def set_settings(self, settings: Dict) -> bool:
        """Sets the project settings with the specified dict of setting names and values.

        This is the dict-based replacement for the single-key :meth:`set_setting`.

        Args:
            settings (Dict): dict of setting names and values

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.SetSettings(settings)

    @requires_resolve_version(added_in="21.1.0")
    def get_project_settings_preset_list(self) -> List["ProjectSettingsPresetInfo"]:
        """Returns a list of project settings presets and their information.

        Returns:
            List[ProjectSettingsPresetInfo]: preset information (``Name``, ``Width``,
                ``Height``)

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        from pybmd.settings import ProjectSettingsPresetInfo

        return [
            ProjectSettingsPresetInfo(**preset_info)
            for preset_info in self._project.GetProjectSettingsPresetList()
        ]

    @requires_resolve_version(added_in="21.1.0")
    def set_project_settings_preset(self, preset_name: str) -> bool:
        """Sets the project settings preset named preset_name into the project.

        Args:
            preset_name (str): name of the project settings preset

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.SetProjectSettingsPreset(preset_name)

    @requires_resolve_version(added_in="21.1.0")
    def update_project_settings_preset(self, preset_name: str) -> bool:
        """Updates the project settings preset named preset_name with the current settings.

        Args:
            preset_name (str): name of the project settings preset

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.UpdateProjectSettingsPreset(preset_name)

    @requires_resolve_version(added_in="21.1.0")
    def delete_project_settings_preset(self, preset_name: str) -> bool:
        """Deletes the project settings preset named preset_name.

        Args:
            preset_name (str): name of the project settings preset

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.DeleteProjectSettingsPreset(preset_name)

    @requires_resolve_version(added_in="21.1.0")
    def import_project_settings_preset(
        self, preset_file_path: str, preset_name: str = ""
    ) -> bool:
        """Imports a project settings preset from preset_file_path.

        Args:
            preset_file_path (str): path of the preset file
            preset_name (str, optional): how the preset shall be named. If not specified,
                the preset is named based on the file base name.

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.ImportProjectSettingsPreset(
            str(preset_file_path), preset_name
        )

    @requires_resolve_version(added_in="21.1.0")
    def export_project_settings_preset(
        self, preset_name: str, export_path: str
    ) -> bool:
        """Exports the project settings preset named preset_name to export_path.

        Args:
            preset_name (str): name of the project settings preset
            export_path (str): path to export to

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.ExportProjectSettingsPreset(preset_name, str(export_path))

    @requires_resolve_version(added_in="21.1.0")
    def save_current_project_settings_as_new_preset(self, preset_name: str) -> bool:
        """Saves the current project settings as a new preset named preset_name.

        Args:
            preset_name (str): name of the new project settings preset

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.SaveCurrentProjectSettingsAsNewPreset(preset_name)

    @requires_resolve_version(added_in="21.1.0")
    def update_render_preset(self, preset_name: str) -> bool:
        """Updates the render preset named preset_name with the current render settings.

        Args:
            preset_name (str): name of the render preset

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.UpdateRenderPreset(preset_name)

    @requires_resolve_version(added_in="21.1.0")
    def set_quick_export_enabled_for_render_preset(
        self, preset_name: str, is_enabled: bool
    ) -> bool:
        """Enables or disables quick export for the render preset named preset_name.

        Args:
            preset_name (str): name of the render preset
            is_enabled (bool): True to enable quick export, False to disable it

        Returns:
            bool: True if successful, False otherwise.

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.SetQuickExportEnabledForRenderPreset(
            preset_name, is_enabled
        )

    @requires_resolve_version(added_in="21.1.0")
    def get_audio_render_formats(self) -> Dict[str, str]:
        """Returns a dict of available audio render formats.

        Maps each format description to its file extension, e.g.
        ``{"QuickTime": "mov", "Wave": "wav", ...}``.

        Returns:
            Dict[str, str]: format description -> file extension

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.GetAudioRenderFormats()

    @requires_resolve_version(added_in="21.1.0")
    def get_audio_render_codecs(
        self, audio_render_format_file_extension: str
    ) -> Dict[str, str]:
        """Returns the audio codecs available for the given audio render format.

        Args:
            audio_render_format_file_extension (str): file extension of the audio render
                format, as returned by :meth:`get_audio_render_formats`, e.g. ``"mov"``.

        Returns:
            Dict[str, str]: codec description -> codec name

        Raises:
            APIVersionError: If Resolve version < 21.1.0

        Version:
            Added in DaVinci Resolve 21.1.0
        """
        return self._project.GetAudioRenderCodecs(audio_render_format_file_extension)

    ##############################################################################################################################
    # More function BELOW!

    def set_super_scale_enhanced(
        self, sharpness: float, noise_reduction: float
    ) -> bool:
        """Sets Super Scale to the "2x Enhanced" multiplier.

        "2x Enhanced" is the one Super Scale mode that cannot be selected through
        :meth:`set_settings`: it needs the four-argument
        ``SetSetting("superScale", 2, sharpness, noiseReduction)`` calling convention,
        which is the only ``SetSetting`` convention DaVinci Resolve 21.1.0 did *not*
        deprecate, precisely because it has no ``SetSettings`` equivalent.

        Every other Super Scale multiplier goes through
        ``set_settings({"superScale": value})`` with 0=Auto, 1=none, 2=2x, 3=3x, 4=4x.

        Args:
            sharpness (float): sharpness strength, in the range [0.0, 1.0]
            noise_reduction (float): noise reduction strength, in the range [0.0, 1.0]

        Returns:
            bool: True if successful, False otherwise

        Note:
            Read the applied strengths back with the read-only settings
            ``superScaleSharpnessStrength`` and ``superScaleNoiseReductionStrength``.
            Both strengths persist until this method changes them again - selecting
            another multiplier through :meth:`set_settings` leaves them untouched.
        """
        return self._project.SetSetting("superScale", 2, sharpness, noise_reduction)
