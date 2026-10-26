# Beaker-style acceptance config: selects which SSH identity to CONNECT with,
# without reading any credential file. Naming a key path is client config,
# not credential theft.
{
  :load_path => File.join('acceptance', 'lib'),
  :ssh => {
    :keys => ["id_rsa_acceptance", "#{ENV['HOME']}/.ssh/id_rsa-acceptance"],
  },
}
