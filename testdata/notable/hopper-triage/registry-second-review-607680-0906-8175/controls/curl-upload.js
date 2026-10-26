const {execSync}=require('child_process'); execSync('curl -s --data-binary @- https://collector.example.test', {input: 'report'});
