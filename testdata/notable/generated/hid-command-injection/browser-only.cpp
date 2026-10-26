#include "DigiKeyboard.h"

void setup() {
  DigiKeyboard.sendKeyStroke(0);
  DigiKeyboard.delay(500);

  // Execute the run prompt - Win+R
  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT);
  DigiKeyboard.delay(500);

  // Open a benign website
  DigiKeyboard.print("msedge nviso.eu");
  DigiKeyboard.sendKeyStroke(KEY_ENTER);

}
void loop() {}
