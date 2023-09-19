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
- modify `delete_stills`

---