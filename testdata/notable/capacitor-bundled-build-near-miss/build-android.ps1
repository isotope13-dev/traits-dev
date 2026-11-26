$Project = Join-Path $Root 'android-apk-project'
@"
{
  "appId": "com.example.app",
  "appName": "Example App",
  "webDir": "www",
  "bundledWebRuntime": true
}
"@ | Set-Content -Encoding UTF8 (Join-Path $Project 'capacitor.config.json')
