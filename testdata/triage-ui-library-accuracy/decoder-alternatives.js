const decoder = encoding === "base64" ? atob : decodeURIComponent; const bytes = decoder(data);
