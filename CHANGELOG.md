# Change Log for PyBMD

# 2026.3.0
## API
### Changes for DaVinci Resolve 21.0.3 / 21.0.4 / 21.1.0

### Resolve
- Add `get_layout_preset_list()` - Returns the list of UI layout presets (DR 21.0.3)
- Add `get_burn_in_preset_list()` - Returns the list of data burn-in presets (DR 21.0.3)
- Add `delete_burn_in_preset()` - Deletes the given data burn-in preset (DR 21.0.3)
- Add `get_user_preferences_preset_list()` - Returns the list of user preferences presets (DR 21.0.3)
- Add `load_user_preferences_preset()` - Loads the given user preferences preset (DR 21.0.3)
- Add `save_user_preferences_preset()` - Saves the current user preferences as a preset (DR 21.0.3)
- Add `delete_user_preferences_preset()` - Deletes the given user preferences preset (DR 21.0.3)
- Add `import_user_preferences_preset()` - Imports a user preferences preset from a file (DR 21.0.3)
- Add `export_user_preferences_preset()` - Exports a user preferences preset to a file (DR 21.0.3)
- Add `get_current_project()` - Shortcut for `get_project_manager().get_current_project()` (DR 21.1.0)
- Add `get_current_timeline()` - Shortcut for the current project's current timeline, `None` when there is none (DR 21.1.0)
- Add `get_media_pool()` - Shortcut for the current project's media pool (DR 21.1.0)
- Add `get_gallery()` - Shortcut for the current project's gallery (DR 21.1.0)
- Add `get_keyboard_preset_list()` - Returns the list of keyboard customization presets (DR 21.1.0)
- Add `get_current_keyboard_preset()` - Returns the name of the active keyboard preset (DR 21.1.0)
- Add `load_keyboard_preset()` - Loads the given keyboard preset (DR 21.1.0)
- Add `delete_keyboard_preset()` - Deletes the given keyboard preset (DR 21.1.0)
- Add `import_keyboard_preset()` - Imports a keyboard preset from a file (DR 21.1.0)
- Add `export_keyboard_preset()` - Exports a keyboard preset to a file (DR 21.1.0)
- Add `validate_dctl()` - Validates DCTL source; returns `None` when the source is valid, an error string otherwise (DR 21.1.0)
- Add `encrypt_dctl()` - Encrypts a DCTL file using `EncryptDCTLOptions` (DR 21.1.0)

### Project
- Add `get_settings()` - Returns all project settings as a dict (DR 21.1.0)
- Add `set_settings()` - Sets multiple project settings from a dict in one call (DR 21.1.0)
- Add `get_project_settings_preset_list()` - Returns a list of `ProjectSettingsPresetInfo` (DR 21.1.0)
- Add `set_project_settings_preset()` - Applies the given project settings preset (DR 21.1.0)
- Add `update_project_settings_preset()` - Updates the preset with the current project settings (DR 21.1.0)
- Add `delete_project_settings_preset()` - Deletes the given project settings preset (DR 21.1.0)
- Add `import_project_settings_preset()` - Imports a project settings preset from a file (DR 21.1.0)
- Add `export_project_settings_preset()` - Exports a project settings preset to a file (DR 21.1.0)
- Add `save_current_project_settings_as_new_preset()` - Saves the current settings as a new preset (DR 21.1.0)
- Add `update_render_preset()` - Updates a render preset with the current render settings (DR 21.1.0)
- Add `set_quick_export_enabled_for_render_preset()` - Shows/hides a render preset in Quick Export (DR 21.1.0)
- Add `get_audio_render_formats()` - Returns the supported audio-only render formats (DR 21.1.0)
- Add `get_audio_render_codecs()` - Returns the audio codecs available for a render format (DR 21.1.0)
- Add `set_super_scale_enhanced()` - Selects the "2x Enhanced" Super Scale multiplier. This needs the four-argument `SetSetting("superScale", 2, sharpness, noiseReduction)` convention, the only `SetSetting` convention DaVinci Resolve 21.1.0 did *not* deprecate, because it has no `set_settings()` equivalent

