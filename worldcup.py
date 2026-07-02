import discord
from main import bot
import json
import os
import aiohttp
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

PREDICTIONS_FILE = 'database/wc_predictions.json'
CACHE_FILE = 'database/wc_match_cache.json'
API_BASE = 'https://api.football-data.org/v4'
COMPETITION = 'WC'
NZ_TZ = ZoneInfo('Pacific/Auckland')


def _load_json(path, default):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def _save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def load_predictions():
    return _load_json(PREDICTIONS_FILE, [])


def save_predictions(predictions):
    _save_json(PREDICTIONS_FILE, predictions)


def load_cache():
    return _load_json(CACHE_FILE, {})


def save_cache(cache):
    _save_json(CACHE_FILE, cache)


def get_api_key():
    return os.environ.get('FOOTBALL_API_KEY')


# ISO alpha-2 country code → team name as used by football-data.org
FLAG_TO_TEAM = {
    # CONCACAF
    'US': 'United States', 'CA': 'Canada', 'MX': 'Mexico',
    'HN': 'Honduras', 'PA': 'Panama', 'JM': 'Jamaica',
    'CR': 'Costa Rica', 'GT': 'Guatemala', 'SV': 'El Salvador',
    'TT': 'Trinidad and Tobago', 'CU': 'Cuba', 'HT': 'Haiti',
    # CONMEBOL
    'BR': 'Brazil', 'AR': 'Argentina', 'UY': 'Uruguay',
    'CO': 'Colombia', 'EC': 'Ecuador', 'VE': 'Venezuela',
    'PE': 'Peru', 'CL': 'Chile', 'PY': 'Paraguay', 'BO': 'Bolivia',
    # UEFA
    'FR': 'France', 'ES': 'Spain', 'DE': 'Germany', 'PT': 'Portugal',
    'IT': 'Italy', 'NL': 'Netherlands', 'BE': 'Belgium', 'HR': 'Croatia',
    'CH': 'Switzerland', 'PL': 'Poland', 'AT': 'Austria', 'DK': 'Denmark',
    'RS': 'Serbia', 'SE': 'Sweden', 'NO': 'Norway', 'CZ': 'Czechia',
    'HU': 'Hungary', 'SK': 'Slovakia', 'TR': 'Türkiye', 'AL': 'Albania',
    'UA': 'Ukraine', 'SI': 'Slovenia', 'RO': 'Romania', 'GR': 'Greece',
    'FI': 'Finland', 'IE': 'Republic of Ireland', 'IS': 'Iceland',
    'ME': 'Montenegro', 'MK': 'North Macedonia', 'BA': 'Bosnia-Herzegovina',
    'GE': 'Georgia', 'AZ': 'Azerbaijan', 'AM': 'Armenia',
    # Note: England/Scotland/Wales use subdivision emojis (🏴), not standard ISO flags
    'GB': 'England',
    # Africa
    'MA': 'Morocco', 'SN': 'Senegal', 'NG': 'Nigeria', 'CM': 'Cameroon',
    'EG': 'Egypt', 'GH': 'Ghana', 'CI': "Côte d'Ivoire", 'ZA': 'South Africa',
    'TN': 'Tunisia', 'DZ': 'Algeria', 'ML': 'Mali', 'CD': 'DR Congo',
    'MZ': 'Mozambique', 'ZM': 'Zambia', 'UG': 'Uganda', 'KE': 'Kenya',
    'ET': 'Ethiopia', 'TZ': 'Tanzania', 'AO': 'Angola', 'BF': 'Burkina Faso',
    'GN': 'Guinea', 'BJ': 'Benin', 'GA': 'Gabon', 'MR': 'Mauritania',
    'LY': 'Libya', 'SD': 'Sudan', 'CF': 'Central African Republic',
    # Asia / AFC
    'JP': 'Japan', 'KR': 'Korea Republic', 'IR': 'Iran', 'AU': 'Australia',
    'SA': 'Saudi Arabia', 'QA': 'Qatar', 'IQ': 'Iraq', 'JO': 'Jordan',
    'OM': 'Oman', 'AE': 'United Arab Emirates', 'KW': 'Kuwait', 'BH': 'Bahrain',
    'UZ': 'Uzbekistan', 'KZ': 'Kazakhstan', 'CN': 'China PR', 'IN': 'India',
    'TH': 'Thailand', 'VN': 'Vietnam', 'ID': 'Indonesia', 'MY': 'Malaysia',
    'SG': 'Singapore', 'PH': 'Philippines',
    # OFC
    'NZ': 'New Zealand', 'FJ': 'Fiji', 'PG': 'Papua New Guinea',
    # Other
    'RU': 'Russia', 'IL': 'Israel',
}


