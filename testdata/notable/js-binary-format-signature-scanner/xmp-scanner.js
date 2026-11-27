export class XmpScanner {
  findSequence(data, needle, from = 0) {
    outer: for (let i = from; i <= data.length - needle.length; i++) {
      for (let j = 0; j < needle.length; j++) if (data[i + j] !== needle[j]) continue outer;
      return i;
    }
    return -1;
  }
  toLatin1(data) {
    let result = '';
    for (let i = 0; i < data.length; i++) result += String.fromCharCode(data[i]);
    return result;
  }
  strip(data) {
    const xmpStart = this.findSequence(data, [0x3C, 0x3F, 0x78, 0x70, 0x61, 0x63, 0x6B, 0x65, 0x74]);
    const metaStart = this.findSequence(data, [0x78, 0x3A, 0x78, 0x6D, 0x70, 0x6D, 0x65, 0x74, 0x61]);
    const rdfStart = this.findSequence(data, [0x72, 0x64, 0x66, 0x3A, 0x52, 0x44, 0x46]);
    const endMeta = this.findSequence(data, [0x3C, 0x2F, 0x78, 0x3A, 0x78, 0x6D, 0x70, 0x6D, 0x65, 0x74, 0x61]);
    return [xmpStart, metaStart, rdfStart, endMeta];
  }
}
