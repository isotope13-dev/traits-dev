$AppUrl = 'https://app.example-cmdline.test/mobile.html'
$Project = Join-Path $Root 'android-apk-project'
@"
{
  "appId": "com.example.shell",
  "appName": "Example Shell",
  "webDir": "www",
  "bundledWebRuntime": false,
  "server": {
    "url": "$AppUrl",
    "cleartext": false,
    "allowNavigation": ["app.example-cmdline.test"]
  }
}
"@ | Set-Content -Encoding UTF8 (Join-Path $Project 'capacitor.config.json')
