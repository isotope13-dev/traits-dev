require 'msf/core/payload_generator'

venom_generator = Msf::PayloadGenerator.new(generator_opts)
payload = venom_generator.generate_payload
