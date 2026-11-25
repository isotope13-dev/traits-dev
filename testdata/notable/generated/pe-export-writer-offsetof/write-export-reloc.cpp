#include "ceefilegenwriter.h"

HRESULT AddExportNameReloc(HCEESECTION sec, unsigned deDataOffset, unsigned deOffset) {
    IMAGE_EXPORT_DIRECTORY exportDirIDD;
    HRESULT hr;
    if (FAILED(hr = m_pCeeFileGen->AddSectionReloc(sec, deOffset + offsetof(IMAGE_EXPORT_DIRECTORY,AddressOfNames), sec, srRelocAbsolute))) return hr;
    exportDirIDD.AddressOfNameOrdinals = VAL32(VAL32(exportDirIDD.AddressOfNameOrdinals) + deDataOffset);
    return S_OK;
}
