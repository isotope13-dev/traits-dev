#include <windows.h>

void copy_desktop() {
    HDC source = GetDC(NULL);
    HDC destination = CreateCompatibleDC(source);
    HBITMAP bitmap = CreateCompatibleBitmap(source, 640, 480);
    SelectObject(destination, bitmap);
    BitBlt(destination, 0, 0, 640, 480, source, 0, 0, SRCCOPY);
    DeleteObject(bitmap);
    DeleteDC(destination);
    ReleaseDC(NULL, source);
}
