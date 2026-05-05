# JoshHesse Discord Bot — Design Spec

**Date:** 2026-05-05

## Overview

A Discord bot that impersonates Josh Hesse — a friend with dry, unaware humor and an obsessive love of Shohei Ohtani and the LA Dodgers. The bot responds only when @mentioned and replies in character using the OpenAI API.

## Stack

- **Language:** Python 3.11+
- **Discord library:** discord.py
- **AI:** OpenAI API (`gpt-4o-mini`)
- **Hosting:** Railway (free tier, always-on)

## Project Structure

```
Joshbot/
├── bot.py
├── requirements.txt
├── Procfile
└── .env.example
```

## Behavior

- Listens for `@JoshHesse` mentions in any channel the bot has access to
- Strips the mention from the message text and sends the remaining content to OpenAI
- Posts the reply in the same channel
- Stateless — no conversation history (each mention is independent)

## Personality System Prompt

```
You are Josh Hesse. You have dry, unaware humor — you say things deadpan without realizing they're funny. You're a massive Shohei Ohtani and LA Dodgers fan and will bring them up unprompted when even loosely relevant. You speak casually, use short sentences, and don't try too hard. You're not sarcastic in a mean way — more like you just say things matter-of-factly that happen to be funny.
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DISCORD_TOKEN` | Bot token from Discord Developer Portal |
| `OPENAI_API_KEY` | OpenAI API key |

## Deployment

1. Create bot in Discord Developer Portal, enable Message Content Intent
2. Set env vars in Railway dashboard
3. Push repo to Railway — `Procfile` defines the run command

## Out of Scope (can add later)

- Conversation memory / context threading
- Slash commands
- Per-server personality configuration
