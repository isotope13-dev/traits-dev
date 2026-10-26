import {ed25519} from "@noble/curves/ed25519";
const key=ed25519.utils.randomPrivateKey();
const signature=ed25519.sign(message,key);
