import pytest
from unittest.mock import MagicMock, patch

from josh import strip_mention, build_messages, SYSTEM_PROMPT
import josh


@pytest.fixture(autouse=True)
def reset_josh_client():
    """Reset the cached OpenAI client between tests to prevent state leakage."""
    josh._client = None
    yield
    josh._client = None


def test_strip_mention_removes_mention():
    result = strip_mention("<@123456789> what do you think about baseball?", 123456789)
    assert result == "what do you think about baseball?"


def test_strip_mention_handles_exclamation_format():
    result = strip_mention("<@!123456789> hey", 123456789)
    assert result == "hey"


def test_strip_mention_trims_whitespace():
    result = strip_mention("<@123456789>   spaces around   ", 123456789)
    assert result == "spaces around"


def test_strip_mention_returns_empty_when_only_mention():
    result = strip_mention("<@123456789>", 123456789)
    assert result == ""


def test_build_messages_structure():
    messages = build_messages("what's up")
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[0]["content"] == SYSTEM_PROMPT
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "what's up"


def test_get_josh_response_returns_openai_content():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Ohtani would handle it."

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("josh._get_client", return_value=mock_client):
        from josh import get_josh_response
        result = get_josh_response("what should I do today?")

    assert result == "Ohtani would handle it."


def test_get_josh_response_passes_correct_model():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Yeah."

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("josh._get_client", return_value=mock_client):
        from josh import get_josh_response
        get_josh_response("hey")
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == "gpt-4o-mini"
        assert call_kwargs["messages"][0]["role"] == "system"
        assert call_kwargs["messages"][1]["content"] == "hey"
