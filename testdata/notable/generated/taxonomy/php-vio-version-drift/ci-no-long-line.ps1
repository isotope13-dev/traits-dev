$dll = Get-ChildItem -Recurse -Filter php_vio.dll | Select-Object -First 1
if (-not $dll) { throw "php_vio.dll not found after build" }
$dllDir = $dll.Directory.FullName
$vkBin = if ($env:VULKAN_SDK) { "$env:VULKAN_SDK\Bin" } else { "" }
$env:PATH = "$PWD\deps\bin;$PWD\deps\lib;$vkBin;$env:PATH"
# Smoke: the extension loads with the full runtime DLL chain present.
php -n -d extension_dir="$dllDir" -d extension=php_vio.dll -r 'exit((int)!extension_loaded("vio"));'
if ($LASTEXITCODE -ne 0) { throw "vio failed to load (runtime DLL chain incomplete)" }
# Shader Model 6: DXC (dxcompiler.dll + dxil.dll) from the newest Windows
# SDK. VIO_REQUIRE_SM6 makes 119 / 144 / 149 fail instead of silently
# falling back to FXC, so a green run proves the DXIL path ran.
$dxc = Get-ChildItem "${env:ProgramFiles(x86)}\Windows Kits\10\bin\10.*\x64\dxcompiler.dll" -ErrorAction SilentlyContinue |
  Where-Object { Test-Path (Join-Path $_.DirectoryName 'dxil.dll') } |
  Sort-Object { [version]$_.Directory.Parent.Name } | Select-Object -Last 1
