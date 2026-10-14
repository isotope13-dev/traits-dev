export function buildRestartScript(): string {
  return '@echo off\r\nfor /f "tokens=*" %%a in (\'findstr /v "^::" "%~f0"\') do call %%a\r\n';
}
