import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Select

# ============ CONFIG ============
BOT_TOKEN = "MTQzNDUzODIwMDg1NjEzMzc0Mw.Gqrtfu.iXzScTphWhQfF2ub6D-5F_QBCLHoKRoWJ82GzM"  # ← Replace with your bot token
GETSCRIPT_CHANNEL_ID = 1433493600834158767  # ← Replace with your #getscript channel ID

# Main Monster Hub script
ALLINONE_SCRIPT = """```lua
-- Monster Hub | All-In-One Script
loadstring(game:HttpGet("https://raw.githubusercontent.com/monster-hub-lol/MonsterHub/refs/heads/main/src/allinone.lua"))()
```"""

# ============ BOT SETUP ============
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Sync failed: {e}")

# ============ SELECT MENU ============
class ScriptSelect(Select):
    def __init__(self, author_id: int):
        options = [
            discord.SelectOption(label="All-In-One", value="allinone", description="Monster Hub combined script"),
            discord.SelectOption(label="99Nights", value="99nights", description="Script currently down"),
            discord.SelectOption(label="Rivals", value="rivals", description="Script currently down"),
            discord.SelectOption(label="BloxFruits", value="bloxfruits", description="Script currently down"),
            discord.SelectOption(label="FixLag", value="fixlag", description="Script currently down"),
            discord.SelectOption(label="TSB (Supa Tech)", value="tsb", description="Script currently down"),
        ]
        super().__init__(placeholder="🔍 Select the script you want to get...", min_values=1, max_values=1, options=options)
        self.author_id = author_id

    async def callback(self, interaction: discord.Interaction):
        # Only the user who ran the command can use this menu
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("❌ You can’t use this menu.", ephemeral=True)
            return

        value = self.values[0]
        channel = bot.get_channel(GETSCRIPT_CHANNEL_ID)

        if value == "allinone":
            embed = discord.Embed(
                title="🧩 Monster Hub | All-In-One Script",
                description="✨ **A complete multi-purpose script** — includes 99Nights, Rivals, BloxFruits, FixLag, and TSB.\nKeyless, fast, clean, and fully optimized for any executor.",
                color=discord.Color.red()
            )
            embed.add_field(name="📜 Script:", value=ALLINONE_SCRIPT, inline=False)
            embed.set_footer(text=f"Requested by {interaction.user.display_name}")
            await channel.send(embed=embed)

            await interaction.response.edit_message(
                content=f"✅ The **All-In-One Script** has been sent in <#{GETSCRIPT_CHANNEL_ID}>.",
                view=None
            )

        else:
            await interaction.response.edit_message(
                content=f"⚠️ The **{value}** script is currently down. Please try again later.",
                view=None,
                ephemeral=True
            )

# ============ VIEW ============
class ScriptView(View):
    def __init__(self, author_id: int, timeout: float = 60.0):
        super().__init__(timeout=timeout)
        self.add_item(ScriptSelect(author_id))

# ============ SLASH COMMAND ============
@bot.tree.command(name="getscript", description="Get a Monster Hub script")
async def getscript(interaction: discord.Interaction):
    view = ScriptView(author_id=interaction.user.id)
    await interaction.response.send_message(
        "🧠 Choose the script you want to receive (only you can see this menu).",
        view=view,
        ephemeral=True
    )

# ============ RUN BOT ============
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