def _is_flag_emoji(text):
    """Return True if text is a standard two-letter regional indicator flag emoji."""
    chars = list(text)
    if len(chars) < 2:
        return False
    return all(0x1F1E6 <= ord(c) <= 0x1F1FF for c in chars[:2])


def flag_emoji_to_code(emoji):
    """Convert a regional indicator flag emoji (e.g. 🇳🇿) to its ISO alpha-2 code (e.g. 'NZ')."""
    chars = list(emoji)
    if len(chars) < 2:
        return None
    try:
        c1 = ord(chars[0]) - 0x1F1E6
        c2 = ord(chars[1]) - 0x1F1E6
        if 0 <= c1 <= 25 and 0 <= c2 <= 25:
            return chr(ord('A') + c1) + chr(ord('A') + c2)
    except Exception:
        pass
    return None


def _teams_match(api_name, lookup_name):
    """Fuzzy team name match — handles 'Korea Republic' vs 'South Korea', etc."""
    a, b = api_name.lower(), lookup_name.lower()
    return a == b or b in a or a in b


async def _find_match_by_teams(session, api_key, home_name, away_name):
    """
    Search all WC fixtures for a match containing both teams.
    Returns (match, swapped) where swapped=True means home/away are reversed vs the API fixture.
    """
    matches = await fetch_competition_matches(session, api_key)
    if not matches:
        return None, False
    for match in matches:
        ah = match['homeTeam']['name']
        aa = match['awayTeam']['name']
        if _teams_match(ah, home_name) and _teams_match(aa, away_name):
            return match, False
        if _teams_match(ah, away_name) and _teams_match(aa, home_name):
            return match, True
    return None, False


def _parse_score(score_str):
    """Parse 'X-Y' into (home_int, away_int) or raise ValueError."""
    parts = score_str.split('-')
    if len(parts) != 2:
        raise ValueError
    return int(parts[0]), int(parts[1])


def calculate_points(pred_home, pred_away, actual_home, actual_away):
    if pred_home == actual_home and pred_away == actual_away:
        return 2
    pred_result = 'H' if pred_home > pred_away else ('A' if pred_home < pred_away else 'D')
    actual_result = 'H' if actual_home > actual_away else ('A' if actual_home < actual_away else 'D')
    return 1 if pred_result == actual_result else 0


async def fetch_match_data(session, match_id, api_key):
    url = f'{API_BASE}/matches/{match_id}'
    async with session.get(url, headers={'X-Auth-Token': api_key}) as resp:
        if resp.status == 200:
            return await resp.json()
        return None


async def fetch_competition_matches(session, api_key, date_from=None, date_to=None, status=None):
    url = f'{API_BASE}/competitions/{COMPETITION}/matches'
    params = {}
    if date_from:
        params['dateFrom'] = date_from
    if date_to:
        params['dateTo'] = date_to
    if status:
        params['status'] = status
    async with session.get(url, headers={'X-Auth-Token': api_key}, params=params) as resp:
        if resp.status == 200:
            return (await resp.json()).get('matches', [])
        return None


def _format_match_line(match):
    home = match['homeTeam']['name']
    away = match['awayTeam']['name']
    mid = match['id']
    status = match['status']
    date_str = match.get('utcDate', '')

    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00')).astimezone(NZ_TZ)
        date_display = dt.strftime('%b %d %H:%M %Z')
    except Exception:
        date_display = date_str

    if status == 'FINISHED':
        score = match.get('score', {}).get('fullTime', {})
        return f'`{mid}` **{home} {score.get("home", "?")}–{score.get("away", "?")} {away}** ✓'
    elif status in ('IN_PLAY', 'PAUSED', 'EXTRA_TIME', 'PENALTY_SHOOTOUT'):
        score = match.get('score', {}).get('currentPeriod') or match.get('score', {}).get('fullTime', {})
        return f'`{mid}` 🔴 **{home} {score.get("home", "?")}–{score.get("away", "?")} {away}** [LIVE]'
    else:
        return f'`{mid}` {home} vs {away} — {date_display}'