if (-not $dxc) { throw "Windows SDK DXC (dxcompiler.dll + dxil.dll) not found" }
$env:VIO_DXC_DIR = $dxc.DirectoryName
$env:VIO_REQUIRE_SM6 = "1"
# WARP offers SV_Barycentrics with SM 6.1+ (measured: SM 6.2, BarycentricsSupported).
$env:VIO_REQUIRE_BARYCENTRICS = "d3d12"
# Native 16-bit shader ops on WARP (measured: float16=1 at SM 6.2).
$env:VIO_REQUIRE_SHADER_FLOAT16 = "d3d12"
# View instancing on WARP (measured: multiview=1 at SM 6.2, test 158 passes).
$env:VIO_REQUIRE_MULTIVIEW = "d3d12"
# Bindless table: WARP is Resource Binding Tier 3 (unbounded SRV tables, FXC 5.1).
$env:VIO_REQUIRE_BINDLESS = "d3d12"
Write-Host "VIO_DXC_DIR=$env:VIO_DXC_DIR"
# Which shader-model features WARP offers (tests skip what it lacks).
# Agility SDK (diagnostic only, not required): the latest Microsoft.Direct3D.D3D12 NuGet
# package, device from its factory - what it reports on the runner.
try {
  $ag = Join-Path $env:RUNNER_TEMP "agility"
  Invoke-WebRequest -Uri "https://www.nuget.org/api/v2/package/Microsoft.Direct3D.D3D12" -OutFile "$ag.zip"
  Expand-Archive -Path "$ag.zip" -DestinationPath $ag -Force
  $env:VIO_AGILITY_DIAG = Join-Path $ag "build\native\bin\x64"
  php -n -d extension_dir="$dllDir" -d extension=php_vio.dll -r '$c = vio_create("d3d12", ["width" => 8, "height" => 8, "headless" => true, "shader_model" => 6, "dxc_dir" => getenv("VIO_DXC_DIR"), "agility_sdk" => getenv("VIO_AGILITY_DIAG")]); $i = vio_swapchain_info($c); printf("D3D12 Agility agility_sdk=%d SM %d work_graphs=%d mesh_shader=%d\n", $i["agility_sdk"], $i["shader_model_version"], vio_supports_feature($c, VIO_FEATURE_WORK_GRAPHS), vio_supports_feature($c, VIO_FEATURE_MESH_SHADER));'
} catch { Write-Host "Agility SDK diagnostic skipped: $_" }
$env:NO_INTERACTION = "1"
$env:REPORT_EXIT_STATUS = "1"
$env:TEST_PHP_ARGS = "-n -d extension_dir=$dllDir -d extension=php_vio.dll"
php -n run-tests.php -q --show-diff `
  tests/render3d/086_vertex_storage.phpt `
  tests/render3d/087_vertex_storage_render.phpt `
  tests/render3d/088_vertex_storage_render_native.phpt `
  tests/render3d/090_cubemap_render_target.phpt `
  tests/render3d/091_pipeline_state.phpt `
  tests/render3d/092_render_target_readback.phpt `
  tests/render3d/093_texture_update_and_pipeline_free.phpt `
  tests/backends/094_uniform_struct_array_layout.phpt `
  tests/backends/095_texture_bind_order.phpt `
  tests/render3d/096_storage_image.phpt `
  tests/render3d/097_mrt.phpt `
  tests/render3d/098_async_compute.phpt `
  tests/core/074_backend_capability_matrix.phpt `
  tests/core/099_audit_gate_backend_branches.phpt `
  tests/core/100_auto_backend_prefers_3d.phpt `
  tests/render3d/101_sampler_filter_wrap.phpt `
  tests/render3d/102_cube_rt_mipmaps_readback_all_backends.phpt `
  tests/render3d/103_midframe_texture_upload_ordering.phpt `
  tests/render3d/104_anisotropy_option.phpt `
  tests/render3d/105_render_target_msaa_resolve.phpt `
  tests/backends/106_vulkan_present_mode.phpt `
  tests/backends/107_opengl_context_generation.phpt `
  tests/backends/108_opengl_spirv_uniform_names.phpt `
  tests/render3d/109_geometry_shader_all_backends.phpt `
  tests/render3d/110_tessellation_all_backends.phpt `
  tests/render3d/111_pending_texture_lifetime_all_backends.phpt `
  tests/render3d/112_per_attachment_blend_all_backends.phpt `
  tests/render3d/113_stencil_test_all_backends.phpt `
  tests/render3d/114_uint16_indices_all_backends.phpt `
  tests/core/115_gpu_frame_time_all_backends.phpt `
  tests/core/116_shader_cache_all_backends.phpt `
  tests/core/117_frame_latency_all_backends.phpt `
  tests/core/118_hdr_output_d3d.phpt `
  tests/core/119_shader_model_6_d3d12.phpt `
  tests/render3d/120_indirect_draw_all_backends.phpt `
  tests/render3d/121_texture_array_bc_ktx2_all_backends.phpt `
  tests/render3d/122_shading_rate_d3d12.phpt `
  tests/render3d/123_vulkan_3d_conventions_all_backends.phpt `
  tests/render3d/124_mrt_formats_texture_mips_all_backends.phpt `
  tests/render3d/125_compute_buffer_writable_rebind_update_all_backends.phpt `
  tests/render3d/126_compute_async_params_snapshot_all_backends.phpt `
  tests/render2d/127_text_bitmap_font_face.phpt `
  tests/input/131_inject_event_path.phpt `
  tests/input/132_virtual_gamepad.phpt `
  tests/input/133_input_record_replay.phpt `
  tests/input/134_replay_drops_os_input_win32.phpt `
  tests/render3d/135_geometry_tessellation_draw_paths_all_backends.phpt `
  tests/render3d/136_layered_render_targets_all_backends.phpt `
  tests/render3d/137_layered_rendering_all_backends.phpt `
  tests/render3d/138_multi_viewport_all_backends.phpt `
  tests/render3d/139_gs_instancing_adjacency_all_backends.phpt `
  tests/render3d/140_hlsl_stage_override_all_backends.phpt `
  tests/render3d/141_shadow_comparison_samplers_all_backends.phpt `
  tests/render3d/142_render_target_rebind_keeps_content_all_backends.phpt `
  tests/render3d/143_gs_gl_in_position_all_backends.phpt `
  tests/render3d/144_tessellation_gl_conventions_all_backends.phpt `
  tests/render3d/145_cube_mipmaps_in_frame_all_backends.phpt `
  tests/render3d/146_uniform_array_elements_all_backends.phpt `
  tests/render3d/147_stencil_layered_depth_only_all_backends.phpt `
  tests/render3d/148_tessellation_point_mode_isolines_all_backends.phpt `
  tests/render3d/149_subgroup_ops_all_backends.phpt `
  tests/render3d/152_subgroup_quad_all_backends.phpt `
  tests/render3d/153_barycentrics_all_backends.phpt `
  tests/render3d/154_atomic64_all_backends.phpt `
  tests/render3d/155_shader_float16_all_backends.phpt `
  tests/render3d/156_base_vertex_instance_all_backends.phpt `
  tests/render3d/157_compute_derivatives_all_backends.phpt `
  tests/render3d/158_multiview_all_backends.phpt `
  tests/render3d/159_primitive_shading_rate_all_backends.phpt `
  tests/render3d/160_shading_rate_image_all_backends.phpt `
  tests/render3d/161_bindless_all_backends.phpt `
  tests/render3d/163_ray_query_all_backends.phpt `
  tests/render3d/162_mesh_shaders_all_backends.phpt `
  tests/render3d/165_sampler_feedback_d3d12.phpt `
  tests/render3d/167_cooperative_matrix_all_backends.phpt `
  tests/render3d/164_raytracing_pipeline_all_backends.phpt `
  tests/render3d/166_work_graphs_d3d12.phpt `
  tests/render3d/169_submit_batch_parity_all_backends.phpt `
  tests/core/171_feature_info_native_emulated.phpt `
  tests/core/172_gpu_named_timestamps_all_backends.phpt `
  tests/render3d/173_pipeline_survives_frame_all_backends.phpt `
  tests/render3d/174_mesh_layout_input_layout_all_backends.phpt `
  tests/render3d/175_uniform_buffer_graphics_all_backends.phpt `
  tests/render3d/176_bindless_release_all_backends.phpt `
  tests/render3d/177_bindless_samplers_all_backends.phpt `
  tests/render3d/178_bindless_cubes_arrays_all_backends.phpt `
  tests/render3d/179_bindless_compute_all_backends.phpt `
  tests/render3d/180_separate_texture_sampler_all_backends.phpt `
  tests/render3d/181_base_vertex_below_sm68.phpt `
  tests/render3d/182_multiview_instancing_emulation.phpt `
  tests/render3d/183_multiview_geometry_tessellation.phpt `
  tests/core/184_backend_info_all_backends.phpt `
  tests/core/185_adapters.phpt `
  tests/core/186_backend_scoring.phpt `
  tests/core/187_backend_benchmark.phpt `
  tests/render3d/188_readback_latest_frame_all_backends.phpt `
  tests/render2d/189_glyph_atlas_lazy_all_backends.phpt `
  tests/render3d/190_ktx2_cubemap_3d_all_backends.phpt `
  tests/render3d/191_astc_textures_all_backends.phpt `
  tests/render2d/192_vertical_text.phpt `
  tests/render3d/193_depth_mipmaps_all_backends.phpt `
  tests/render3d/194_msaa_mrt_all_backends.phpt `
  tests/render3d/195_msaa_cube_array_all_backends.phpt `
  tests/render3d/196_msaa_depth_only_all_backends.phpt `
  tests/render3d/197_mesh_task_textures_all_backends.phpt `
  tests/render3d/198_tess_varyings_all_backends.phpt `
  tests/render3d/199_acceleration_structure_update_all_backends.phpt `
  tests/render3d/200_rt_pipeline_groups_records_all_backends.phpt `
  tests/render3d/201_rt_pipeline_textures_all_backends.phpt `
  tests/render3d/202_trace_rays_in_frame_all_backends.phpt `
  tests/render3d/203_fragment_storage_all_backends.phpt `
  tests/render3d/204_sampler_feedback_emulated_all_backends.phpt `
  tests/render3d/205_geometry_stage_gaps_all_backends.phpt `
  tests/backends/206_pass_switches_vulkan_core_all_backends.phpt `
  tests/render3d/207_bundle_all_backends.phpt `
  tests/render3d/208_upscale_all_backends.phpt `
  tests/media/209_recorder_encoders_all_backends.phpt `
  tests/render3d/210_compute_msl_override_all_backends.phpt `
  tests/render3d/211_rate_map_all_backends.phpt `
  tests/core/212_audit_gate_no_glfw_outside_platform.phpt `
  tests/window/213_win32_platform.phpt `
  tests/core/170_d3d12_shader_model_pin.phpt `
  tests/backends/168_d3d12_pipeline_freed_after_frame.phpt `
  tests/backends/221_d3d12_capture_mid_frame_keeps_list_state.phpt `
  tests/render3d/222_mrt_6_attachments_all_backends.phpt `
  tests/render3d/223_rt_depth_sample_all_backends.phpt `
  tests/render3d/224_rt_raw_readback_all_backends.phpt `
  tests/render3d/225_rt_storage_compute_all_backends.phpt `
  tests/render3d/226_upscaler_unavailable_all_backends.phpt `
  tests/render3d/227_upscaler_fsr3_converges.phpt `
  tests/render3d/228_upscaler_lifecycle_no_leak.phpt `
  tests/render3d/229_upscaler_dlss_unavailable_all_backends.phpt `
  tests/render3d/232_vulkan_stale_texture_binding_validation_clean.phpt `
  tests/render3d/234_upscaler_plugin_missing_all_backends.phpt `
  tests/render3d/235_upscaler_plugin_abi_refused.phpt `
  tests/render3d/236_upscaler_plugin_dispatch_states.phpt `
  tests/render3d/237_compute_many_dispatches_per_frame_all_backends.phpt `
  tests/render3d/238_generate_mipmaps_many_per_frame_all_backends.phpt `
  tests/media/241_audio_decode_opus_vorbis.phpt `
  tests/media/242_audio_encode_opus_vorbis.phpt `
  tests/media/243_audio_load_opus_vorbis.phpt `
  tests/media/244_audio_init_backends.phpt `
  tests/media/245_audio_phar_opus_vorbis.phpt
