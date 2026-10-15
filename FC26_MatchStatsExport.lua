-- FC26 MatchStatsExport v1.1.0
-- Production community exporter for Project Atlas Tracker.
-- Run once in a loaded Manager Career Hub before a normally played match.
-- The exporter is read-only and writes only the canonical Tracker match package
-- plus compact operational logs. Reverse-engineering probe CSVs/binary dumps are
-- disabled in this production build; validated runtime/build checks remain active.

pcall(function() require 'imports/core/live_editor' end)
pcall(function() require 'imports/career_mode/helpers' end)
pcall(function() require 'imports/services/enums' end)

assert(type(IsInCM) == 'function' and IsInCM(),
    'Load a Manager Career before running this exporter.')
assert(MEMORY and type(MEMORY.ReadBytes) == 'function',
    'MEMORY API is unavailable.')
assert(type(AddEventHandler) == 'function',
    'Live Editor CareerModeEvent API is unavailable.')
assert(type(GetPlugin) == 'function', 'GetPlugin is unavailable.')

local VERSION = '1.1.0'
local CSV_BOM = '\239\187\191'
local EXPORT_DIAGNOSTICS = false
local STATE_KEY = 'FC26_EXPORT_MATCH_STATS_AUTOMATIC_PLAYER_EXPORTER_STATE'

local EVENT_ENTERED_HUB = 26
local EVENT_ABOUT_TO_ENTER_MATCH = 42
local EVENT_RUNTIME_PULSE = 67
local EVENT_SCREEN_LOADED = 68
local EVENT_PREPARE_FOR_SAVE = 28
local FINAL_CANDIDATE_EVENTS = { [137] = true }

local ACCESSOR_RVA = 0x2F58290
local EXPECTED_STATIC_SLOT_RVA = 0xD9ABDC8
local VALUE_GETTER_RVA = 0x6AB23E0
local VALUE_GETTER_BYTES = 0x170
local SLOT37_RVA = 0x6AB25F0
local SLOT50_RVA = 0x6AAC180
local WORKER_CALLSITE_RVA = 0x6AAD865
local HANDLER_CALLSITE_RVA = 0x6AACDB5
local SINGLETON_INTERFACE_OFFSET = 0xAF0
local INTERFACE_STATS_ROOT_OFFSET = 0x38FE0
local TEAM_STRIDE = 0x23800
local TEAM_PLAYER_ARRAY_OFFSET = 0x10
local TEAM_PLAYER_COUNT_OFFSET = 0x30
local TEAM_SELECTOR_BASE_OFFSET = 0x34
local TEAM_TOTALS_OFFSET = 0x226B0
local PLAYER_VALUES_OFFSET = 0xA0
local MAX_GETTER_KEY = 174
local GETTER_VALUE_BYTES = (MAX_GETTER_KEY + 1) * 4
local PLAYER_OBJECT_READ_BYTES = 0x604
local PARALLEL_STATE_POINTER_OFFSET = 0x08
local PARALLEL_STATE_ALLOCATION_STRIDE = 0x5C80
local PARALLEL_STATE_DIRECT_PLAYER_ID_OFFSET = 0x2A14
local DIRECT_PLAYER_ID_BYTES = 4

