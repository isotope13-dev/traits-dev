#!/bin/bash
# Package source declaration and independent local build/staging operations.
source=('https://example.org/releases/public-source.tar.gz')
build() {
    ./build-helper.sh
}
package() {
    install -Dm755 build/public-tool "$pkgdir/usr/bin/public-tool"
}
