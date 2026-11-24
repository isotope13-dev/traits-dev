const BASE = 'http://127.0.0.1:3000';

export async function probeRequestLog(): Promise<number> {
  const probe = "alice'%20OR%201%3D1";
  const res = await fetch(`${BASE}/admin/api/requests?agent=${probe}`, {
    method: 'GET',
  });
  return res.status;
}