### ProjectManager
- Add `get_project_attributes_in_current_folder()` - Returns a `{project_name: ProjectAttributes}` dict for the current folder (DR 21.0.3)

### Timeline
- Add `get_selected_clips()` - Returns the timeline items currently selected in the UI (DR 21.0.4)
- Add `get_settings()` - Returns all timeline settings as a dict (DR 21.1.0)
- Add `set_settings()` - Sets multiple timeline settings from a dict in one call (DR 21.1.0)
- Add `get_output_blanking()` / `set_output_blanking()` - Reads/writes the timeline output blanking using `OutputBlanking` (DR 21.1.0)
- Add `get_normalize_audio_modes()` - Returns the available audio normalization modes (DR 21.1.0)
- Add `normalize_audio_level()` - Normalizes the audio level of the given timeline items using `NormalizeAudioOptions` (DR 21.1.0)
- Add `auto_align_clips()` - Auto-aligns the given timeline items using `AutoAlignOptions` (DR 21.1.0)

### TimelineItem
- Add `get_type()` - Returns the item type (`"video"`, `"audio"`, `"generator"`, `"transition"`) (DR 21.1.0)
- Add `get_properties()` / `set_properties()` - Reads/writes all item properties at once using `TimelineItemProperties` (DR 21.1.0)
- Add `get_fades()` / `set_fades()` - Reads/writes fade in/out using `FadeInfo` (DR 21.1.0)
- Add `get_speed()` / `set_speed()` - Reads/writes retime speed using `SpeedOptions` (DR 21.1.0)
- Add `get_output_blanking()` / `set_output_blanking()` - Per-item output blanking; the getter returns `{}` while the item follows the timeline (DR 21.1.0)
- Add `get_use_timeline_for_output_blanking()` / `set_use_timeline_for_output_blanking()` (DR 21.1.0)
- Add `add_transition()` - Adds a transition described by `TransitionOptions`, returns the new `TimelineItem` (DR 21.1.0)
- Add `flatten_multicam()` - Flattens a multicam clip using a `FlattenMulticamGradeOption` (DR 21.1.0)
- Add `perform_multicam_smart_switch()` - Runs multicam smart switch using `SmartSwitchSettings` (Studio/AI) (DR 21.1.0)
- Add `set_source_audio_channel_mapping()` - Sets the source audio channel mapping from a JSON string (DR 21.1.0)

### MediaPool
- Add `create_multicam_clip()` - Creates multicam clips from the given `MediaPoolItem` list using `MulticamOptions` (DR 21.1.0)
- Add `ImportClipInfo` dataclass - `clipInfo` entry for `import_media`, so an image sequence can be imported as a single `MediaPoolItem`
- Add `import_media()` overloads accepting `List[ImportClipInfo]` and `List[dict]`

### MediaPoolItem
- Add `get_timeline()` - Returns the `Timeline` a timeline-type media pool item represents (DR 21.0.4)
- Add `get_transcription()` - Returns the clip transcription as a `Transcription` model (DR 21.1.0)
- Add `set_audio_mapping()` - Sets the clip audio mapping from a JSON string (DR 21.1.0)
- Update `set_metadata()` - Now also accepts a metadata dict, e.g. `set_metadata({"Scene": "42"})`

### MediaStorage
- Add `start_clone_media()` - Starts a clone job from a source folder to one or more target folders (DR 21.1.0)
- Add `stop_clone_media()` - Stops the running clone job (DR 21.1.0)
- Add `get_clone_status()` - Returns the clone job status as a `CloneStatus` model (DR 21.1.0)
- Add `set_clone_tool_settings()` - Sets the clone tool settings from `CloneToolSettings`; resets to defaults when called without arguments (DR 21.1.0)

