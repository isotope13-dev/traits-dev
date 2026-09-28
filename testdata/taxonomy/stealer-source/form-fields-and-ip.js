// Preparing form fields beside a destination does not send the form.
const destination = 'http://45.77.22.11/upload';
const formData = new FormData();
formData.append('note', 'report');
console.log(destination, formData);
