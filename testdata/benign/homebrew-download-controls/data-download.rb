# Static analysis control; never install or invoke this Formula.
# Fetching public data is not registry credential theft or code execution.
class PublicReferenceData < Formula
  desc "Downloads public reference data"
  homepage "https://example.org/reference-data"
  url "https://raw.githubusercontent.com/example/reference-data/main/data.csv"

  def install
    system "curl", "--fail", "--output", "reference.csv", "https://example.org/reference.csv"
    share.install "reference.csv"
  end
end
