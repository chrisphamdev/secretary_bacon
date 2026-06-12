# Secretary Bacon — Discord Bot

Discord bot for the server **Cong ty TNHH MTV Fuho**. Command prefix is `.`

## Running the bot

```bash
python run.py
```

Prompts for two secrets on startup (both hidden via `getpass`):
1. **Discord bot token**
2. **Football API key** — from [football-data.org](https://www.football-data.org), needed for World Cup commands

## Project structure

| File | Purpose |
|---|---|
| `run.py` | Entry point — prompts for tokens, starts the bot |
| `main.py` | Bot instance + imports all feature modules |
| `basiccommands.py` | Misc commands: ping, lotto, cleanup, dis, etc. |
| `archive.py` | Reaction-role system (hardcoded message/role IDs) |
| `stockgame.py` | Stock trading simulator using yahoo_fin / yfinance |
| `pokergame.py` | Texas Hold'em poker game, one game per channel |
| `worldcup.py` | World Cup 2026 fantasy league (predictions + leaderboard) |
| `helper/poker.py` | Pure poker logic: hand evaluation, game state |
| `helper/Deck.py` | Card/Deck classes |
| `database/databasehandler.py` | TinyDB wrapper for stock game portfolio data |
| `database/casino.json` | TinyDB file for stock game |
| `database/wc_predictions.json` | World Cup predictions (auto-created) |
| `database/wc_match_cache.json` | Cached match results from football-data.org (auto-created) |

## Dependencies

```
discord.py==1.7.3
tinydb==4.5.2
aiohttp>=3.8.0        # already a transitive dep of discord.py
yahoo_fin==0.8.9.1
yfinance==0.1.70
beautifulsoup4==4.11.1
```

**Note:** The `venv/` interpreter (`python@3.9`) has been uninstalled from this machine. The site-packages are still present and functional when the bot is run with a working Python 3.9 binary. `aiohttp 3.7.4` is already installed in the venv as a discord.py dependency.

## Adding a new feature module

1. Create `myfeature.py`, import `bot` from `main`: `from main import bot`
2. Define commands with `@bot.command(name='...')`
3. Add `from myfeature import *` to `main.py`

## World Cup fantasy league

Commands (all prefixed with `.`):

| Command | Description |
|---|---|
| `.wcmatches [upcoming\|today\|live\|recent]` | Browse fixtures |
| `.wcpredict <match_id> 2-1` | Predict by match ID |
| `.wcpredict 🇳🇿 🇦🇺 2-1` | Predict by flag emojis (`:flag_nz:` style) |
| `.mypicks` | Your predictions + current points |
| `.wcleaderboard` | Full leaderboard |
| `.wchelp` | Command reference |

Scoring: **2 pts** exact scoreline, **1 pt** correct result (win/draw/loss), **0 pts** otherwise.

Predictions lock once a match enters `IN_PLAY`. Results are fetched from the football-data.org API and cached in `database/wc_match_cache.json` — finished matches are never re-fetched.

Flag emoji lookup uses `FLAG_TO_TEAM` in `worldcup.py` (ISO alpha-2 → team name). If a flag isn't in the map, the bot tells the user to use a match ID instead. When the user's flag order differs from the API fixture order, the score is silently flipped to match intent.

## Known issues / quirks

- `basiccommands.py` imports `from carlookup import *` — that file no longer exists. The import will fail on startup unless removed or the file is restored.
- `archive.py` reaction-role handlers contain hardcoded message and role IDs specific to the original server.
- The stock game (`stockgame.py`) uses `yf.Ticker` without importing `yfinance as yf` — the `summary` command will error.
