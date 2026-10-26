// Ordinary hardware inventory: no VM-dependent exit or payload.
async function inventory(si) {
  const info = await si.system();
  await si.uuid();
  await si.cpu();
  await si.chassis();
  await si.baseboard();
  await si.diskLayout();
  const command = 'dmidecode -t system';
  const fields = ['dmi product_name', 'QEMU', 'VMware', 'Bochs'];
  return {info, command, fields};
}
