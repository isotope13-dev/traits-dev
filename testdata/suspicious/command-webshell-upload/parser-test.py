def test_extract_multipart_parts_pulls_filename_and_php_shell():
    boundary = "----WebKitFormBoundaryABC123"
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="upload[]"; filename="shell.php"\r\n'
        "Content-Type: application/x-php\r\n"
        "\r\n"
        "<?php system($_GET['cmd']); ?>\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")
    names, filenames, content_types, has_php_shell = tbenv.extract_multipart_parts(
        body, f"multipart/form-data; boundary={boundary}", 16,
    )
    assert names == ["upload[]"]
    assert filenames == ["shell.php"]
    assert content_types == ["application/x-php"]
    assert has_php_shell is True

