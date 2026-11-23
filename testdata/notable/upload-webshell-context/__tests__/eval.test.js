// Upload inspection regression case.
describe('upload inspection', () => {
  it('detects an eval webshell', () => {
    const verdict = inspectBytes(Buffer.from('<?php @eval($_POST["x"]); ?>'));
    expect(verdict.findings[0]).toMatchObject({rule: 'upload.webshell', signature: 'php.eval_request'});
  });
});
