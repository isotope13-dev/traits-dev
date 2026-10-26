@echo off
set PORT=13305
curl -s -X POST "https://model.example:%PORT%/api/v1/load" ^
  -H "Content-Type: application/json" ^
  -d "{\"model_name\": \"Example\"}" ^
  --max-time 120