### settings module
- Add write models: `CloneToolSettings`, `NormalizeAudioOptions`, `AutoAlignOptions`, `EncryptDCTLOptions`, `OutputBlanking`, `FadeInfo`, `SpeedOptions`, `TransitionOptions`, `MulticamOptions`, `SmartSwitchSettings`, `TimelineItemProperties`
- Add read models: `CloneStatus`, `ProjectSettingsPresetInfo`, `ProjectAttributes`, `Transcription`, `TranscriptionSegment`, `TranscriptionWord`
- Add enums: `CloneChecksumType`, `NormalizeAudioSetLevelMode`, `AutoAlignSyncUsing`, `AutoAlignWaveformTrack`, `MulticamAngleSyncMode`, `MulticamAudioMode`, `MulticamAngleNameMode`, `MulticamDetectSameCameraClipsMode`, `FlattenMulticamGradeOption`, `SmartSwitchAnalysisMode`, `SmartSwitchWideAngleFrequency`, `SmartSwitchQuality`, `DynamicZoomEase`, `CompositeMode`, `RetimeProcess`, `MotionEstimation`, `Scaling`, `ResizeFilter`, `DialogueLevelerMode`
- Add `RenderSetting` keys: `ClipStartFrame`, `TimelineStartTimecode`, `ReplaceExistingFilesInPlace`, `UseFullExtents`, `AddFrameHandles`, `DataBurnIn`
- Update `AudioSyncChannel` - Now reads the `AUDIO_SYNC_CHANNEL_AUTOMATIC` / `AUDIO_SYNC_CHANNEL_MIX` constants instead of hardcoded values
- Add the DR 21.1.0 constants to the `ResolveObject` protocol in `_resolve_types.py` (clone checksum types, normalize audio modes, auto align, multicam, flatten multicam, smart switch, dynamic zoom ease, composite modes, retime process, motion estimation incl. `MOTION_EST_METAL`, scaling, resize filters, dialogue leveler modes)

## Deprecations
DaVinci Resolve 21.1.0 deprecates several calling conventions. Nothing is removed - the wrappers
below keep working and now emit an `APIDeprecationWarning` when the deprecated form is used.

### Project
- `get_setting()` → `get_settings()`
- `set_setting()` → `set_settings({setting_name: setting_value})`
- `get_preset_list()` → `get_project_settings_preset_list()`
- `set_preset()` → `set_project_settings_preset()`

### Timeline
- `get_setting()` → `get_settings()`
- `set_setting()` → `set_settings({setting_name: setting_value})`

### TimelineItem
- `get_property()` → `get_properties()`
- `set_property()` → `set_properties({property_key: property_value})`

### MediaPool
- `append_to_timeline([MediaPoolItem])` → `append_to_timeline([ClipInfo])`
- `create_timeline_from_clips(name, [MediaPoolItem])` → `create_timeline_from_clips(name, [ClipInfo])`
- `import_media([path])` → `import_media([ImportClipInfo])`

### MediaPoolItem
- `get_metadata(metadata_type)` → `get_metadata()` and index into the returned dict
- `get_clip_property(property_name)` → `get_clip_property()` and index into the returned dict
- `set_metadata(metadata_type, metadata_value)` → `set_metadata({metadata_type: metadata_value})`
- `set_third_party_metadata(metadata_type, metadata_value)` → `set_third_party_metadata({metadata_type: metadata_value})`

### MediaStorage
- `add_item_list_to_media_pool([path])` → `add_item_list_to_media_pool([Item_Info(media=path)])`

## Fixes
### MediaStorage
- Fix `Item_Info` to serialize as the `startFrame` / `endFrame` keys DaVinci Resolve expects (they were sent as `start_frame` / `end_frame`, so `add_item_list_to_media_pool` silently ignored the frame range). Both the snake_case field names and the Resolve key names are accepted on init
- Fix `set_clone_tool_settings()` to send an empty dict when resetting to defaults; calling `SetCloneToolSettings()` with no argument returns False
- Document that every `start_clone_media()` target folder has to exist already - DaVinci Resolve returns False instead of creating it

