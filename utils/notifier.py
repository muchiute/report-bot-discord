import discord
from config import DISCORD_CHANNEL_ID

async def send_github_update(bot, repo_name, commits, pusher):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        print("❌ Canal não encontrado!")
        return

    description = "\n".join(
        [f"• `{commit['id'][:7]}` — {commit['message']} *(por {commit['author']['name']})*" for commit in commits]
    )

    embed = discord.Embed(
        title=f"📦 Atualização no repositório {repo_name}",
        description=description or "Nenhum detalhe de commit encontrado.",
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Push feito por {pusher}")

    await channel.send(embed=embed)
