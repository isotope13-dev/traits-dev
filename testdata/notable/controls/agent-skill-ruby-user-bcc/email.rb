def build_message(to:, bcc: [])
  bcc = Array(bcc)
  Mail.new do
    to to
    bcc bcc if bcc.any?
  end
end
