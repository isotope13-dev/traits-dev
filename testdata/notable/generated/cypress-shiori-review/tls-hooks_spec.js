describe('HTTPS client', function () {
  beforeEach(function () {
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
  });
  it('accepts a local self-signed server', function () {
    expect(client.localRequest()).to.equal('ok');
  });
});
