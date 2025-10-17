import discord
from discord.ext import commands
from flask import Flask, request, jsonify
import asyncio
import threading
from config import DISCORD_TOKEN, WEBHOOK_SECRET
from utils.notifier import send_github_update

# ====== CONFIGURAÇÃO DO BOT ======
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ====== CONFIGURAÇÃO DO FLASK ======
app = Flask(__name__)

@app.route("/github", methods=["POST"])
def github_webhook():
    data = request.json

    # Verifica assinatura se quiser segurança extra (opcional)
    if not data or "repository" not in data:
        return jsonify({"error": "Payload inválido"}), 400

    repo_name = data["repository"]["name"]
    commits = data.get("commits", [])
    pusher = data["pusher"]["name"]

    asyncio.run_coroutine_threadsafe(
        send_github_update(bot, repo_name, commits, pusher),
        bot.loop
    )

    return jsonify({"status": "ok"}), 200


@bot.event
async def on_ready():
    print(f"🤖 Bot conectado como {bot.user}")
    print("✅ Servidor Flask está escutando webhooks do GitHub...")


def run_flask():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.run(DISCORD_TOKEN)