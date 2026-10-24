import { zip } from 'fflate';
import { encryptedStream } from './messages-media.js';
export function prepare(files, media) {
    zip(files, (error, result) => console.log(error, result));
    return encryptedStream(media, 'image', {});
}

export function transfer(options, filePath) {
    return options.upload(filePath, {mediaType: 'image'});
}