### MediaPool
- Fix `create_timeline_from_clips(name, [MediaPoolItem])` to unwrap each item before passing it to the API
- Fix `create_timeline_from_clips(name, [ClipInfo])` to serialize each `ClipInfo` via `to_dict()`; it previously passed the `ClipInfo` *class* through `asdict()` and emitted snake_case keys
- Fix `ClipInfo` to only require `media_pool_item`; `start_frame`, `end_frame`, `media_type`, `track_index` and `record_frame` now default to `None` and are omitted from the dict handed to DaVinci Resolve. This makes `[ClipInfo(media_pool_item=item)]` - the migration path for the deprecated `[MediaPoolItem]` convention - expressible
- Fix `import_media()` to return an empty list instead of raising `TypeError` when DaVinci Resolve returns nothing, and document that the `clipInfo` conventions only import image sequences (entries carrying `start_index` / `end_index`)

### settings module
- Fix `CloneStatus.JobStatus` to accept any string; DaVinci Resolve reports statuses beyond the documented set, e.g. `"InProgress"` while a clone job runs

### decorators
- Fix deprecation warnings raised from `@multimethod` overloads to blame the calling line instead of multimethod's dispatch machinery
- Add `warn_deprecated_calling_convention()` for APIs where only one *calling convention* was deprecated, which is known at call time rather than at decoration time

----
# 2026.2.0
## API
### Changes for DaVinci Resolve 21.0.2

### Resolve
- Add `disable_background_tasks_for_current_resolve_session()` - Disables all background tasks for the current Resolve session

### Project
- Add `reset_intellisearch_analysis()` - Clears Intellisearch analysis data (Studio/AI)
- Add `generate_speech()` - Generates an audio `MediaPoolItem` from `SpeechGenerationSettings` and (optionally) adds it to the timeline at a given timecode (Studio/AI)

### MediaPoolItem
- Add `perform_audio_classification()` - Classifies the clip's audio into categories/subcategories (Studio/AI)
- Add `clear_audio_classification()` - Clears the clip's audio classification (Studio/AI)
- Add `remove_motion_blur()` - Applies motion deblur, returns the new `MediaPoolItem` (Studio/AI)
- Add `analyze_for_intellisearch()` - Runs Intellisearch analysis (Studio/AI)
- Add `analyze_for_slate()` - Runs Slate analysis using a `MarkerColor` (Studio/AI)
- Update `transcribe_audio()` - Add optional `use_speaker_detection` parameter

### Folder
- Add `perform_audio_classification()`, `clear_audio_classification()`, `analyze_for_intellisearch()`, `analyze_for_slate()` (Studio/AI)
- Add `remove_motion_blur()` - Returns a list of `[original, new]` `MediaPoolItem` pairs (Studio/AI)
- Update `transcribe_audio()` - Add optional `use_speaker_detection` parameter

### settings module
- Add `SpeechGenerationSettings` (Pydantic model) for `Project.generate_speech`
- Add `MotionDeblurSettings` (Pydantic model) for `remove_motion_blur`
- Add `MarkerColor` enum for `analyze_for_slate`

## Fixes
### MediaPoolItem
- Fix `delete_marker_by_color()` to call `DeleteMarkersByColor` (correct MediaPoolItem API name)
- Fix `update_marker_custom_data()` to call `UpdateMarkerCustomData` (was the typo `UpdataMarkerCustomData`); `updata_marker_custom_data()` kept as a deprecated alias
- Fix `get_clip_property()` / `get_metadata()` return type to `str | dict` and make the key optional (returns a dict of all properties when no key is given)

### TimelineItem
- Add `str | dict` return annotation to `get_property()`

### Gallery / GalleryStillAlbum
- Fix `Gallery.get_album_name()` and `GalleryStillAlbum.set_label()` to unwrap the underlying Resolve object before passing it to the API

### MediaPool / MediaStorage
- Fix `MediaPool.delete_clip_mattes()`, `MediaPool.get_clip_matte_list()` and `MediaStorage.add_clip_mattes_to_media_pool()` to unwrap the `MediaPoolItem` before passing it to the API

