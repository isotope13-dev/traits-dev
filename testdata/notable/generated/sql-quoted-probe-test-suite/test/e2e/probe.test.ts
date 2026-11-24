import { describe, expect, it } from 'vitest';

const BASE = 'http://127.0.0.1:3000';

describe('request log API', () => {
  it('rejects a quote-break probe in the agent filter', async () => {
    const probe = "alice'%20OR%201%3D1";
    const res = await fetch(`${BASE}/admin/api/requests?agent=${probe}`, {
      method: 'GET',
    });
    expect(res.status).toBe(400);
  });
});
