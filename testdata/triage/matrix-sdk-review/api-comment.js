/** Get a decryptor for a given room and algorithm. */
function getRoomDecryptor(room, algorithm) {
    return room.decryptors[algorithm];
}