async def _refresh_cache_for_preds(predictions, api_key):
    cache = load_cache()
    match_ids = list(set(p['match_id'] for p in predictions))

    # One-time migration: finished entries cached before the stage field was added
    # are all group stage matches — stamp them without an API call.
    for entry in cache.values():
        if entry.get('status') == 'FINISHED' and 'stage' not in entry:
            entry['stage'] = 'GROUP_STAGE'

    async with aiohttp.ClientSession() as session:
        for mid in match_ids:
            key = str(mid)
            # Finished matches are fully resolved — skip them.
            if key in cache and cache[key]['status'] == 'FINISHED':
                continue
            match = await fetch_match_data(session, mid, api_key)
            if not match:
                continue
            entry = {
                'status': match.get('status', 'UNKNOWN'),
                'home_team': match['homeTeam']['name'],
                'away_team': match['awayTeam']['name'],
                'stage': match.get('stage', 'GROUP_STAGE'),
            }
            if match.get('status') == 'FINISHED':
                score = match.get('score', {}).get('fullTime', {})
                entry['home'] = score.get('home')
                entry['away'] = score.get('away')
            cache[key] = entry
    save_cache(cache)
    return cache


@bot.command(name='wcpredict')
async def wcpredict_cmd(ctx, *, args: str):
    """Predict a score. Usage: .wcpredict <match_id> 2-1  OR  .wcpredict 🇳🇿 🇦🇺 2-1"""
    api_key = get_api_key()
    if not api_key:
        await ctx.send('No API key set. Add `FOOTBALL_API_KEY` to your environment variables.')
        return

    parts = args.strip().split()

    # --- Resolve match and intended home/away scores ---
    match = None
    home_score = away_score = None
    swapped = False  # whether the user's flag order was reversed vs the API fixture

    if len(parts) == 2 and parts[0].lstrip('-').isdigit():
        # Mode 1: .wcpredict <match_id> <score>
        try:
            match_id = int(parts[0])
            home_score, away_score = _parse_score(parts[1])
        except ValueError:
            await ctx.send('Usage: `.wcpredict <match_id> <home>-<away>`, e.g. `.wcpredict 508018 2-1`')
            return
        async with aiohttp.ClientSession() as session:
            match = await fetch_match_data(session, match_id, api_key)
        if not match:
            await ctx.send(f'Match `{match_id}` not found. Use `.wcmatches` to see upcoming matches.')
            return

    elif len(parts) == 3 and _is_flag_emoji(parts[0]) and _is_flag_emoji(parts[1]):
        # Mode 2: .wcpredict 🇳🇿 🇦🇺 <score>
        home_code = flag_emoji_to_code(parts[0])
        away_code = flag_emoji_to_code(parts[1])
        home_name = FLAG_TO_TEAM.get(home_code) if home_code else None
        away_name = FLAG_TO_TEAM.get(away_code) if away_code else None

        if not home_name or not away_name:
            unknown = parts[0] if not home_name else parts[1]
            await ctx.send(
                f"Unknown flag {unknown} (code: `{home_code or away_code}`). "
                "Try `.wcpredict <match_id> <score>` instead — run `.wcmatches` to get IDs."
            )
            return

        try:
            home_score, away_score = _parse_score(parts[2])
        except ValueError:
            await ctx.send('Invalid score format. Use `<home>-<away>`, e.g. `2-1`')
            return

        async with aiohttp.ClientSession() as session:
            match, swapped = await _find_match_by_teams(session, api_key, home_name, away_name)

        if not match:
            await ctx.send(
                f'No scheduled match found between {parts[0]} and {parts[1]}. '
                'Run `.wcmatches` to check available fixtures.'
            )
            return

        # If the API has them in the opposite order, flip the stored score
        if swapped:
            home_score, away_score = away_score, home_score

    else:
        await ctx.send(
            'Usage:\n'
            '• `.wcpredict <match_id> <home>-<away>` — e.g. `.wcpredict 508018 2-1`\n'
            '• `.wcpredict 🇳🇿 🇦🇺 <home>-<away>` — e.g. `.wcpredict 🇳🇿 🇦🇺 2-1`\n'
            'Run `.wcmatches` to see upcoming fixtures and their IDs.'
        )
        return

    if home_score < 0 or away_score < 0:
        await ctx.send('Scores cannot be negative.')
        return

    status = match.get('status', '')
    if status in ('IN_PLAY', 'PAUSED', 'EXTRA_TIME', 'PENALTY_SHOOTOUT', 'FINISHED'):
        await ctx.send('Predictions are locked — that match has already started or finished.')
        return

    match_id = match['id']
    home_team = match['homeTeam']['name']
    away_team = match['awayTeam']['name']
    # Display score in the user's intended direction (pre-swap)
    display_home, display_away = (away_score, home_score) if swapped else (home_score, away_score)
    user_home_flag = parts[0] if _is_flag_emoji(parts[0]) else home_team
    user_away_flag = parts[1] if len(parts) == 3 and _is_flag_emoji(parts[1]) else away_team

    predictions = load_predictions()
    user_id = str(ctx.author.id)
    username = ctx.author.display_name

    existing = next((p for p in predictions if p['user_id'] == user_id and p['match_id'] == match_id), None)
    if existing:
        old = f"{existing['home_score']}-{existing['away_score']}"
        existing.update({'home_score': home_score, 'away_score': away_score, 'username': username,
                         'submitted_at': datetime.now(timezone.utc).isoformat()})
        save_predictions(predictions)
        await ctx.send(
            f'Updated: **{home_team} vs {away_team}** — {old} → **{home_score}-{away_score}**\n'
            f'*(your pick: {user_home_flag} {display_home}–{display_away} {user_away_flag})* ✅'
        )
    else:
        predictions.append({
            'user_id': user_id,
            'username': username,
            'match_id': match_id,
            'home_score': home_score,
            'away_score': away_score,
            'submitted_at': datetime.now(timezone.utc).isoformat(),
        })
        save_predictions(predictions)
        await ctx.send(
            f'Prediction saved: **{home_team} vs {away_team}**\n'
            f'*(your pick: {user_home_flag} {display_home}–{display_away} {user_away_flag})* ✅'
        )


