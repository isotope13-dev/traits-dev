# Benign control: backup capacity administration. Lists shadow copies and
# grows shadow storage on a backup volume. No deletion, no encryption.
vssadmin list shadows
vssadmin resize shadowstorage /for=D: /on=D: /maxsize=20%
vssadmin list shadowstorage
