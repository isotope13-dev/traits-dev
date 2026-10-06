"""IoTSploit-style network audit harness control.

Mimics an authorized flood/stress routine (start_/stop_ pair, explicit
target, hping3 with --flood --rand-source, UDP random-port sendto) inside
the recognized security-testing distribution. None of the DoS
hostile/suspicious traits may fire here.
"""
import random
import socket


class NetAudit_Mgr:
    def start_tcp_flood_attack(self, target_ip: str):
        self.stop_tcp_flood_attack()
        cmd = "sudo hping3 -V -d 120 -S -w 64 -p 445 -s 445 --flood --rand-source {}".format(
            target_ip
        )
        return cmd

    def stop_tcp_flood_attack(self):
        return 1

    def start_udp_flood_attack(self, target_ip: str, target_port=0):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if target_port == 0:
            port = random.randint(1, 65535)
        else:
            port = target_port
        sock.sendto(b"\xAA" * 128, (target_ip, port))
        sock.close()
