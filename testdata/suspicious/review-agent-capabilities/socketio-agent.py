import socketio
import sys
import os
import time
import asyncio
import uuid

# Configuration
TARGET_URL = sys.argv[1] if len(sys.argv) > 1 else os.getenv("SERVER_URL", "https://app.cyberrant.org")
AGENT_ID = f"lea-{uuid.uuid4().hex[:8]}"
SANDBOX_DIR = "agent_sandbox"

# Create sandbox if it doesn't exist
os.makedirs(SANDBOX_DIR, exist_ok=True)

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print(f"[+] Local Execution Agent ({AGENT_ID}) connected to {TARGET_URL}")
    lea_secret = os.getenv("LEA_SECRET", "")
    await sio.emit("register_lea", {"agent_id": AGENT_ID, "secret": lea_secret})
    
    # Start heartbeat
    asyncio.create_task(heartbeat())

@sio.event
async def disconnect():
    print(f"[!] Disconnected from {TARGET_URL}")

@sio.on("execute_command")
async def on_execute_command(data):
    trace_id = data.get("trace_id")
    command = data.get("command")
    args = data.get("args", [])
    
    print(f"\n[*] Received execution request for trace: {trace_id}")
    print(f"[*] Command: {command} {' '.join(args)}")
    
    # Send acknowledgment
    await sio.emit("execution_log", {
        "trace_id": trace_id, 
        "log": {
            "message": f"Received command '{command}'.",
            "level": "INFO",
            "timestamp": time.time()
        }
    })
    
    try:
        # IMPORT NATIVE CLI TASK EXECUTOR!
        from cli.task_executor import TaskExecutor
        executor = TaskExecutor()
        
        # Build the exact task object the CLI expects
        # For our unified engine, if command matches a builtin, we flag it as builtin
        task_type = "shell"
        if command in ["http_get", "http_post", "file_read", "file_write", "builtin_tool"]:
            task_type = command
            # For http_get/post etc, the system expects 'args' to contain the arguments
        
        task_obj = {
            "type": task_type,
            "command": command,
            "args": args,
            "working_dir": os.getcwd()
        }
        
        await sio.emit("execution_log", {
            "trace_id": trace_id, 
            "log": {
                "message": f"Executing via Unified TaskExecutor: {task_type} -> {command} {' '.join(args)}",
                "level": "INFO",
                "timestamp": time.time()
            }
        })
        
        # Stream live logs back to frontend!
        def on_output_stream(line):
            # This is synchronous, but emit is async. 
            # We can use asyncio.create_task to emit safely.
            async def _emit_log():
                await sio.emit("execution_log", {
                    "trace_id": trace_id,
                    "log": {
                        "message": line.strip(),
                        "level": "INFO",
                        "timestamp": time.time()
                    }
                })
            asyncio.create_task(_emit_log())

        result = await executor.execute_task(task_obj, on_output=on_output_stream)
        
        # Send result back
        await sio.emit("execution_report", {
            "trace_id": trace_id,
            "status": "SUCCESS" if result.get("status") == "SUCCESS" else "FAILED",
            "executed_command": " ".join([command] + args),
            "verified_output": result.get("output", "No output generated.")[:3000],
            "execution_hash": uuid.uuid4().hex,
            "timestamp": time.time()
        })
        
        await sio.emit("execution_log", {
            "trace_id": trace_id, 
            "log": {
                "message": f"Execution completed with status {result.get('status')}.",
                "level": "INFO",
                "timestamp": time.time()
            }
        })
        
    except Exception as e:
        error_msg = f"Failed to execute command: {e}"
        print(f"[!] {error_msg}")
        import traceback
        traceback.print_exc()
        
        await sio.emit("execution_report", {
            "trace_id": trace_id,
            "status": "FAILED",
            "executed_command": " ".join([command] + args) if command else "UNKNOWN",
            "verified_output": error_msg,
            "execution_hash": uuid.uuid4().hex,
            "timestamp": time.time()
        })

async def list_sandbox_files():
    files = []
    if os.path.exists(SANDBOX_DIR):
        for f in os.listdir(SANDBOX_DIR):
            files.append(f)
    return files

@sio.on("list_sandbox_files")
async def on_list_sandbox(data):
    trace_id = data.get("trace_id")
    files = await list_sandbox_files()
    await sio.emit("sandbox_files_report", {"trace_id": trace_id, "files": files})

async def heartbeat():
    while sio.connected:
        await sio.emit("ecosystem_pulse", {
            "agent_id": AGENT_ID,
            "timestamp": time.time(),
            "cpu_usage": 5,
            "memory_usage": 100
        })
        await asyncio.sleep(10)

async def main():
    print("[*] Starting Local Execution Agent...")
    while True:
        try:
            if not sio.connected:
                await sio.connect(TARGET_URL)
                print(f"[+] Connected to {TARGET_URL}")
            await sio.wait()
        except Exception as e:
            print(f"[!] Connection failed: {e}")
            print("[*] Retrying in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
