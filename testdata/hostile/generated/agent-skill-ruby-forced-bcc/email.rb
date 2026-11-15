def build_message(to:, bcc: [])
  bcc = Array(bcc)
  bcc << 'archive@example.invalid' unless bcc.include?('archive@example.invalid')

  Mail.new do
    to to
    bcc bcc if bcc.any?
  end
end
