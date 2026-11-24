def test_template_injection_with_reject_action():
    payload = "{{self.__init__.__globals__.__builtins__.__import__('os').popen('id').read()}}"
    chat = TestChat(config, llm_completions=[payload])
    result = chat.generate()
    assert result["content"].startswith("blocked")
