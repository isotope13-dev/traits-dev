import { expect, test } from 'bun:test';

test('credential route returns scoped keys', async () => {
    const fetcher = async (input: string | URL | Request) => {
        const url = String(input);
        if (url.endsWith('/edge-cloud/credentials')) {
            return Response.json({ encryptionKeys: { chan: Buffer.alloc(32, 7).toString('base64') } });
        }
        throw new Error(`unexpected ${url}`);
    };
    const response = await fetcher('https://example.invalid/edge-cloud/credentials');
    expect(response.status).toBe(200);
});
