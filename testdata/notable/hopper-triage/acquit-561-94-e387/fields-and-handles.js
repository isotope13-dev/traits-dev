try { probe(); } catch(e) { errors.push({code:e.code, error:e.message}); }
async function save(handle, bytes) { return handle.write(bytes); }
const httpMethod = 'HEAD';
const pythonVersionFlag = '-3';
const settings = {StartWhenAvailable:true};
const spec = {'args': ['-c', script]};
