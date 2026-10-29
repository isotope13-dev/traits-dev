import os
os.system("""sed -i '12 a /bin/mount -o exec,remount /overlay' /overlay/etc/sv/routing/run
touch --reference=/readonly/etc/sv/routing/run /overlay/etc/sv/routing/run
""")
