function parseSocket(data) {
  const alldata = String(data);
  const packages = 'SIP.DIP.DIMM.SODIMM'.split('.');
  return { alldata, packages };
}
