const BASE_URL = 'https://lekzoasync.my.id';

export async function sendLink(email) {
  if (!email || !email.includes('@')) {
    throw new Error('Email tidak valid!');
  }
  
  try {
    const response = await fetch(`${BASE_URL}/api/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gmail: email })
    });
    
    let data;
    try {
      data = await response.json();
    } catch (err) {
      throw new Error(`Server Error (HTTP ${response.status}). Pastikan domain benar.`);
    }

    if (!data.success) throw new Error(data.error || 'Gagal kirim magic link');
    return data;
  } catch (error) {
    throw new Error(`Gagal kirim magic link: ${error.message}`);
  }
}

export async function verifyLink(email, magicLink) {
  if (!email || !email.includes('@')) {
    throw new Error('Email tidak valid!');
  }
  if (!magicLink || !magicLink.startsWith('https://')) {
    throw new Error('Magic link tidak valid!');
  }
  
  try {
    const response = await fetch(`${BASE_URL}/api/verif`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gmail: email, link: magicLink })
    });
    
    let data;
    try {
      data = await response.json();
    } catch (err) {
      throw new Error(`Server Error (HTTP ${response.status}). Pastikan domain benar.`);
    }

    if (!data.success) throw new Error(data.error || 'Gagal verifikasi');
    return data;
  } catch (error) {
    throw new Error(`Gagal verifikasi: ${error.message}`);
  }
}

export async function bulkGenerate(total) {
  if (!total || total < 1 || total > 5) {
    throw new Error('Jumlah akun harus antara 1-5!');
  }
  
  try {
    const response = await fetch(`${BASE_URL}/api/bulk`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ total })
    });
    
    let data;
    try {
      data = await response.json();
    } catch (err) {
      throw new Error(`Server Error (HTTP ${response.status}). Pastikan domain benar.`);
    }

    if (!data.success) throw new Error(data.error || 'Gagal generate bulk');
    return data;
  } catch (error) {
    throw new Error(`Gagal generate bulk: ${error.message}`);
  }
}