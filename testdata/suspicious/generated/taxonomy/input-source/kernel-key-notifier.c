#include<linux/keyboard.h>
void observe(unsigned long kcode, struct keyboard_notifier_param *event) {
    if (kcode == KBD_KEYCODE) notify_accessibility(event->value);
}
void begin(void) { register_keyboard_notifier(&notifier); }
void end(void) { unregister_keyboard_notifier(&notifier); }
