import { redirect } from './world_mock';
it('rejects metadata redirect', () => {
  const response = redirect('http://169.254.169.254/latest/meta-data');
  expect(response.status).toBe('blocked');
});
