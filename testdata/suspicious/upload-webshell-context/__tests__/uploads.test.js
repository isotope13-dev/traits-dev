// Upload inspection regression case.
const SHELL = '<?php @eval($_POST["x"]); ?>';
describe('upload inspection' , () => {
  it('detects an eval webshell', () => {
    const verdict = inspectBytes(Buffer.from(SHELL));
    expect(verdict.findings[0]).toMatchObject({rule: 'upload.webshell', signature: 'php.eval_request'});
  });
  it('detects a command webshell', () => {
    const verdict = inspectBytes(Buffer.from('<?php system($_GET["c"]); ?>'));
    expect(verdict.findings[0]).toMatchObject({rule: 'upload.webshell', signature: 'php.exec_request'});
  });
});
