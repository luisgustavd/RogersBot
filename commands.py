import os
import discord
import requests
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do .env

API_KEY = os.getenv("HENRIK_API_KEY") # CHAVE API DO HENRIK DEV
VALORANT_RED = 0xFF4655 # cor tema do valorant

# Comando /ping
@app_commands.command(name="ping", description="Mostra a latência do bot.")
async def ping(interaction):
    latency = round(interaction.client.latency * 1000)
    embed = discord.Embed(
        title="🛰️ PING - RogersBot",
        description=f"📶 | **Latência Atual:** `{latency} ms`",
        color=VALORANT_RED
    )
    embed.set_footer(
        text="RogersBot • Status do Bot",
        icon_url="https://img.icons8.com/?size=100&id=30998&format=png&color=000000"
    )
    await interaction.response.send_message(embed=embed)

# Comando /info
@app_commands.command(name="info", description="Mostra informações de um jogador do VALORANT.")
@app_commands.describe(nickname="Nickname", tag="Tag (sem #)")
async def info(interaction: discord.Interaction, nickname: str, tag: str):
    await interaction.response.defer()

    if "#" in tag or "#" in nickname:
        await interaction.followup.send("❗ Formato incorreto. Use o <Nome> sem # na <tag>.")
        return

    headers = {"Authorization": API_KEY}

    url_account = f"https://api.henrikdev.xyz/valorant/v2/account/{nickname}/{tag}"
    response_account = requests.get(url_account, headers=headers)

    if response_account.status_code != 200:
        await interaction.followup.send(
            f"😥 Não foi possível encontrar o jogador `{nickname}`.\n"
            f"📃 Erro: `{response_account.text}`"
        )
        return

    data_account = response_account.json().get("data", {})
    region = data_account.get("region")

    url_elo = f"https://api.henrikdev.xyz/valorant/v2/mmr/{region}/{nickname}/{tag}"
    response_elo = requests.get(url_elo, headers=headers)

    if response_elo.status_code != 200:
        await interaction.followup.send("❌ Não foi possível buscar o elo do jogador.")
        return

    data_elo = response_elo.json().get("data", {})
    elo_details = data_elo.get("current_data", {})
    elo_highest_details = data_elo.get("highest_rank", {})

    current_tier = elo_details.get("currenttierpatched", "Desconhecido")
    elo_progress = elo_details.get("ranking_in_tier", "0")
    highest_elo = elo_highest_details.get("patched_tier", "Indefinido")

    nome_completo = f"{data_account.get('name')}#{data_account.get('tag')}"
    account_level = data_account.get("account_level", "Desconhecido")

    embed = discord.Embed(
        title=f"🎮 {nome_completo}",
        description=(
            f"🌏 Região: `{region.upper()}`\n"
            f"⭐ Nível da Conta: `{account_level}`\n"
            f"🏆 Rank Atual: **{current_tier}**\n"
            f"📈 Progresso no Rank: `{elo_progress}/100`\n"
            f"👑 Maior Elo da Conta: **{highest_elo}**"
        ),
        color=VALORANT_RED
    )
    embed.set_footer(
        text="RogersBot • Powered by HenrikDev API",
        icon_url="https://img.icons8.com/?size=100&id=aUZxT3Erwill&format=png&color=000000"
    )

    await interaction.followup.send(embed=embed)


@app_commands.command(name="ranked", description="Mostra informações do Competitivo de um jogador do VALORANT.")
@app_commands.describe(nickname="Nickname", tag="Tag (sem #)")
async def ranked(interaction: discord.Interaction, nickname: str, tag: str):
    await interaction.response.defer()

    if "#" in tag or "#" in nickname:
        await interaction.followup.send("❗ Formato incorreto. Use o <Nome_do_player> sem # na <tag>.")
        return

    headers = {"Authorization": API_KEY}
    url_account = f"https://api.henrikdev.xyz/valorant/v2/account/{nickname}/{tag}"
    response_account = requests.get(url_account, headers=headers)

    if response_account.status_code != 200:
        await interaction.followup.send(
            f"😥 Não foi possível encontrar o jogador `{nickname}`.\n"
            f"📃 Detalhes técnicos: `{response_account.text}`."
        )
        return

    data_account = response_account.json().get("data", {})
    region = data_account.get("region")

    url_mmr = f"https://api.henrikdev.xyz/valorant/v2/mmr/{region}/{nickname}/{tag}"
    response_mmr = requests.get(url_mmr, headers=headers)

    if response_mmr.status_code != 200:
        await interaction.followup.send("❌ Não foi possível obter dados Competitivo do jogador.")
        return

    data_mmr = response_mmr.json()
    seasons = data_mmr.get("data", {}).get("by_season", {})

    total_partidas = sum(season.get("number_of_games", 0) for season in seasons.values())
    total_vitorias = sum(season.get("wins", 0) for season in seasons.values())
    taxa_vitoria = (total_vitorias / total_partidas) * 100 if total_partidas > 0 else 0

    nome_completo = f"{data_account.get('name')}#{data_account.get('tag')}"
    account_level = data_account.get("account_level", "Desconhecido")

    url_hs = f"https://api.henrikdev.xyz/valorant/v3/matches/{region}/{nickname}/{tag}"
    response_hs = requests.get(url_hs, headers=headers)

    if response_hs.status_code != 200:
        await interaction.followup.send("❌ Não foi possível calcular %HS do jogador.")
        return

    partidas = response_hs.json().get("data", [])
    taxa_hs = 0.0

    if partidas:
        ultima_partida = partidas[0]
        jogadores = ultima_partida.get("players", {}).get("all_players", [])
        for player in jogadores:
            if player["name"].lower() == nickname.lower() and player["tag"] == tag:
                stats = player.get("stats", {})
                headshots = stats.get("headshots", 0)
                bodyshots = stats.get("bodyshots", 0)
                legshots = stats.get("legshots", 0)

                total_shots = headshots + bodyshots + legshots
                taxa_hs = (headshots / total_shots) * 100 if total_shots > 0 else 0
                break

    embed = discord.Embed(
        title=nome_completo,
        description=(
            f"🔥 COMPETITIVO\n\n"
            f"⭐ Nível da Conta: `{account_level}`\n"
            f"🎮 Partidas jogadas : **{total_partidas}**\n"
            f"💯 Partidas vencidas: **{total_vitorias}**\n"
            f"📊 Taxa de Vitória: **{taxa_vitoria:.2f}%**\n"
            f"💪 %HS na última partida: **{taxa_hs:.2f}%**\n"
        ),
        color=VALORANT_RED
    )

    embed.set_footer(
        text="RogersBot • Powered by HenrikDev API",
        icon_url="https://img.icons8.com/?size=100&id=aUZxT3Erwill&format=png&color=000000"
    )

    await interaction.followup.send(embed=embed)

async def setup_command(bot):
    bot.tree.add_command(ping)
    bot.tree.add_command(info)
    bot.tree.add_command(ranked)
