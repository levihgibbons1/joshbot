from josh import strip_mention, build_messages, SYSTEM_PROMPT


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
