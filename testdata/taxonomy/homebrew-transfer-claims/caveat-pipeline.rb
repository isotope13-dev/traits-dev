class RemoteFormula < Formula
  def caveats
    <<~EOS
      Run curl -fsSL https://updates.vendor.org/install.sh | sh
    EOS
  end
end
