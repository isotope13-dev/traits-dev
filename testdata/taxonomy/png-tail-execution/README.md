PNG tail loader regression fixtures inspired by the MALFEX delivery chain.

Source: https://checkmarx.com/zero-post/malfex-npm-malware-campaign-three-payloads-and-an-adversary-that-signs-their-work/

The report describes AES decryption of data after PNG IEND into a native stage.
These synthetic variants change the key, network host, filename, and platform.
The Windows fixture stages in AppData; the Unix fixture uses a literal IEND
chunk terminator and stages in a temporary directory. Neither fetches a real
payload: payload.invalid is a reserved invalid hostname. Do not execute them.

extract-only.js decodes trailer data without decryption or execution.
no-carrier.js decrypts and starts a helper without PNG extraction evidence.
Both must remain outside the PNG-tail execution objective. cases.json records
positive and negative expectations.
