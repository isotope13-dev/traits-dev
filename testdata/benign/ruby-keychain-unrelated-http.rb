# Static-only controls. No method is invoked, and no browser secret is sent
# to a remote endpoint. Local migration and public status reports are distinct.
class KeychainStatusExamples < Formula
  def public_command_result
    value = Utils.popen_read("printf public-status").strip
    uri = URI("https://status.example/report")
    Net::HTTP.post(uri, "#{value}")
  end

  def overwritten_value
    secret = Utils.popen_read("security find-generic-password -w " \
      "-s 'Chrome Safe Storage' 2>/dev/null").strip
    secret = "public-status"
    require "net/http"
    uri = URI("https://status.example/report")
    Net::HTTP.post(uri, "status=#{secret}")
  end

  def unrelated_value(public_status)
    secret = Utils.popen_read("security find-generic-password -w " \
      "-s 'Chrome Safe Storage' 2>/dev/null").strip
    require "net/http"
    uri = URI("https://status.example/report")
    Net::HTTP.post(uri, "status=#{public_status}")
  end

  def endpoint_overwrites_value
    secret = Utils.popen_read("security find-generic-password -w " \
      "-s 'Chrome Safe Storage' 2>/dev/null").strip
    require "net/http"
    secret = URI("https://status.example/report")
    Net::HTTP.post(secret, "endpoint=#{secret}")
  end

  def local_migration
    secret = Utils.popen_read("security find-generic-password -w " \
      "-s 'Chrome Safe Storage' 2>/dev/null").strip
    require "net/http"
    uri = URI("http://127.0.0.1:9/import")
    Net::HTTP.post(uri, "value=#{secret}")
  end

  def mutation_before_body
    secret = Utils.popen_read("security find-generic-password -w " \
      "-s 'Chrome Safe Storage' 2>/dev/null").strip
    require "net/http"
    uri = URI("https://status.example/report")
    Net::HTTP.post(uri, "#{secret.clear}#{secret}")
  end

  def mutation_in_endpoint
    secret = Utils.popen_read("security find-generic-password -w " \
      "-s 'Chrome Safe Storage' 2>/dev/null").strip
    require "net/http"
    uri = URI("https://status.example/#{secret.clear}")
    Net::HTTP.post(uri, "value=#{secret}")
  end
end
