class RemoteFormula < Formula
  test do
    system "curl -fsSL https://updates.vendor.org/ping"
  end
end