----
# 2026.1.2
### Project
- `set_render_settings()` - Now supports partial updates. Only fields explicitly provided on the `RenderSetting` object are sent to DaVinci Resolve (via `model_dump(exclude_unset=True)`); any unset field keeps its current value in DR
- `RenderSetting` - **Breaking**: all fields are now optional with no preset defaults (`X | None = None`). Previously every field was required. Construct with only the fields you want to change, e.g. `RenderSetting(FrameRate=24.0)`
  

----
# 2026.1.1
## API
### Timeline
- `add_marker()` - Change `frame_id` parameter type from `str` to `int`
- `add_marker()` - Change `duration` parameter type from `str` to `int` (counted by frames)

### TimelineItem
- `add_marker()` - Change `frame_id` parameter type from `str` to `int`
- `add_marker()` - Change `duration` parameter type from `str` to `int` (counted by frames)

## Docs
- Update samples for `StillManager`

----
# 2026.1.0
## Infrastructure
### Windows Support Fix
- Set PYTHON3HOME environment variable for virtual environments on Windows (e.g., created by uv) to fix compatibility issues with Windows virtual environments

## API Enhancements
### Version Management System
- Introduce comprehensive version checking system for API compatibility with DaVinci Resolve versions
- Add `version_info.py` module with `Version`, `APIStatus`, and `VersionConstraint` classes
- Create `VersionRegistry` in `version_registry.py` to centralize API version constraints
- Add version management decorators (`@require_version`, `@deprecated_in_version`) for automatic compatibility checks
- Update multiple modules (`timeline_item.py`, `gallery.py`, `media_pool.py`, `project.py`, etc.) with version decorators

### Type Safety Improvements
- Create `_resolve_types.py` to define protocols for `BMDModule` and `ResolveObject`
- Add type casting and improved type hints across modules (`_init_bmd.py`, `timeline.py`, `timeline_item.py`)
- Enhanced error handling in timeline retrieval functions with proper exceptions

## Refactoring
### Pydantic Models
- **RenderSetting** (settings.py): Convert from dataclass to Pydantic BaseModel with comprehensive validation
  - Add `Field` with descriptions for all properties (moved from inline comments)
  - Add type constraints using `Literal` for restricted values:
    - `UniqueFilenameStyle`: `Literal[0, 1]` (0 for prefix, 1 for suffix)
    - `AlphaMode`: `Literal[0, 1]` (0 for Premultiplied, 1 for Straight)
    - `SubtitleFormat`: `Literal["BurnIn", "EmbeddedCaptions", "SeparateFile"]`
  - Add numeric validation constraints (ge=0 for MarkIn/MarkOut, gt=0 for dimensions/rates)
  - Add `VideoQuality` type as `int | Literal["Least", "Low", "Medium", "High", "Best"]`
  - Add custom field validators for `VideoQuality` and `MarkOut` validation

- **Item_Info** (media_storage.py): Convert from dataclass to Pydantic BaseModel
  - Add field descriptions and validation for `start_frame` and `end_frame` (ge=0)
  - Update `add_item_list_to_media_pool()` to use `model_dump()` instead of `asdict()`

- **Settings Module Cleanup**:
  - Remove `SettingParameter` legacy class
  - Remove `_get_resolve_object()` and `_get_resolve_constant()` helper functions
  - Simplify imports and directly use `_resolve_object` from `_init_bmd`
  - Convert all settings classes to use Pydantic's `BaseModel` and `Field`
  - Add `BaseIndexSetting` base class with `model_serializer` for index-based serialization

### UI Components
- Update `UI_Dispatcher` to ignore unresolved attribute warnings
- Fix `UI_Manager` initialization to correctly assign `_ui_manager` from `_object`

### Data Handling
- Update `project.py` and `project_manager.py` to use Pydantic's `model_dump()` for data serialization
- Refactor `export_type.py` to remove unnecessary checks and directly use the resolved object

### Toolkits
- Adjust toolkit functions to return empty lists instead of `None` for consistency
- Improve error handling in timeline retrieval functions

----
# 2026.0.1
## API
### TimelineItem
- Modify `get_property()` - Returns the value of the specified property key or all properties if no key is provided
- Add `set_property()` - Sets the value of the specified property key

