#!/usr/bin/env python3
"""Static regression controls for brokered scanning and task run levels."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
WORKER = r'''package main
import (
    "bytes"
    "compress/gzip"
    "context"
    "net"
    "time"
    "github.com/rabbitmq/amqp091-go"
    "github.com/redis/go-redis/v9"
)
func bannerGrab(target string) []byte {
    connection, err := net.DialTimeout("tcp", target, time.Second)
    if err != nil { return nil }
    defer connection.Close()
    connection.SetReadDeadline(time.Now().Add(time.Second))
    banner := make([]byte, 1024)
    count, _ := connection.Read(banner)
    return banner[:count]
}
func main() {
    broker, _ := amqp091.Dial("amqps://mq-task.example.org")
    channel, _ := broker.Channel()
    tasks, _ := channel.Consume("penetration-tests", "", true, false, false, false, nil)
    resultDB := redis.NewClient(&redis.Options{Addr: "mq-result.example.org:6379"})
    for task := range tasks {
        banner := bannerGrab(string(task.Body))
        var packed bytes.Buffer
        writer := gzip.NewWriter(&packed)
        writer.Write(banner)
        writer.Close()
        resultDB.RPush(context.Background(), "scan-results", packed.Bytes())
    }
}
'''


def main():
    with tempfile.TemporaryDirectory(prefix="distributed-scan-precision-") as tmp:
        path = Path(tmp)
        fixtures = {
            "authorized.go": WORKER,
            "qscan.go": WORKER.replace("example.org", "qt-proxy.org"),
            "mixed-brokers.go": WORKER + '\nconst LocalBroker = "amqp://localhost:5672"\n',
            "local-broker.go": 'package config\nconst Broker = "amqp://guest:guest@localhost:5672"\n',
            "commented-redis.go": 'package config\n// import "github.com/redis/go-redis/v9"\n// redis.NewClient(nil)\n',

            "single-endpoint.go": 'package config\nconst Broker = "amqps://mq-task.qt-proxy.org"\n',
            "highest.xml": '<Task><Principals><Principal><RunLevel>HighestAvailable</RunLevel></Principal></Principals></Task>',
            "limited.xml": '<Task><Principals><Principal><RunLevel>LeastPrivilege</RunLevel></Principal></Principals></Task>',
        }
        for name, source in fixtures.items():
            (path / name).write_text(source)
        env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), CLEAVE_ANALYSIS_MEMO_MB="0")
        result = subprocess.run(
            [os.environ.get("ATOMSCAN", "atomscan"), "--no-update", "--mode", "slow",
             "--format", "json", "path", *[str(path / name) for name in fixtures]],
            text=True, capture_output=True, env=env, cwd=ROOT,
        )
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)
        assert "Failed to parse YAML" not in result.stderr, result.stderr
        reports = [json.loads(line) for line in result.stdout.splitlines()]
        roots = {Path(report["raw"]["files"][0]["path"]).name: report["raw"]["files"][0] for report in reports}
        assert roots.keys() == fixtures.keys(), (roots.keys(), result.stderr)
        findings = {name: {t["id"]: t["crit"] for t in root.get("traits", [])} for name, root in roots.items()}
        for name in ("authorized.go", "single-endpoint.go", "highest.xml", "limited.xml", "mixed-brokers.go", "local-broker.go", "commented-redis.go"):
            assert all(crit < 4 for crit in findings[name].values()), (name, findings[name])
        qscan = {key: crit for key, crit in findings["qscan.go"].items() if crit >= 4}
        prefix = "well-known/malware/botnet/qtfy::"
        assert qscan == {prefix + "qscan-worker-node": 4, prefix + "qtfy-platform-config": 4}, qscan
        assert findings["authorized.go"]["objectives/discovery/network/scan/distributed::brokered-scan-fleet-worker"] == 3
        broker = "micro-behaviors/communications/ipc/message::amqp-broker-url"
        assert broker in findings["mixed-brokers.go"]
        assert broker not in findings["local-broker.go"]
        for suffix in ("go-redis-import", "go-redis-new-client", "go-redis-client"):
            assert "micro-behaviors/data/db/redis::" + suffix not in findings["commented-redis.go"]
        task = "micro-behaviors/os/autorun/task-xml-scheduled::scheduled-task-highest-runlevel-xml"
        assert findings["highest.xml"][task] == 3
        assert task not in findings["limited.xml"]
        print("Passed: scanning, QScan evidence, mixed/local brokers, Redis comments, and task run levels")


if __name__ == "__main__":
    main()
