```markdown
# PandOS — Commands Reference (English)

This file documents the commands implemented in PandOS.py and explains how to use them.  
Commands are grouped by category. For each command you will find: description, usage, required permissions (if any), aliases, and examples.

Note: Prefix used by the bot in the code is `$`. Replace `$` with your server's prefix if different.

------------------------------------------------------------------------------------------------------------------------

## Table of Contents
- Economy & Currency
- Gambling & Games
- Shop & Inventory
- XP / Leveling / Leaderboards
- Verification & Welcome
- Moderation & Warnings
- Administration & Utility
- Teams & Community
- Fun / Social
- Integration / Misc

------------------------------------------------------------------------------------------------------------------------

## Economy & Currency

### pandocoin (aliases: pcoin)
- Description: Shows the current exchange rate of PandoCoin and a graph of historical rates.
- Usage: `$pandocoin`
- Permissions: none
- Example: `$pcoin`

### exchange
- Description: Exchange PanDollars ($P) from your balance into PandoCoin at current rate.
- Usage: `$exchange <amount>`
- Parameters:
  - `<amount>` — amount of $P to exchange (float allowed)
- Permissions: none
- Example: `$exchange 100`

### setrate
- Description: (Admin) Set a new exchange rate for PandoCoin manually.
- Usage: `$setrate <new_rate>`
- Parameters:
  - `<new_rate>` — integer or number representing the new rate
- Permissions: Administrator
- Example: `$setrate 500`

### givepando
- Description: (Admin) Give PandoCoin to a specified user.
- Usage: `$givepando @user <amount>`
- Parameters:
  - `@user` — mention of the user
  - `<amount>` — integer amount of PandoCoin to give
- Permissions: Administrator
- Example: `$givepando @SomeUser 5`

### buyrank
- Description: Buy a server rank (role) using PandoCoin.
- Usage: `$buyrank <rank_name>`
- Parameters:
  - `<rank_name>` — one of the ranks available (e.g., VIP, Megalodon, Crypto King)
- Permissions: none
- Example: `$buyrank VIP`

### ranks
- Description: Shows the available ranks and their prices in PandoCoin.
- Usage: `$ranks`
- Permissions: none
- Example: `$ranks`

------------------------------------------------------------------------------------------------------------------------

## Gambling & Games

### gambling (aliases: gam)
- Description: Central command for various gambling games (jackpot, double, safe, risky, roulette, russianroulette).
- Usage: `$gambling <game_name> [args]`
- Games supported:
  - `jackpot` — 10% chance to win 6x your bet
  - `double` — 45% chance to double your bet
  - `safe` — 65% chance to win 1.3x your bet
  - `risky` — 25% chance to win 3.5x your bet
  - `roulette` — choose a color and bet (see below)
  - `russianroulette` — bet all your balance, 50/50 chance to double or lose everything
- Permissions: none
- Examples:
  - `$gambling double 100`
  - `$gambling jackpot 50`
  - `$gambling roulette red 200`
  - `$gambling russianroulette`

Notes:
- The command updates user balance depending on outcome.
- For `roulette`, valid colors: red, black, green, white.

### rob
- Description: Attempt to rob another user. 10% of target's balance is stolen on success. There is a 24-hour cooldown between robberies for the same robber.
- Usage: `$rob @target_user`
- Parameters:
  - `@target_user` — user mention to rob
- Permissions: none
- Example: `$rob @Victim123`

Notes:
- If target has active protection, robbery is blocked.
- Failed robbery penalizes the robber (loses a portion of his balance) and increments failed attempts.

### robbank (aliases: robberybank)
- Description: Attempt to rob the bank. Success chance ~30% (randomized), rewards or losses fixed range.
- Usage: `$robbank`
- Permissions: none
- Example: `$robbank`

### work
- Description: Work to earn $P. Has a cooldown (6 hours).
- Usage: `$work`
- Permissions: none
- Example: `$work`

### jackpot / double / safe / risky
- These are not separate commands; they are subgames under `$gambling`. Use `$gambling <game> <amount>`.

------------------------------------------------------------------------------------------------------------------------

## Shop & Inventory

### shop
- Description: Browse shop categories (Houses, Cars, Clothes, Luxury Items, Travel). View items and prices.
- Usage:
  - `$shop` — shows available categories
  - `$shop <category>` — shows items in the chosen category (use the category name or a part of it)
- Permissions: none
- Examples:
  - `$shop`
  - `$shop houses`
  - `$shop cars`

### buy
- Description: Purchase an item from the shop with your $P balance. The command searches for a matching item name in the catalogue.
- Usage: `$buy <item_name>`
- Parameters:
  - `<item_name>` — the name (or part of the name) of the item you want to purchase
- Permissions: none
- Example: `$buy Tesla Model S`

Notes:
- The bot checks your balance and deducts price if you have enough funds; purchased item is added to your inventory.

### inventory (aliases: inv)
- Description: Show your inventory (items owned, PandoCoin in inventory, and protection status/time remaining).
- Usage: `$inventory` or `$inv`
- Permissions: none
- Example: `$inv`

### buyprotection
- Description: Buy protection to prevent being robbed for a chosen duration.
- Usage: `$buyprotection <time_period>`
- Valid periods and prices:
  - `1h` — 10,000 $P
  - `24h` — 50,000 $P
  - `7d` — 250,000 $P
  - `30d` — 1,000,000 $P
- Permissions: none
- Example: `$buyprotection 24h`

------------------------------------------------------------------------------------------------------------------------

## XP / Leveling / Leaderboards

### lvl
- Description: Show a user's level and XP progress.
- Usage: `$lvl [@user]`
- Parameters:
  - `@user` — optional; if omitted, shows your own stats
- Permissions: none
- Example: `$lvl @User123` or `$lvl`

### toplvl (aliases: topl)
- Description: Show top 10 users by level and XP on the server.
- Usage: `$toplvl` or `$topl`
- Permissions: none
- Example: `$toplvl`

Notes:
- XP is earned from messages and voice activity. There is a per-message cooldown for XP awarding.

------------------------------------------------------------------------------------------------------------------------

## Verification & Welcome

### Verify flow (commands & behavior)
- New users without the verify role will have messages removed and will get a private verification channel created for them.
- The standard manual verification command is:

### start
- Description: Submit your verification code to complete verification after accepting rules in the verification channel.
- Usage: `$start <code>`
- Parameters:
  - `<code>` — the 10-character verification code provided in your verification channel/DM
- Permissions: none (used by the user undergoing verification)
- Example: `$start Abc123XyZ9`

Notes:
- Users must react ✅ to the rules message in the verification channel before using `$start`.
- After successful verification, the VERIFY_ROLE is added and the verification channel is deleted (if possible).

### twm (test welcome message)
- Description: Admin-only test command to send welcome message DM to the invoker (used to preview welcome DM).
- Usage: `$twm`
- Permissions: Administrator
- Example: `$twm`

------------------------------------------------------------------------------------------------------------------------

## Moderation & Warnings

### ban
- Description: Ban a user from the guild.
- Usage: `$ban <user> [reason]`
- Parameters:
  - `<user>` — mention or ID
  - `[reason]` — optional reason text
- Permissions: `ban_members` required
- Example: `$ban @Troll123 Spamming`

### kick
- Description: Kick a user from the guild.
- Usage: `$kick <user> [reason]`
- Parameters:
  - `<user>` — mention or ID
  - `[reason]` — optional
- Permissions: `kick_members` required
- Example: `$kick @BadUser Breaking rules`

### mute
- Description: Temporarily mute a user by assigning/creating a "Muted" role and disabling send/speak; unmute occurs after duration.
- Usage: `$mute <user> <time_in_minutes> [reason]`
- Parameters:
  - `<user>` — mention of the user to mute
  - `<time_in_minutes>` — duration in minutes (integer)
  - `[reason]` — optional reason
- Permissions: `manage_roles` required
- Example: `$mute @NoisyUser 30 Spamming in chat`

### unmute
- Description: Remove the "Muted" role from a user.
- Usage: `$unmute <user>`
- Permissions: `manage_roles` required
- Example: `$unmute @NoisyUser`

### warn
- Description: Warn a user (logs the warning in a JSON file and DM the user).
- Usage: `$warn <user> [reason]`
- Parameters:
  - `<user>` — mention
  - `[reason]` — optional reason
- Permissions: `kick_members` required
- Example: `$warn @User1 Inappropriate language`

### Pwarn
- Description: Bot issues a warning in the name of PandOS (similar to warn).
- Usage: `$Pwarn <user> [reason]`
- Permissions: `kick_members` required
- Example: `$Pwarn @User2 Violation of rules`

### warnings
- Description: Show warnings (count and reasons) for a user.
- Usage: `$warnings <user>`
- Permissions: none
- Example: `$warnings @User1`

### resetwarnings
- Description: Reset a user's warnings (delete warnings record).
- Usage: `$resetwarnings <user>`
- Permissions: Administrator
- Example: `$resetwarnings @User1`

Notes:
- Warnings are stored in `warnings.json` in the bot directory.

------------------------------------------------------------------------------------------------------------------------

## Administration & Utility

### say
- Description: Send a message as the bot. (Implementation: only works if invoker matches SAY_USER_ID; also requires admin permission decorator.)
- Usage: `$say <message>`
- Permissions: Administrator (and extra check vs SAY_USER_ID in code)
- Example: `$say Server maintenance in 10 minutes.`

### announcement
- Description: (Admin) Send a DM announcement message to all server members. The bot attempts to DM each member and reports failures.
- Usage: `$announcement <message>`
- Permissions: Administrator
- Example: `$announcement Server event tonight at 20:00!`

Notes:
- This can be heavy — if many members have DMs closed, those members will be skipped.

### ping
- Description: Check bot latency.
- Usage: `$ping`
- Permissions: none
- Example: `$ping`

### uptime
- Description: Show bot uptime (computed from bot creation time in code).
- Usage: `$uptime`
- Permissions: none
- Example: `$uptime`

### serverinfo
- Description: Display server (guild) information such as name, ID, member count, creation date.
- Usage: `$serverinfo`
- Permissions: none
- Example: `$serverinfo`

### userinfo
- Description: Show detailed user information for a guild member (joined date, roles, status, activity).
- Usage: `$userinfo <user>`
- Permissions: none
- Example: `$userinfo @SomeUser`

### pvsend
- Description: (Admin) Send a private DM to a user by user ID and message text.
- Usage: `$pvsend <user_id> <message>`
- Permissions: Administrator
- Example: `$pvsend 123456789012345678 Hello from the admins!`

### clear
- Description: Delete a number of messages (1–100) in the current text channel.
- Usage: `$clear <amount>`
- Parameters:
  - `<amount>` — number of messages to delete (int)
- Permissions: Administrator (command decorated)
- Example: `$clear 25`

### bug
- Description: Submit a bug report to a specific log channel; reporter message is forwarded as an embed.
- Usage: `$bug <description>`
- Permissions: none
- Example: `$bug The /shop command shows wrong price for Tesla Model S`

### check_sales
- Description: (Admin) Manually fetch and send current Steam sales (uses Steam API fetch routine).
- Usage: `$check_sales`
- Permissions: Administrator
- Example: `$check_sales`

------------------------------------------------------------------------------------------------------------------------

## Teams & Community

### teamrank
- Description: Show team ranking leaderboard using `team_points`.
- Usage: `$teamrank`
- Permissions: none
- Example: `$teamrank`

### teamreset
- Description: (Admin) Reset all team points to zero.
- Usage: `$teamreset`
- Permissions: Administrator
- Example: `$teamreset`

### partnership_start
- Description: (Admin) Assign the Partnership Program role to a user by ID and DM them a welcome embed.
- Usage: `$partnership_start <user_id>`
- Permissions: Administrator
- Example: `$partnership_start 123456789012345678`

### partnership_end
- Description: (Admin) Remove the Partnership Program role from a user by ID and DM them a termination embed.
- Usage: `$partnership_end <user_id>`
- Permissions: Administrator
- Example: `$partnership_end 123456789012345678`

### sendrateserverinfo (command name in code)
- Description: (Admin) DM a user asking them to rate the server and provide a short friendly embed.
- Usage: `$sendrateserverinfo <user_id>`
- Permissions: Administrator
- Example: `$sendrateserverinfo 123456789012345678`

------------------------------------------------------------------------------------------------------------------------

## Fun / Social

### bonk
- Description: Send a playful "bonk" message + GIF mentioning target user.
- Usage: `$bonk <@user>`
- Permissions: none
- Example: `$bonk @Friend`

### slap
- Description: Send a slap GIF to a user.
- Usage: `$slap <@user>`
- Permissions: none
- Example: `$slap @Friend`

### hug
- Description: Send a hug GIF to a user.
- Usage: `$hug <@user>`
- Permissions: none
- Example: `$hug @Friend`

### fuck
- Description: (Crude) Send an adult-style gif/message. (Be cautious: content may be explicit.)
- Usage: `$fuck <@user>`
- Permissions: none
- Example: `$fuck @Friend`

### kill
- Description: Send a random humorous "kill" text with a gif embed.
- Usage: `$kill <@user>`
- Permissions: none
- Example: `$kill @Friend`

### ship
- Description: Calculate a random compatibility score between two users with progress bar and commentary.
- Usage: `$ship <@user1> <@user2>`
- Permissions: none
- Example: `$ship @Alice @Bob`

### simp
- Description: Random "simp" percentage for a user.
- Usage: `$simp <@user>`
- Permissions: none
- Example: `$simp @Friend`

### gooner
- Description: Random "gooner" intensity scan for a user (fun).
- Usage: `$gooner <@user>`
- Permissions: none
- Example: `$gooner @Friend`

### fullscan
- Description: Run multiple fun scans combined (gooner, simp, ship) for two users.
- Usage: `$fullscan <@user1> <@user2>`
- Permissions: none
- Example: `$fullscan @Alice @Bob`

### gooneroftheday
- Description: Select a daily "gooner" (random member) and announce it. Command has a 24-hour cooldown (persisted).
- Usage: `$gooneroftheday`
- Permissions: none
- Example: `$gooneroftheday`

------------------------------------------------------------------------------------------------------------------------

## Voice & Calls

### call
- Description: Invite a user to join your voice channel. Sends a DM to the invited user with interactive buttons (Join / Busy). If they choose "I'm joining" and they are in voice, the bot attempts to move them to the author's voice channel.
- Usage: `$call <@user>`
- Permissions: none (caller must be in a voice channel)
- Example: `$call @Gamer`

Notes:
- The view uses discord UI buttons and times out after 60 seconds.
- If the bot lacks move permissions or DMs are closed, actions may fail.

------------------------------------------------------------------------------------------------------------------------

## Integration / Misc

### send_steam_sales (task) / fetch_steam_sales
- Description: Periodic task that fetches featured categories / specials from Steam and sends embeds to a configured channel. There is also an admin command to force a check (`$check_sales`).
- Usage: Automatic (task) or `$check_sales` (admin)
- Permissions: Administrator (for manual check)

------------------------------------------------------------------------------------------------------------------------

## Help Commands

### userhelp
- Description: Show user help embed (multiple pages split into embeds with common commands).
- Usage: `$userhelp`
- Permissions: none
- Example: `$userhelp`

### adminhelp
- Description: Show admin commands help embed. Only available for administrators.
- Usage: `$adminhelp`
- Permissions: Administrator
- Example: `$adminhelp`

Notes:
- The bot also sets a custom help via `bot.help_command = UserHelpCommand()` and contains several help embeds split into parts.

------------------------------------------------------------------------------------------------------------------------

MORE ABOUT PandOS Bot: https://vezyyy.github.io/VPanda/PandOS

```
