# Change Log for PyBMD
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
- Modify `add_item_list_to_meida_pool`
  
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

### Porject
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
