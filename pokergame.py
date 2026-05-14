import discord
from main import bot
from helper.poker import PokerGame, card_display

# One game per channel: {channel_id: PokerGame}
_games = {}


def _status_embed(game):
    phase_label = game.phase.replace('-', ' ').title()
    embed = discord.Embed(title=f"Texas Hold'em — {phase_label}", color=0x2ecc71)

    if game.community_cards:
        community = ' '.join(card_display(c) for c in game.community_cards)
        embed.add_field(name="Community Cards", value=community, inline=False)

    embed.add_field(name="Pot", value=f"${game.pot}", inline=True)
    if game.current_bet > 0:
        embed.add_field(name="Current Bet", value=f"${game.current_bet}", inline=True)

    lines = []
    for pid in game.players:
        name = game.names[pid]
        chips = game.balances[pid]
        bet = game.round_bets.get(pid, 0)
        tags = []
        if pid in game.folded:
            tags.append("folded")
        elif pid in game.all_in:
            tags.append("ALL IN")
        bet_str = f" | bet ${bet}" if bet > 0 else ""
        tag_str = f" ({', '.join(tags)})" if tags else ""
        lines.append(f"{name}: ${chips}{bet_str}{tag_str}")
    embed.add_field(name="Players", value='\n'.join(lines), inline=False)

    current = game.current_player()
    if current:
        owed = game.current_bet - game.round_bets.get(current, 0)
        actions = "`.fold` `.check`" if owed == 0 else f"`.fold` `.call` (${owed})"
        actions += " `.raise <amount>` `.allin`"
        embed.add_field(name=f"Turn: {game.names[current]}", value=actions, inline=False)

    return embed


async def _after_action(ctx, ok, msg, game):
    if not ok:
        await ctx.send(f"{ctx.author.display_name}: {msg}")
        return

    await ctx.send(msg)

    if len(game.active_players()) == 1:
        await _finish_hand(ctx, game)
        return

    while game.is_round_over():
        continues = game.advance_phase()
        if not continues:
            await _finish_hand(ctx, game)
            return
        community = ' '.join(card_display(c) for c in game.community_cards)
        await ctx.send(f"**{game.phase.title()}:** {community}")
        if game.current_player() is not None:
            break

    if game.phase not in ('showdown', 'lobby'):
        await ctx.send(embed=_status_embed(game))


async def _finish_hand(ctx, game):
    winners, hand_results = game.resolve()
    winner_names = ', '.join(game.names[w] for w in winners)

    if not hand_results:
        embed = discord.Embed(title="Hand Over", color=0xf1c40f)
        embed.add_field(name="Winner", value=f"**{winner_names}** wins the pot!", inline=False)
    else:
        embed = discord.Embed(title="Showdown!", color=0xe74c3c)
        for pid, (hand_name, best_5, _) in hand_results.items():
            hole = ' '.join(card_display(c) for c in game.hole_cards[pid])
            best = ' '.join(best_5)
            marker = " 🏆" if pid in winners else ""
            embed.add_field(
                name=f"{game.names[pid]}{marker}",
                value=f"Hole: {hole}\n**{hand_name}:** {best}",
                inline=False
            )
        embed.add_field(name="Winner(s)", value=f"**{winner_names}**", inline=False)

    await ctx.send(embed=embed)

    balance_lines = [f"{game.names[p]}: ${game.balances[p]}" for p in game.players]
    await ctx.send("**Chip counts after hand:**\n" + '\n'.join(balance_lines))

    broke = [p for p in list(game.players) if game.balances[p] == 0]
    if broke:
        broke_names = ', '.join(game.names[p] for p in broke)
        await ctx.send(f"{broke_names} {'is' if len(broke) == 1 else 'are'} out of chips and eliminated!")
        for p in broke:
            game.players.remove(p)
            del game.names[p]
            del game.balances[p]

    if len(game.players) < 2:
        if game.players:
            last = game.players[0]
            await ctx.send(f"**{game.names[last]}** wins the game! Use `.poker` to start a new one.")
        del _games[ctx.channel.id]
        return

    await ctx.send("Use `.deal` to start the next hand.")


