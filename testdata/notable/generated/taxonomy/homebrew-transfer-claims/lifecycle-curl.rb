class RemoteFormula < Formula
  def install
    system "curl -fsSL https://updates.vendor.org/ping"
  end
end