@bot.command(name='wcmatches')
async def wcmatches_cmd(ctx, filter_arg: str = 'upcoming'):
    """Show World Cup matches. Usage: .wcmatches [live|recent]"""
    api_key = get_api_key()
    if not api_key:
        await ctx.send('No API key set. Add `FOOTBALL_API_KEY` to your environment variables.')
        return

    now_nz = datetime.now(NZ_TZ)
    status_filter = None
    date_from = None
    date_to = None

    if filter_arg == 'live':
        status_filter = 'IN_PLAY'
    elif filter_arg == 'recent':
        date_from = (now_nz - timedelta(days=3)).strftime('%Y-%m-%d')
        date_to = now_nz.strftime('%Y-%m-%d')
    else:
        date_from = now_nz.strftime('%Y-%m-%d')
        date_to = (now_nz + timedelta(days=1)).strftime('%Y-%m-%d')

    async with aiohttp.ClientSession() as session:
        matches = await fetch_competition_matches(session, api_key, date_from, date_to, status_filter)

    if matches is None:
        await ctx.send('Failed to fetch matches — check your API key or try again later.')
        return
    if not matches:
        await ctx.send(f'No {filter_arg} matches found.')
        return

    lines = [_format_match_line(m) for m in matches[:15]]
    label = 'Today & Tomorrow' if filter_arg == 'upcoming' else filter_arg.title()
    embed = discord.Embed(
        title=f'World Cup 2026 — {label} Matches',
        description='\n'.join(lines),
        color=0x1a6b3c,
    )
    embed.set_footer(text='Predict: .wcpredict 🇳🇿 🇦🇺 2-1  or  .wcpredict <match_id> 2-1')
    await ctx.send(embed=embed)


@bot.command(name='wcleaderboard')
async def wcleaderboard_cmd(ctx):
    """Show the World Cup fantasy league leaderboard."""
    api_key = get_api_key()
    if not api_key:
        await ctx.send('No API key set. Add `FOOTBALL_API_KEY` to your environment variables.')
        return

    predictions = load_predictions()
    if not predictions:
        await ctx.send('No predictions yet! Use `.wcpredict <match_id> <score>` to get started.')
        return

    async with ctx.typing():
        cache = await _refresh_cache_for_preds(predictions, api_key)

    scores = {}
    for pred in predictions:
        uid = pred['user_id']
        uname = pred.get('username', f'User {uid}')
        mid = str(pred['match_id'])

        if uid not in scores:
            scores[uid] = {'username': uname, 'points': 0, 'exact': 0, 'result': 0, 'pending': 0}

        if mid in cache and cache[mid]['status'] == 'FINISHED':
            pts = calculate_points(
                pred['home_score'], pred['away_score'],
                cache[mid]['home'], cache[mid]['away'],
            )
            scores[uid]['points'] += pts
            if pts == 2:
                scores[uid]['exact'] += 1
            elif pts == 1:
                scores[uid]['result'] += 1
        else:
            scores[uid]['pending'] += 1

    sorted_scores = sorted(scores.values(), key=lambda x: x['points'], reverse=True)
    medals = ['🥇', '🥈', '🥉']
    lines = []
    for i, s in enumerate(sorted_scores[:10]):
        rank = medals[i] if i < 3 else f'**{i + 1}.**'
        pending = f' (+{s["pending"]} pending)' if s['pending'] else ''
        lines.append(
            f'{rank} **{s["username"]}** — {s["points"]} pts'
            f' ({s["exact"]}🎯 {s["result"]}✅{pending})'
        )

    embed = discord.Embed(
        title='World Cup 2026 — Fantasy Leaderboard',
        description='\n'.join(lines),
        color=0xf4c300,
    )
    embed.set_footer(text='🎯 exact score = 2pts  •  ✅ correct result = 1pt')
    await ctx.send(embed=embed)