@bot.command(name='poker')
async def poker_cmd(ctx):
    """Create a new poker game in this channel."""
    cid = ctx.channel.id
    if cid in _games:
        await ctx.send("A game is already running here. Use `.join` to join, or `.endpoker` to cancel it.")
        return
    game = PokerGame(ctx.author.id, ctx.author.display_name)
    _games[cid] = game
    embed = discord.Embed(
        title="New Texas Hold'em Game",
        description=(
            f"**{ctx.author.display_name}** has started a poker game!\n\n"
            "Others: use `.join` to join.\n"
            f"Host: use `.deal` when everyone is ready."
        ),
        color=0x3498db
    )
    embed.add_field(name="Starting Chips", value=f"${PokerGame.STARTING_CHIPS} per player")
    embed.add_field(name="Blinds", value=f"Small ${PokerGame.SMALL_BLIND} | Big ${PokerGame.BIG_BLIND}")
    await ctx.send(embed=embed)


@bot.command(name='join')
async def join_cmd(ctx):
    """Join the poker game in this channel."""
    cid = ctx.channel.id
    if cid not in _games:
        await ctx.send("No poker game here. Start one with `.poker`.")
        return
    game = _games[cid]
    if game.phase != 'lobby':
        await ctx.send("The hand has already started. Wait for the next hand.")
        return
    ok, msg = game.add_player(ctx.author.id, ctx.author.display_name)
    await ctx.send(msg)
    if ok:
        names = ', '.join(game.names[p] for p in game.players)
        await ctx.send(f"Players ({len(game.players)}): {names}")


@bot.command(name='deal')
async def deal_cmd(ctx):
    """Deal hole cards and start the hand (host only)."""
    cid = ctx.channel.id
    if cid not in _games:
        await ctx.send("No poker game here. Start one with `.poker`.")
        return
    game = _games[cid]
    if game.phase != 'lobby':
        await ctx.send("A hand is already in progress.")
        return
    ok, msg = game.start_game(ctx.author.id)
    if not ok:
        await ctx.send(msg)
        return

    dm_fails = []
    for pid in game.players:
        member = ctx.guild.get_member(pid)
        if member:
            hand = ' '.join(card_display(c) for c in game.hole_cards[pid])
            try:
                await member.send(f"Your hole cards for the game in **#{ctx.channel.name}**:\n**{hand}**")
            except discord.Forbidden:
                dm_fails.append(game.names[pid])

    if dm_fails:
        await ctx.send(
            f"Could not DM hole cards to: {', '.join(dm_fails)}. "
            "They need to enable DMs from server members. Use `.hand` to retry."
        )

    n = len(game.players)
    sb_name = game.names[game.players[(game.dealer_idx + 1) % n]]
    bb_name = game.names[game.players[(game.dealer_idx + 2) % n]]
    dealer_name = game.names[game.players[game.dealer_idx]]
    await ctx.send(
        f"Cards dealt! Dealer: **{dealer_name}** | "
        f"Small blind: **{sb_name}** (${PokerGame.SMALL_BLIND}) | "
        f"Big blind: **{bb_name}** (${PokerGame.BIG_BLIND})"
    )
    await ctx.send(embed=_status_embed(game))


@bot.command(name='hand')
async def hand_cmd(ctx):
    """Re-send your hole cards via DM."""
    cid = ctx.channel.id
    if cid not in _games:
        return
    game = _games[cid]
    uid = ctx.author.id
    if uid not in game.players or uid not in game.hole_cards:
        await ctx.send("You're not in the current hand.")
        return
    hand = ' '.join(card_display(c) for c in game.hole_cards[uid])
    try:
        await ctx.author.send(f"Your hole cards: **{hand}**")
        await ctx.send(f"Sent your cards via DM, {ctx.author.display_name}!")
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.display_name}: Please enable DMs from server members.")


@bot.command(name='fold')
async def fold_cmd(ctx):
    cid = ctx.channel.id
    if cid not in _games:
        return
    game = _games[cid]
    if ctx.author.id not in game.players:
        return
    ok, msg = game.do_fold(ctx.author.id)
    await _after_action(ctx, ok, msg, game)


@bot.command(name='check')
async def check_cmd(ctx):
    cid = ctx.channel.id
    if cid not in _games:
        return
    game = _games[cid]
    if ctx.author.id not in game.players:
        return
    ok, msg = game.do_check(ctx.author.id)
    await _after_action(ctx, ok, msg, game)


@bot.command(name='call')
async def call_cmd(ctx):
    cid = ctx.channel.id
    if cid not in _games:
        return
    game = _games[cid]
    if ctx.author.id not in game.players:
        return
    ok, msg = game.do_call(ctx.author.id)
    await _after_action(ctx, ok, msg, game)