# 2025.3.3
## Toolkits
### StillManager
- `export_still` now includes still details in the returned dictionary

# 2025.3.2
## Refactoring
- Add WrapperBase class to reduce code duplication in wrapper classes

# 2025.3.1
## Fixes
- Fix typo `gallert_still_album` -> `gallery_still_album` in gallery.py
- Fix typo `ture` -> `true` in docstrings (gallery.py, gallery_still_album.py)
- Fix typo `MeidaPoolItem` -> `MediaPoolItem` in timeline_item.py
- Fix typo `meida` -> `media` in docstrings (timeline_item.py, media_pool.py)
- Fix typo `succssful` -> `successful` in docstrings (project.py, resolve.py)
- Fix typo `delet_marker_at_frame` -> `delete_marker_at_frame` in timeline_item.py
- Fix typo `fram_num` -> `frame_num` in timeline_item.py
- Fix typo `stero_eye` -> `stereo_eye` in media_storage.py
- Fix typo `add_item_list_to_meida_pool` -> `add_item_list_to_media_pool` in media_storage.py
- Fix typo `pen davinci` -> `open davinci` in resolve.py docstring
- Fix typo `Porject` -> `Project` in CHANGELOG.md
- Fix bug in `ProjectManager.import_project()`

----
# 2025.3.0
## API
### Changes for DaVinci Resolve 20.3.0

### Resolve
- Add `get_fairlight_presets()` - Returns a list of Fairlight preset names

### Project
- Add `apply_fairlight_preset_to_current_timeline()` - Applies a Fairlight preset to the current timeline

### ProjectManager
- Update `create_project()` - Now supports optional `media_location_path` parameter

### GalleryStillAlbum
- Add `import_stills()` - Imports stills from file paths into the album

### Timeline
- Add adaptive audio track subtypes `ADAPTIVE_25` through `ADAPTIVE_36` to `OptionalSubTrackType` enum

### Toolkits
- Fix bug in `StillManager.grab_all_still()` method with incorrect timeline timecode handling
- Modify `StillManager.export_still()` to include `clean_still_album` parameter to control album cleanup after export,default is False.

----
# 2025.2.5
## API
### Gallery
- Fix `set_current_still_album()` to unwrap the Resolve album object before passing it to the API

## Toolkits
### StillManager
- Create a dedicated still album named `StillManager_{TimelineName}` when `create_gallery_still_album()` is available (Resolve ≥ 19.1.0)
- Fall back to the previously selected album on older Resolve versions and log failures gracefully
- Add `grab_all_still()` method to grab stills for all clips in the current timeline at a specified position (default: 0.5)
----
# 2025.2.4
## API
### Project
- Fix bug in `delete_color_group` method
----
# 2025.2.3
## API
### MediaPoolItem
- Add `set_name()` - Sets the clip's name to the specified string (DR 20.2.0)

### TimelineItem
- Add `set_name()` - Sets the timeline item's name to the specified string (DR 20.2.0)
- Add `reset_all_node_colors()` - Reset node color for all nodes in the active version (DR 20.2.0) [Note: Currently non-functional due to API issues]

### RenderSettings
- Add `ExportSubtitle` - Enable/disable subtitle export (DR 20.2.0)
- Add `SubtitleFormat` - Set subtitle format: "BurnIn", "EmbeddedCaptions", or "SeparateFile" (DR 20.2.0)

----
# 2025.2.2
## API
### Timeline
- Add `get_voice_isolation_state()` - Returns Voice Isolation State for audio track (DR 20.1.0)
- Add `set_voice_isolation_state()` - Sets Voice Isolation state for audio track (DR 20.1.0)

### TimelineItem
- Add `get_voice_isolation_state()` - Returns Voice Isolation State for timeline item (DR 20.1.0)
- Add `set_voice_isolation_state()` - Sets Voice Isolation state for timeline item (DR 20.1.0)

