class ContentReader {
  Object read(android.content.Context context, android.net.Uri uri) throws Exception {
    return context.getContentResolver().openInputStream(uri);
  }
}
