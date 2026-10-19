// FUN_10009e188 @ 10009e188

void FUN_10009e188(int *param_1,undefined8 param_2,undefined8 param_3,int param_4,int param_5,
                  undefined8 param_6,uint param_7)

{
  uint local_28;
  uint local_24;
  
  local_24 = 0x88cc487e;
  local_28 = 0xe928abcd;
LAB_10009e22c:
LAB_10009e230:
  do {
    if ((int)local_24 < -0x3cc40dca) {
      if (local_24 == 0x88cc487e) {
        local_24 = 0x5689706a;
      }
      else {
        if (local_24 != 0xb8745e72) {
          return;
        }
        local_24 = 0xf918cd6a;
      }
    }
    else {
      if (0x4821d262 < (int)local_24) break;
      if (local_24 != 0xc33bf236) {
        return;
      }
      param_1[3] = param_5 * param_4 ^ param_7;
      local_24 = 0x63920773;
    }
    local_28 = local_28 * 0x19660d + 0x3c6ef35f;
    local_24 = local_28 ^ local_24;
  } while( true );
  if (local_24 == 0x4821d263) {
    param_5 = param_1[1];
    local_28 = local_28 * 0x19660d + 0x3c6ef35f;
    local_24 = local_28 ^ 0x56dbc782;
    goto LAB_10009e22c;
  }
  if (local_24 == 0x58712aa2) goto LAB_10009e210;
  if (local_24 != 0x6b7830b8) {
    return;
  }
  param_7 = param_1[2];
  local_28 = local_28 * 0x19660d + 0x3c6ef35f;
  local_24 = local_28 ^ 0x15d66f67;
  goto LAB_10009e230;
LAB_10009e210:
  param_4 = *param_1;
  local_28 = local_28 * 0x19660d + 0x3c6ef35f;
  local_24 = local_28 ^ 0x989eede4;
  goto LAB_10009e22c;
}