----
# 2025.2.1
## Documentation
- Fix Sphinx documentation build by properly reading version from pyproject.toml
## Dev
- Convert project manager to uv
## API
### Timeline 
- Fix bug for `Timeline.get_media_pool_item()`

----
# 2025.2.0
## API
### MediaPoolItem
- Add `link_full_resolution_media()` - Links proxy media to full resolution media files (DR 20.0.0)
- Add `replace_clip_preserve_sub_clip()` - Replaces clip while preserving original sub clip extents (DR 20.0.0)
- Add `monitor_growing_file()` - Monitor a file as it keeps growing (DR 20.0.0)


----
# 2025.1.1
## Project
- Add `LoadBurnInPreset`

## Media Pool
- Add `ImportFolderFromFile`

## Folder
- Add `Export`

## Timeline Item
- Add `ApplyArriCdlLut`
- Add `SetClipEnabled`
- Add `GetClipEnabled`
- Add `LoadBurnInPreset`
- Add`GetNodeLabel`
-----
# 2023.3.0
## Bmd
- Add Timeline export option `EXPORT_OTIO` ([OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO))

## Media Pool Item
- Add `transcribe_audio`
- Add `clear_transcription`

## Media Pool
- Modify `Clipinfo` dataclass
  - Add `track_index`
  - Add `record_frame`
- Fix `append_to_timeline`
  
## Media Storage
- Add `Item_Info` dataclass
- Modify `add_item_list_to_media_pool`
  
## Project
- Add `export_current_frame_as_still`

## Timeline Item
- Add `MagicMask_Mode` dataclass
- Add `create_magic_mask`
- Add `regenerate_magic_mask`
- Add `stabilize`
- Add `smart_reframe`

## Timeline
- Add `OptionalSubTrackType` data class
- Add `add_track`
- Add `delete_track`
- Add `set_track_enable`
- Add `get_is_track_enabled`
- Add `set_track_lock`
- Add `get_is_track_locked`
- Add `delete_clips`
- Add `set_clips_linked`
- Add `create_subtitle_from_audio`
- Add `detect_scene_cuts`
----

# 2023.4.0
## Bmd
- Add `ImportRenderPreset`
- Add `ExportRenderPreset`
- Add `ImportBurnInPreset`
- Add `ExportBurnInPreset`

----
# 2023.4.1
## GalleryStillAlbum
- Modify `delete_stills`

---

# 2024.1.1
## ProjectManager
- Add `create_cloud_project`
- Add `import_cloud_project`
- Add `restore_cloud_project`

## MediaPool
- Add `create_stereo_clip`

## Folder
- Add `transcribe_audio`
- Add `clear_transcription`

## Timeline
- Modify `create_subtitle_from_audio`
- Add `convert_timeline_to_stereo`

## MISC
- Add settings module
- Auto start davinci resolve if not running (optional)
----
# 2024.2.1
## toolkits
- Add `StillManager` for grab and export still from timeline markers
------
# 2024.2.2
## toolkits
- Fix some bugs in `StillManager`

--------
# 2024.2.3
## StillManager
- Change default `file_name_format` to `"$file_name$_$clip_frame_count$"` in `export_still`

--------
# 2024.2.4
## StillManager
- Add subfolder export option fpr `export_still`
- Check if exporting to folder failed

--------
# 2024.2.5
## StillManager
- Fix export path bug in `export_still` method when export_base_path is a relative path 

--------
# 2024.2.6
## StillManager
- Fix bug in `2024.2.5` 

--------
# 2024.2.7
## StillManager
- Fix bug in `2024.2.6`

--------
# 2024.3.0
## Refactoring
- Refactor `BMD()` to `Resolve()`
- Move setting/export types const in `BMD()` class to `export_type` and `settings` module
- Add `_init_bmd` module to init fusionscript module from library
- Init `UI_Dispather` class directly from fusionscript module
- change `MediaStorage` init args
- change `ProjectManager` init args
- change `Project` init args
## Changes in DR 19.0.0
### [New] ColorGroup
### [New] Graph
### MediaPollItem
- Add `get_audio_mapping`
### Project
- Add `get_color_groups_list`
- Add `add_color_group`
- Add `delete_color_group`
### Resolve
- Add `get_keyframe_mode`
- Add `set_keyframe_mode`

