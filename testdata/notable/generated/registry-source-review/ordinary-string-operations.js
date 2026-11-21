function parseSocket(data) {
  let alldata = '';
  alldata = alldata + data.toString();
  const packages = 'SIP|DIP|DIMM|SODIMM'.split('|');
  return { alldata, packages };
}
