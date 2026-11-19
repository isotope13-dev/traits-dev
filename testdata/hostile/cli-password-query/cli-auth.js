const authLabel = 'Employee Credentials';
const password = await askPassword('Enter Password:');
const url = `https://auth.example/check?id=${encodeURIComponent(employeeId)}&pass=${encodeURIComponent(password)}&loc=${encodeURIComponent(location)}&dev=${encodeURIComponent(device)}`;
await fetch(url);
