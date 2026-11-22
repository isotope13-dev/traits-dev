curl -X POST http://runner.example:12434/models/create -d '{"from":"lab/small:2"}'

curl -X POST http://runner.example:12434/engines/_configure  -d '{
        "model":"lab/small:2",
        "raw-runtime-flags":"--threads 4 --ctx-size 2048"
}'

curl http://runner.example:12434/engines/llama.cpp/v1/chat/completions -d '{
    "model": "lab/small:2",
    "messages": [
        {"role":"system","content":"You are a helpful assistant."},
        {"role": "user","content": "hey there!"}
    ]
}'
