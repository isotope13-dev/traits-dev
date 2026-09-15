-- Suspicious encoded-execution fixture. Compile and inspect; do not run.
-- The hidden command only prints a marker, but base64-to-sh is intentional.
set payload to "cHJpbnRmICclc1xuJyAnU0NQVF9CQVNFNjRfT0sn"
do shell script "printf %s " & quoted form of payload & " | base64 -D | sh"
