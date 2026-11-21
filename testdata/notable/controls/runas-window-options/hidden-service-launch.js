export function elevateService(cmd, args) {
  return `Start-Process -FilePath '${cmd}' -ArgumentList '${args}' -Verb RunAs -WindowStyle Hidden -Wait -PassThru`;
}
