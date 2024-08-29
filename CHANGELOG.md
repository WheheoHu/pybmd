# Change Log for PyBMD
----
# 2023.2.0
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