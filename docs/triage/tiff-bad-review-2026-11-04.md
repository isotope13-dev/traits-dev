# TIFF filetype mislabeled-bad review — 2026-11-04

The 40-file snapshot contains 39 good images and 1 bad malformed image.

`b1ce3d8c5aa8` is a TIFF image with a one-row image, a DotRange field containing 204 values where the TIFF reader expects two, and an embedded network URL. The malformed field and the payload context are hostile; no successful exploitation or network request is asserted. Both scanners match the new structured TIFF finding, and changing the DotRange count to two clears the control. Atomscan reports the hostile trait but exits successfully. Full validation passed.

The following 39 standalone TIFF resources are good. Each was decoded with `tiffinfo -D` without warnings, and neither scanner reported a hostile trait; cleave reported no suspicious traits. Their parent application labels do not establish malicious behavior in the images.

- `92b794d42cd9`: ComboBox_Selected_Mac.tiff.
- `2d31af441f2a`: ComboBox_Mac.tiff.
- `df4314a54349`: add_dis.tiff.
- `0c2445b99d4e`: add.tiff.
- `c85f3a061e8c`: ComboBox_iPad.tiff.
- `ea6661178409`: ComboBox_iPod.tiff.
- `d5be132a5201`: feedback_on_normal.tiff.
- `313f8a2d5d85`: ComboBox_AppleTV.tiff.
- `3cc5d3b6be61`: mainFuncIcon_8.tiff.
- `3e10f2fe0ddb`: rd_free.tiff.
- `0d31e2e8aa16`: mainFuncIcon_3.tiff.
- `3f6565d9ae53`: rd_free.tiff.
- `1b67219cf90d`: rd_free.tiff.
- `7e52e382b1d6`: rd_free.tiff.
- `859ab084bcd3`: rd_free.tiff.
- `597128a35719`: rd_free.tiff.
- `ca308f3a1b9a`: iOS17_Beta_1.tiff.
- `366a59362cfc`: iOS17_Beta_2.tiff.
- `9cdcd8a2bd09`: iOS27_Beta_2.tiff.
- `44697cb7c3cc`: backgroundImage.tiff.
- `d00b99b2e786`: iOS29_Beta_2.tiff.
- `e4f9b6e222de`: iOS17_1.tiff.
- `c1e430425040`: iOS27_1.tiff.
- `f23bce7d5844`: iOS18_1.tiff.
- `c679952df39f`: MacBookPro_3_step_1.tiff.
- `a63d1f4e6add`: MacBookPro_step_2.tiff.
- `ae06310942f6`: MacMini_step3_2.tiff.
- `b0c5d7124def`: reset_quick_step_02.tiff.
- `04b56f6f2fce`: iMac_3_step_2.tiff.
- `325fc20f77a9`: T2_guide_after_repair_step_3.tiff.
- `9d6b9749cd56`: reset_quick_step_02.tiff.
- `9903ded63bb1`: reset_quick_step_02.tiff.
- `e71ee194b0cc`: reset_quick_step_02.tiff.
- `032816215b14`: priceImg.tiff.
- `5529b5aea31b`: reset_quick_step_01.tiff.
- `5251043cfd03`: reset_quick_step_03.tiff.
- `1bc1af41525d`: reset_quick_step_01.tiff.
- `11f5455e3dba`: reset_quick_step_03.tiff.
- `16cdba44f7d9`: dmgcanvas_bg.tiff.
