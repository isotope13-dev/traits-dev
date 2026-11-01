snapshot = ENV.to_hash.map { |name, value| "#{value}=#{name}" }.join("\n")
