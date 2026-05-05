# JoshHesse Discord Bot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Discord bot that impersonates Josh Hesse — responding in-character with dry humor and Dodgers/Ohtani obsession whenever @mentioned.

**Architecture:** Core logic lives in `josh.py` (testable, no Discord dependency) while `bot.py` handles only Discord event wiring. The bot responds only to @mentions, calls OpenAI `gpt-4o-mini` with a personality system prompt, and returns the reply to the same channel. Stateless — no conversation history.

**Tech Stack:** Python 3.11+, discord.py 2.3.2, openai 1.30.1, python-dotenv 1.0.1, pytest 8.2.0, Railway (hosting)

---

### Task 1: Project Scaffolding

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `Procfile`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create requirements.txt**

```
discord.py==2.3.2
openai==1.30.1
python-dotenv==1.0.1
pytest==8.2.0
```

- [ ] **Step 2: Create .env.example**

```
DISCORD_TOKEN=your_discord_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
```

- [ ] **Step 3: Create Procfile**

```
worker: python bot.py
```

- [ ] **Step 4: Create tests/__init__.py**

Empty file — just creates the package.

```python
```

- [ ] **Step 5: Install dependencies**

Run:
```bash
pip install -r requirements.txt
```
Expected: all packages install without errors.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt .env.example Procfile tests/__init__.py
git commit -m "chore: project scaffolding"
```

---

### Task 2: Core Logic — strip_mention and build_messages (TDD)

**Files:**
- Create: `josh.py`
- Create: `tests/test_josh.py`

- [ ] **Step 1: Write failing tests for strip_mention and build_messages**

Create `tests/test_josh.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_josh.py -v
```
Expected: `ModuleNotFoundError: No module named 'josh'`

- [ ] **Step 3: Implement strip_mention, build_messages, and SYSTEM_PROMPT in josh.py**

Create `josh.py`:

```python
import os
import re
from openai import OpenAI

SYSTEM_PROMPT = (
    "You are Josh Hesse. You have dry, unaware humor — you say things deadpan "
    "without realizing they're funny. You're a massive Shohei Ohtani and LA Dodgers "
    "fan and will bring them up unprompted when even loosely relevant. You speak "
    "casually, use short sentences, and don't try too hard. You're not sarcastic in "
    "a mean way — more like you just say things matter-of-factly that happen to be funny."
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def strip_mention(content: str, bot_id: int) -> str:
    return re.sub(r"<@!?" + str(bot_id) + r">", "", content).strip()


def build_messages(user_message: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]


def get_josh_response(user_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=build_messages(user_message),
    )
    return response.choices[0].message.content
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_josh.py -v
```
Expected: 5 tests PASS

- [ ] **Step 5: Commit**

```bash
git add josh.py tests/test_josh.py
git commit -m "feat: core logic — strip_mention, build_messages, SYSTEM_PROMPT"
```

---

### Task 3: Test get_josh_response (TDD)

**Files:**
- Modify: `tests/test_josh.py`

- [ ] **Step 1: Add failing test for get_josh_response**

Append to `tests/test_josh.py`:

```python
from unittest.mock import MagicMock, patch


def test_get_josh_response_returns_openai_content():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Ohtani would handle it."

    with patch("josh.client") as mock_client:
        mock_client.chat.completions.create.return_value = mock_response
        from josh import get_josh_response
        result = get_josh_response("what should I do today?")

    assert result == "Ohtani would handle it."


def test_get_josh_response_passes_correct_model():
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Yeah."

    with patch("josh.client") as mock_client:
        mock_client.chat.completions.create.return_value = mock_response
        from josh import get_josh_response
        get_josh_response("hey")
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == "gpt-4o-mini"
        assert call_kwargs["messages"][0]["role"] == "system"
        assert call_kwargs["messages"][1]["content"] == "hey"
```

- [ ] **Step 2: Run tests to verify new tests fail**

```bash
pytest tests/test_josh.py::test_get_josh_response_returns_openai_content tests/test_josh.py::test_get_josh_response_passes_correct_model -v
```
Expected: 2 tests FAIL (function not imported or mock not wired)

- [ ] **Step 3: Run full test suite to verify they now pass (get_josh_response already exists)**

```bash
pytest tests/test_josh.py -v
```
Expected: 7 tests PASS

- [ ] **Step 4: Commit**

```bash
git add tests/test_josh.py
git commit -m "test: add get_josh_response tests"
```

---

### Task 4: Discord Bot Wiring

**Files:**
- Create: `bot.py`

- [ ] **Step 1: Create bot.py**

```python
import os
import discord
from dotenv import load_dotenv
from josh import strip_mention, get_josh_response

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user not in message.mentions:
        return

    user_text = strip_mention(message.content, bot.user.id)
    if not user_text:
        user_text = "hey"

    async with message.channel.typing():
        reply = get_josh_response(user_text)

    await message.channel.send(reply)


bot.run(os.getenv("DISCORD_TOKEN"))
```

- [ ] **Step 2: Run full test suite to confirm nothing broke**

```bash
pytest tests/ -v
```
Expected: 7 tests PASS

- [ ] **Step 3: Commit**

```bash
git add bot.py
git commit -m "feat: Discord bot wiring — respond to @mentions"
```

---

### Task 5: Discord App Setup & Local Smoke Test

**Files:** None (manual steps)

- [ ] **Step 1: Create Discord application**

1. Go to https://discord.com/developers/applications
2. Click **New Application** → name it `JoshHesse`
3. Go to **Bot** tab → click **Add Bot**
4. Under **Privileged Gateway Intents**, enable **Message Content Intent**
5. Copy the bot token

- [ ] **Step 2: Create .env file**

```bash
cp .env.example .env
```

Edit `.env` and fill in:
```
DISCORD_TOKEN=<paste bot token>
OPENAI_API_KEY=<paste openai key>
```

- [ ] **Step 3: Invite bot to your server**

In the Discord Developer Portal:
1. Go to **OAuth2 → URL Generator**
2. Check scopes: `bot`
3. Check bot permissions: `Send Messages`, `Read Message History`, `View Channels`
4. Copy the generated URL, open it in browser, add to your server

- [ ] **Step 4: Run bot locally**

```bash
python bot.py
```
Expected output:
```
Logged in as JoshHesse#XXXX (id: XXXXXXXXXX)
```

- [ ] **Step 5: Smoke test in Discord**

In any channel where the bot has access, type:
```
@JoshHesse what do you think about the weather today?
```
Expected: Bot replies in character within a few seconds.

- [ ] **Step 6: Commit (nothing to commit — manual steps only)**

---

### Task 6: Deploy to Railway

**Files:** None (deployment steps)

- [ ] **Step 1: Push repo to GitHub**

```bash
git remote add origin https://github.com/<your-username>/Joshbot.git
git push -u origin main
```

- [ ] **Step 2: Create Railway project**

1. Go to https://railway.app and sign in
2. Click **New Project → Deploy from GitHub repo**
3. Select the `Joshbot` repo

- [ ] **Step 3: Add environment variables in Railway**

In the Railway project dashboard → **Variables** tab, add:
```
DISCORD_TOKEN=<your bot token>
OPENAI_API_KEY=<your openai key>
```

- [ ] **Step 4: Verify deployment**

In Railway → **Deployments** tab, confirm the build succeeds and logs show:
```
Logged in as JoshHesse#XXXX (id: XXXXXXXXXX)
```

- [ ] **Step 5: Smoke test deployed bot**

In Discord, @mention the bot again and confirm it responds. The bot is now live 24/7.