@bot.command(name='raise', aliases=['bet'])
async def raise_cmd(ctx, amount: int):
    cid = ctx.channel.id
    if cid not in _games:
        return
    game = _games[cid]
    if ctx.author.id not in game.players:
        return
    ok, msg = game.do_raise(ctx.author.id, amount)
    await _after_action(ctx, ok, msg, game)


@bot.command(name='allin')
async def allin_cmd(ctx):
    cid = ctx.channel.id
    if cid not in _games:
        return
    game = _games[cid]
    if ctx.author.id not in game.players:
        return
    ok, msg = game.do_allin(ctx.author.id)
    await _after_action(ctx, ok, msg, game)


@bot.command(name='pokerstatus')
async def pokerstatus_cmd(ctx):
    """Show the current game state."""
    cid = ctx.channel.id
    if cid not in _games:
        await ctx.send("No active poker game in this channel.")
        return
    await ctx.send(embed=_status_embed(_games[cid]))


@bot.command(name='leave')
async def leave_cmd(ctx):
    """Leave the poker game (lobby only)."""
    cid = ctx.channel.id
    if cid not in _games:
        return
    game = _games[cid]
    uid = ctx.author.id
    if uid not in game.players:
        await ctx.send("You're not in this game.")
        return
    if game.phase != 'lobby':
        await ctx.send("Can't leave mid-hand. Wait for the hand to end.")
        return
    name = game.names[uid]
    chips = game.balances[uid]
    game.players.remove(uid)
    del game.names[uid]
    del game.balances[uid]
    await ctx.send(f"**{name}** left the game with ${chips} chips.")
    if not game.players:
        del _games[cid]
        await ctx.send("No players left. Game ended.")
    elif uid == game.host_id:
        game.host_id = game.players[0]
        await ctx.send(f"**{game.names[game.host_id]}** is now the host.")


@bot.command(name='endpoker')
async def endpoker_cmd(ctx):
    """End and cancel the poker game (host only)."""
    cid = ctx.channel.id
    if cid not in _games:
        await ctx.send("No active poker game in this channel.")
        return
    game = _games[cid]
    if ctx.author.id != game.host_id:
        await ctx.send("Only the host can end the game.")
        return
    del _games[cid]
    await ctx.send("Poker game ended.")


@bot.command(name='pokerhelp')
async def pokerhelp_cmd(ctx):
    """Show all poker commands."""
    embed = discord.Embed(
        title="Texas Hold'em — Command Reference",
        description=(
            "The bot acts as dealer. Hole cards are sent to you via DM.\n"
            f"Each player starts with **${PokerGame.STARTING_CHIPS} chips**. "
            f"Blinds: small **${PokerGame.SMALL_BLIND}** / big **${PokerGame.BIG_BLIND}**."
        ),
        color=0x3498db
    )

    embed.add_field(
        name="Setup",
        value=(
            "`.poker` — Create a new game in this channel\n"
            "`.join` — Join the waiting game\n"
            "`.deal` — **(Host)** Deal hole cards and start the hand\n"
            "`.leave` — Leave the game (lobby only)\n"
            "`.endpoker` — **(Host)** Cancel and end the game"
        ),
        inline=False
    )

    embed.add_field(
        name="During a Hand",
        value=(
            "`.fold` — Discard your hand and forfeit the round\n"
            "`.check` — Pass the action (only when no bet is owed)\n"
            "`.call` — Match the current bet\n"
            "`.raise <amount>` — Raise by an amount on top of the call (min $20)\n"
            "`.bet <amount>` — Same as `.raise`\n"
            "`.allin` — Bet all your remaining chips"
        ),
        inline=False
    )

    embed.add_field(
        name="Info",
        value=(
            "`.hand` — Re-send your hole cards via DM\n"
            "`.pokerstatus` — Show the current game state and chip counts"
        ),
        inline=False
    )

    embed.add_field(
        name="Hand Rankings (best to worst)",
        value=(
            "1. Royal Flush — A K Q J 10 of the same suit\n"
            "2. Straight Flush — Five consecutive cards, same suit\n"
            "3. Four of a Kind — Four cards of the same rank\n"
            "4. Full House — Three of a kind + a pair\n"
            "5. Flush — Five cards of the same suit\n"
            "6. Straight — Five consecutive cards\n"
            "7. Three of a Kind — Three cards of the same rank\n"
            "8. Two Pair — Two different pairs\n"
            "9. One Pair — Two cards of the same rank\n"
            "10. High Card — Highest card wins"
        ),
        inline=False
    )

    await ctx.send(embed=embed)
