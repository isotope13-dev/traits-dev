# Static analysis control: all installation-like text below is documentation.
class FormulaGuide < Formula
  url "https://docs.github.io/reference/manual.txt"

  def caveats
    <<~GUIDE
      Example formula method:
        def install
          system "curl", "--output", "data.csv", "https://example.org/data.csv"
        end
    GUIDE
  end
end
