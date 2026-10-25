import { platform, release } from 'node:os'
import { gzip } from 'node:zlib'
import { promisify } from 'node:util'
const compress = promisify(gzip)
export const run = (x: string) => [platform(), release(), compress(x)]
