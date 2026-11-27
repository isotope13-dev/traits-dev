#!/usr/bin/env python3
# Local helper: print which known security products are running.
import psutil

AV_NAMES = ["MsMpEng.exe", "ekrn.exe", "CylanceSvc.exe", "SentinelAgent.exe"]


def main():
    names = {str(p.info["name"]).lower() for p in psutil.process_iter(["name"])}
    for n in AV_NAMES:
        print(n, "running" if n.lower() in names else "absent")


if __name__ == "__main__":
    main()