@bot.command(name='mypicks')
async def mypicks_cmd(ctx):
    """Show your World Cup predictions and current points."""
    api_key = get_api_key()
    if not api_key:
        await ctx.send('No API key set. Add `FOOTBALL_API_KEY` to your environment variables.')
        return

    user_id = str(ctx.author.id)
    user_preds = [p for p in load_predictions() if p['user_id'] == user_id]
    if not user_preds:
        await ctx.send("You haven't made any predictions yet. Use `.wcpredict <match_id> <home>-<away>`!")
        return

    async with ctx.typing():
        cache = await _refresh_cache_for_preds(user_preds, api_key)

    total = 0
    group_count = group_pts = group_exact = group_result = group_pending = 0
    knockout_lines = []

    for pred in user_preds:
        mid = str(pred['match_id'])
        pred_score = f"{pred['home_score']}-{pred['away_score']}"
        entry = cache.get(mid, {})
        is_group = entry.get('stage', 'GROUP_STAGE') == 'GROUP_STAGE'
        home_team = entry.get('home_team', f'Match {mid}')
        away_team = entry.get('away_team', '')

        if is_group:
            group_count += 1

        if entry.get('status') == 'FINISHED':
            ah, aa = entry['home'], entry['away']
            pts = calculate_points(pred['home_score'], pred['away_score'], ah, aa)
            total += pts
            if is_group:
                group_pts += pts
                if pts == 2:
                    group_exact += 1
                elif pts == 1:
                    group_result += 1
            else:
                icon = '🎯' if pts == 2 else ('✅' if pts == 1 else '❌')
                knockout_lines.append(f'{icon} **{home_team} vs {away_team}** — pred: {pred_score} | actual: {ah}-{aa} | **{pts}pt**')
        else:
            status_label = entry.get('status', 'UNKNOWN')
            if is_group:
                group_pending += 1
            else:
                knockout_lines.append(f'⏳ **{home_team} vs {away_team}** — pred: {pred_score} | [{status_label}]')

    embed = discord.Embed(
        title=f"{ctx.author.display_name}'s World Cup Picks",
        color=0x3498db,
    )

    if group_count:
        group_summary = f'{group_pts} pts — {group_exact}🎯 {group_result}✅'
        if group_pending:
            group_summary += f' • {group_pending} pending'
        embed.add_field(name=f'Group Stage ({group_count} predictions)', value=group_summary, inline=False)

    if knockout_lines:
        embed.add_field(name='Knockout Stage', value='\n'.join(knockout_lines), inline=False)

    if not group_count and not knockout_lines:
        embed.description = 'No predictions yet.'

    embed.set_footer(text=f'Total: {total} pts  •  🎯 exact (2pt)  ✅ result (1pt)  ❌ miss (0pt)')
    await ctx.send(embed=embed)


@bot.command(name='wchelp')
async def wchelp_cmd(ctx):
    """Show World Cup fantasy league commands."""
    embed = discord.Embed(
        title='World Cup 2026 — Fantasy League',
        description='Predict match scores before kick-off and earn points!',
        color=0x1a6b3c,
    )
    embed.add_field(
        name='Scoring',
        value='🎯 **2 points** — Exact scoreline correct\n✅ **1 point** — Correct result (win/draw/loss)\n❌ **0 points** — Wrong result',
        inline=False,
    )
    embed.add_field(
        name='Commands',
        value=(
            '`.wcmatches` — Today & tomorrow\'s matches (NZ time)\n'
            '`.wcmatches live` — Live matches right now\n'
            '`.wcmatches recent` — Last 3 days of results\n'
            '`.wcpredict <id> <score>` — Submit or update a prediction\n'
            '`.mypicks` — Your predictions with current points\n'
            '`.wcleaderboard` — Full leaderboard'
        ),
        inline=False,
    )
    embed.add_field(
        name='Examples',
        value=(
            '`.wcpredict 508018 2-1` — by match ID (from `.wcmatches`)\n'
            '`.wcpredict 🇳🇿 🇦🇺 2-1` — by flag emoji (home flag first)\n'
            'Both formats accept `:flag_nz:` style Discord shortcodes.'
        ),
        inline=False,
    )
    embed.set_footer(text='Requires FOOTBALL_API_KEY env var (football-data.org)')
    await ctx.send(embed=embed)
