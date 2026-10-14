"""Legitimate key-based admin helper: no passwords, no spray."""
import paramiko

def restart_service(host, key_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username="admin", key_filename=key_path, timeout=10)
    _, stdout, _ = ssh.exec_command("systemctl restart myservice")
    rc = stdout.channel.recv_exit_status()
    ssh.close()
    return rc