### settings module
- Add `KeyframeMode` Enum
- Add `CloudSyncState` Enum

### TimelineItem
- Remove `set_lut` to `Graph`
- Remove `get_num_node` to `Graph`
- Remove `get_lut` to `Graph`
- Remove `get_node_label` to `Graph`
- Add `get_node_graph`
- Add `get_color_group`
- Add `assign_to_color_group`
- Add `remove_from_color_group`
- Add `export_LUT`
- Add `get_linked_items`
- Add `get_track_type_and_index`

### Timeline
- Change `add_track`
- Add `get_node_graph`
- Add `analyze_dolby_vision`

------
# 2024.3.1
## Changes in DR 19.0.1
### settings module
- `CloudSyncState` add `CLOUD_SYNC_SUCCESS`

### TimelineItem 
- Add `get_source_audio_channel_mapping`

### Timeline
- Add `get_track_sub_type`

------
# 2024.3.2
## Library
- Add dependency [`multimethod`](https://github.com/coady/multimethod) to overload method
## Changes in DR 19.0.2
### MediaPool
-  `ClipInfo` Change `record_frame` type to `int/float`
-  `ClipInfo` Add `to_dict` method
- Add `get_selected_clips`
- Add `set_selected_clip`
- Typo fixed

### MediaPoolItem
- Add `get_third_party_metadata`
- Add `set_third_party_metadata`(W/ Overloading method)

### TimelineItem

- `get_duration` add `subframe_precision` option
- `get_end` add `subframe_precision` option
- `get_left_offset` add `subframe_precision` option
- `get_right_offset` add `subframe_precision` option
- `get_start` add `subframe_precision` option
- Add `get_source_end_frame`
- Add `get_source_end_time`
- Add `get_source_start_frame`
- Add `get_source_start_time`
- Fix Bug in `add_take`
- Typo fixed

-------
# 2024.3.3
## Library
- Fix bug when load fusioscript library

## API
### settings module
- `RenderSetting` has default value (Test feature)

-------
# 2024.3.4
## Library
- Fix typo in `__repr__` format

------
# 2024.4.0
## API
### ProjectManager 
- Added `load_cloud_project()`

### Project
- Added `delete_render_preset` 
- Added `get_quick_export_render_presets`
- Added `render_with_quick_export`

### MediaPool
- Added `auto_sync_audio` (NOT WORKING)

### MediaPoolItem
- Added `get_mark_in_out`
- Added `set_mark_in_out`
- Added `clear_mark_in_out`


### Timeline 
- Added `get_mark_in_out()` to get timeline marks
- Added `set_mark_in_out()` to set timeline marks
- Added `clear_mark_in_out()` to clear timeline marks
- Moved `apply_grade_from_drx()` to `Graph`

### TimelineItem 
- Added cache control methods:
  - `get_color_output_cache_enabled()`
  - `get_fusion_output_cache_enabled()`
  - `set_color_output_cache()`
  - `set_fusion_output_cache()`
- Moved `apply_arri_cdl_lut()` to `Graph`

### Gallery 
- Added `get_gallery_power_grade_albums()` to get PowerGrade albums
- Added `create_gallery_still_album()` to create new still album
- Added `create_gallery_power_grade_album()` to create new PowerGrade album

### Graph 
- Added node cache control:
  - `set_node_cache_mode()`
  - `get_node_cache_mode()`
- Added grade management:
  - `apply_grade_from_drx()`
  - `apply_arri_cdl_lut()`
  - `reset_all_grades()`

# 2024.4.1
## API
### StillManager
- Fix bug in timeline framerate detection

# 2025.1.0
## API
### StillManager
- Refactor StillManager to support all metadata from davinci resolve GUI

# 2025.1.1
## API
### StillManager
- Still manager support maker info as wildcard in file name format(`marker_note` and `marker_name`)
### MediaPool
- Fix bug for `export_metadata` method when clip is none
