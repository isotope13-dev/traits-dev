require "open3"
Open3.capture3("kubectl", "get", "pods")
