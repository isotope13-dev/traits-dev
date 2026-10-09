IWbemServices *services;
const wchar_t *query = L"SELECT * FROM Win32_ShadowCopy";
services->DeleteInstance(path, 0, 0, 0);