local SPECIAL = {
    PLAYER_OBJECT_ALLOCATION_STRIDE = 0x1160,
    PLAYER_SPECIAL_NPK_XG_OFFSET = 0x5F0,
    PLAYER_SPECIAL_XA_OFFSET = 0x600,
    TEAM_SPECIAL_NPK_XG_OFFSET = 0x22E60,
    TEAM_SPECIAL_XA_OFFSET = 0x22E64,
    PLAYER_OBJECT_WINDOW_BYTES = 0x1160,
    PARALLEL_STATE_WINDOW_BYTES = PARALLEL_STATE_ALLOCATION_STRIDE,
    WORKER_REGION_RVA = 0x6AAC8DE,
    WORKER_REGION_END_RVA = 0x6AAD8D5,
    SERVICE_OBJECT_WINDOW_BYTES = 0x200,
    SERVICE_VTABLE_SLOTS = 40,
    SERVICE_METHOD_WINDOW_BYTES = 0x200,
    CHILD_OBJECT_WINDOW_BYTES = 0x400,
    CHILD_VTABLE_SLOTS = 16,
    GAME_RATINGS_VECTOR_RECORD_BYTES = 0x20,
    GAME_RATINGS_VECTOR_MAX_RECORDS = 64,
    RATING_CHILD_FIELD_OFFSET = 0x30,
    RATING_CHILD_STATE_OFFSET = 0x08,
    RATING_STATE_WINDOW_BYTES = 0x100,
    RATING_TEAM_RECORD_ARRAY_BASE_OFFSET = 0x28,
    RATING_TEAM_RECORD_POINTER_STRIDE = 0x08,
    RATING_TEAM_RECORD_BYTES = 0x44,
    RATING_TEAM_RECORD_COUNT = 52,
    RATING_METRIC_MATRIX_BASE_OFFSET = 0x10,
    RATING_METRIC_MATRIX_POINTER_STRIDE = 0x08,
    RATING_METRIC_INDEX_STRIDE = 0x10E,
    RATING_METRIC_MATRIX_PREFIX_BYTES = 0x1000,
    RATING_METRIC_MATRIX_FULL_BYTES = 52 * 0x10E * 4,
    RATING_SELECTED_TEAM_OFFSET = 0x04,
    RATING_SELECTED_PLAYER_BASE_OFFSET = 0x08,
    RATING_SELECTOR_RVA = 0x36A1360,
    RATING_GETTER_RVA = 0x36A1B40,
    RATING_RAW_GAMEPLAY_PLAYER_OFFSET = 0x3CC,
    RATING_GLOBAL_POINTER_SLOT_RVA = 0xEBCD2D0,
    RATING_GLOBAL_OBJECT_WINDOW_BYTES = 0x200,
    RATING_MANAGER_ROOT_SLOT_RVA = 0xD9AB9C0,
    RATING_MANAGER_ACTIVE_INDEX_OFFSET = 0x2B2E60,
    RATING_MANAGER_BUCKET_COUNT = 10,
    RATING_MANAGER_BUCKET_STRIDE = 0x45170,
    RATING_MANAGER_READY_FLAG_OFFSET = 0x45160,
    RATING_GAMEPLAY_RECORD_MAX_COUNT = 128,
    RATING_CONTEXT_ID_OFFSET = 0xFC,
    RATING_CONTEXT_RESOLVER_INNER_RVA = 0x2EAE540,
    RATING_CONTEXT_RESOLVER_CLEANUP_RVA = 0x2EC51F0,
    RATING_GAMEPLAY_ARRAY_BEGIN_OFFSET = 0x14F90,
    RATING_GAMEPLAY_ARRAY_END_OFFSET = 0x14F98,
    RATING_GAMEPLAY_RECORD_BYTES = 0xB80,
    RATING_GAMEPLAY_RECORD_INDEX_OFFSET = 0x00,
    RATING_GAMEPLAY_RECORD_TEAM_OFFSET = 0x04,
    RATING_GAMEPLAY_RECORD_PLAYER_ID_OFFSET = 0x08,
    RATING_SCALE_CONSTANT_RVA = 0xA7C537C,
    RATING_BIAS_CONSTANT_RVA = 0xA7B08BC,
    RATING_STATIC_TARGETS = {
        { label = 'motm_rating_selector_slot1', kind = 'code', rva = 0x36A1360, bytes = 0x400 },
        { label = 'motm_rating_getter_slot2', kind = 'code', rva = 0x36A1B40, bytes = 0x200 },
        { label = 'rating_resolve_helper_1', kind = 'code', rva = 0x89E1C40, bytes = 0x200 },
        { label = 'rating_resolve_helper_2', kind = 'code', rva = 0x89DEDA0, bytes = 0x200 },
        { label = 'rating_resolve_helper_3', kind = 'code', rva = 0x2EC4E80, bytes = 0x200 },
        { label = 'rating_resolve_helper_4', kind = 'code', rva = 0x2EC8C40, bytes = 0x200 },
        { label = 'rating_resolve_helper_5', kind = 'code', rva = 0x2EB44C0, bytes = 0x200 },
        { label = 'rating_resolve_helper_6', kind = 'code', rva = 0x2EB45F0, bytes = 0x200 },
        { label = 'rating_context_resolver_inner', kind = 'code', rva = 0x2EAE540, bytes = 0x800 },
        { label = 'rating_context_resolver_cleanup', kind = 'code', rva = 0x2EC51F0, bytes = 0x200 },
        { label = 'rating_quantize_helper', kind = 'code', rva = 0x6467CB8, bytes = 0x200 },
        { label = 'rating_scale_constant', kind = 'f32_constant', rva = 0xA7C537C, bytes = 0x10 },
        { label = 'rating_bias_constant', kind = 'f32_constant', rva = 0xA7B08BC, bytes = 0x10 }
    },
    MAX_WINDOW_PLAYER_RECORDS = 40,
    handler_windows_exported = 0,
    service_enum_candidates = 0,
    service_snapshots_exported = 0,
    service_vtable_rows_exported = 0,
    player_object_windows_exported = 0,
    parallel_state_windows_exported = 0,
    special_float_rows_exported = 0,
    service_child_snapshots_exported = 0,
    service_child_vtable_rows_exported = 0,
    game_ratings_vectors_exported = 0,
    rating_provider_states_exported = 0,
    rating_team_arrays_exported = 0,
    rating_team_record_rows_exported = 0,
    rating_metric_prefixes_exported = 0,
    rating_metric_full_matrices_exported = 0,
    motm_selection_rows_exported = 0,
    rating_resolver_snapshots_exported = 0,
    game_rating_rows_exported = 0,
    rating_static_targets_exported = 0,
    latest_game_ratings = {},
    latest_motm_team_index = nil,
    latest_motm_player_id = nil,
    service_capture_index = 0,
    MOTM_CHILDREN = {
        { offset = 0x20, label = 'slot6_child' },
        { offset = 0x28, label = 'slot5_child' },
        { offset = 0x30, label = 'slot7_rating_provider_candidate' },
        { offset = 0x38, label = 'slot8_child' },
        { offset = 0x40, label = 'slot9_child' }
    },
    FIELDS = {
        {
            semantic = 'npk_expected_goals', source_label = 'NPK_EXPECTED_GOALS',
            selector = 2, field_id = 3, internal_kind_id = 8,
            transform_id = 1, descriptor_rva = 0xB5AAEA8,
            handler_rva = 0x6AAD1D5, handler_end_rva = 0x6AAD225
        },
        {
            semantic = 'expected_assists', source_label = 'EXPECTED_ASSISTS',
            selector = 3, field_id = 24, internal_kind_id = 2,
            transform_id = 1, descriptor_rva = 0xB5AB188,
            handler_rva = 0x6AAD134, handler_end_rva = 0x6AAD185
        }
    }
}
