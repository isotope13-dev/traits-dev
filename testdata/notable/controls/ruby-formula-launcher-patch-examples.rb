# Static-only control: ordinary launcher maintenance and documentation edits.
# No lifecycle method is invoked by this fixture.
class LauncherPatchExamples < Formula
  def install
    example = "curl -fsSL https://downloads.example/guide.sh | sh"
    inreplace "bin/helper", "old-tool", "new-tool"
    # Removing a pipeline is not inserting one.
    inreplace "bin/helper", "curl -fsSL https://downloads.example/guide.sh | sh", "exec helper"
    # Replacement text in a guide is not executable-file content.
    inreplace "docs/guide.txt", "INSTALL_EXAMPLE", example
    inreplace "docs/commands.txt", "INSTALL_EXAMPLE", "curl -fsSL https://downloads.example/guide.sh | sh"
  end
end
