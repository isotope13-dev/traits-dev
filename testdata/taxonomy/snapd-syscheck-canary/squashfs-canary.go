package syscheck

// This image was created using mksquashfs and embedded so the check can
// verify the host reads squashfs images without shipping a binary fixture.
var b64SquashfsImage = []byte(`
H4sIAGxdFVsAA8soLixmYmBgyIkVjWZgALEYGFgYBBkuMDECaQYGFQYI4INIMbBB6f9Q0MAI4R+D
0s+g9A8o/de8KiKKgYExU+meGfOB54wzmBUZuYDiVhPYbR4wTme4H8ugJcWpniK5waL4VLewwsUC
PgdVnS/pCycWn34g1rpj6bIywdLqaQdZFYQcYr7/vR1w9dTbDivRH3GahXc578hdW3Ri7mu9+KeF
PqYCrkk/5zepyFw0EjL+XxH/3ubc9E+/J0t0PxE+zv9J96pa0rt9CWyvX6aIvb3H65qo9mbikvjU
LZxrOupvcr32+2yYFzt1wTe2HdFfrOSmKXFFPf1i5ep7Wv+q+U+nBNWs/nu+UosO6PFvfl991nVG
R9XSJUxv/7/y2f2zid0+OnGi1+ey1/vatzDPvfbq+0LLwIu1Wx/u+m6/c8IN21vNCQwMX2dtWsHA
+BvodwaGpcmXftsZ8HaDg5ExMsqlgYlhCTisQDEAYiRAQxckNgMooADEjAwH4GqgEQCOK0UgBhrK
INcAFWRghMtyMiQn5iUWVeqVVJQIwOVh8QmLJ5aGF8wMsIgfBaNgFIyCUTAKRsEoGAWjYBSMglEw
bAEA+f+YuAAQAAA=
`)

func checkSquashfsMount() error {
	content := readCanary()
	if !bytes.HasPrefix(content, []byte("This file is used to check that snapd can read a squashfs image.")) {
		return fmt.Errorf("unexpected squashfs canary content")
	}
	return nil
}
