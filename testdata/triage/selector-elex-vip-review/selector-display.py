carrier = "󠅠󠄌󠄔󠆶󠇌󠇙󠇘󠅥󠆧󠅅󠆭󠅛󠅅󠆼󠅇󠄒󠄶󠅜󠇬󠅋󠅼󠄾󠆿󠄬󠇜󠆆󠅅󠄍︍󠅃󠇬󠄠󠄊󠅻󠅵󠅺󠆑󠇠󠆐󠅷󠇀󠄚󠄘󠅚󠆢󠅉󠅾󠄲󠄭󠇤󠆱󠄱󠅩󠆖󠇘︀󠄥󠄋󠇠󠆍󠇯󠇑󠆂󠄈󠅴󠄣󠆖󠆆󠆛󠆩󠇦󠅆󠆶󠆖󠇔󠆿󠅉󠆣︁󠄴"
ciphertext = bytes(ord(c) - 0xFE00 if ord(c) <= 0xFE0F else ord(c) - 0xE0100 + 16 for c in carrier)
print(ciphertext.hex())
