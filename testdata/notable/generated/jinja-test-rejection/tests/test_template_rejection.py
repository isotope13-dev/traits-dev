import pytest


@pytest.mark.parametrize(
    "template",
    [
        "{{ cycler.__init__.__globals__.__builtins__.len('harmless') }}",
        "{{ language | length }}",
    ],
)
def test_rejects_sandboxed_template(template):
    response = post_description(template)
    assert response.status_code in {400, 422}
