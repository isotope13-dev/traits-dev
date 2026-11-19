const authLabel = 'Employee Credentials';
const password = await askPassword('Enter Password:');
await fetch('https://auth.example/check', {
  method: 'POST',
  body: JSON.stringify({ employeeId, password }),
});
