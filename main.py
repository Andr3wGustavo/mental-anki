import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
from anki_manager import AnkiManager

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
ANKI_URL = os.getenv('ANKI_CONNECT_URL', 'http://localhost:8765')

if not TOKEN or not CHANNEL_ID:
    logging.error("As variáveis DISCORD_TOKEN e DISCORD_CHANNEL_ID precisam estar definidas no .env")
    exit(1)

# Converte CHANNEL_ID para int
try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    logging.error("DISCORD_CHANNEL_ID deve ser um número inteiro")
    exit(1)

# Inicia o gerenciador do Anki
anki_manager = AnkiManager(anki_url=ANKI_URL)

# Configura o Bot do Discord com suporte a comandos
intents = discord.Intents.default()
intents.message_content = True  # Necessário para ler o conteúdo da mensagem e anexos
intents.messages = True

# O prefixo de comandos será "!"
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    logging.info(f'Bot logado como {bot.user}')
    logging.info(f'Escutando mensagens no canal ID: {CHANNEL_ID}')
    # Verifica inicialização do AnkiConnect
    if anki_manager.is_online():
        logging.info("AnkiConnect detectado! O baralho está pronto para uso.")
    else:
        logging.warning("AnkiConnect está offline no momento. O Anki está fechado?")
        logging.warning("Imagens recebidas irão para a fila e aguardarão o Anki ser aberto.")

@bot.event
async def on_message(message):
    # Ignora as próprias mensagens do bot
    if message.author == bot.user:
        return

    # Processa os comandos (importante para que o bot não ignore comandos por causa do on_message)
    await bot.process_commands(message)

    # Apenas processa imagens do canal específico
    if message.channel.id != CHANNEL_ID:
        return
    
    # Se a mensagem começar com o prefixo de comando, ignora a busca por imagens
    if message.content.startswith(bot.command_prefix):
        return

    # Verifica se há imagens anexadas ou links de imagens
    images_found = []

    # 1. Verifica attachments (imagens anexadas diretamente)
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith('image/'):
                images_found.append({
                    'url': attachment.url,
                    'filename': attachment.filename
                })

    # 2. Verifica embeds
    if message.embeds:
        for i, embed in enumerate(message.embeds):
            if embed.image and embed.image.url:
                filename = f"embed_image_{message.id}_{i}.jpg"
                images_found.append({
                    'url': embed.image.url,
                    'filename': filename
                })
            elif embed.thumbnail and embed.thumbnail.url:
                filename = f"embed_thumb_{message.id}_{i}.jpg"
                images_found.append({
                    'url': embed.thumbnail.url,
                    'filename': filename
                })
            
    # Processa as imagens encontradas
    for img in images_found:
        logging.info(f"Nova imagem detectada no Discord: {img['filename']} - URL: {img['url']}")
        anki_manager.add_image_note(url=img['url'], filename=img['filename'])
        
        try:
            await message.add_reaction('✅')
        except:
            pass 

# ==========================================
# PAINEL DE COMANDOS
# ==========================================

@bot.command(name="ajuda")
async def cmd_ajuda(ctx):
    """Mostra o painel de ajuda e comandos disponíveis."""
    embed = discord.Embed(title="🧠 Mental Anki - Painel de Controle", color=0x00ff00)
    embed.add_field(name="`!status`", value="Verifica se a conexão com o seu aplicativo Anki está ativa.", inline=False)
    embed.add_field(name="`!fila`", value="Mostra quantas imagens estão aguardando o Anki abrir para serem salvas.", inline=False)
    embed.set_footer(text="Basta enviar imagens neste canal para enviá-las automaticamente para o Anki!")
    await ctx.send(embed=embed)

@bot.command(name="status")
async def cmd_status(ctx):
    """Verifica o status da conexão com o Anki."""
    if anki_manager.is_online():
        await ctx.send("🟢 **AnkiConnect Online!** O seu aplicativo Anki está aberto e conectado.")
    else:
        await ctx.send("🔴 **AnkiConnect Offline.** O seu Anki parece estar fechado. Se você enviar imagens agora, elas irão para a fila.")

@bot.command(name="fila")
async def cmd_fila(ctx):
    """Verifica quantas imagens estão na fila."""
    size = anki_manager.get_queue_size()
    if size == 0:
        await ctx.send("✅ A fila está vazia. Todas as imagens já foram enviadas pro Anki!")
    else:
        await ctx.send(f"📦 **Existem {size} imagem(ns) na fila!**\nAbra o seu aplicativo Anki no computador para que eu possa enviá-las automaticamente.")

if __name__ == "__main__":
    logging.info("Iniciando o Bot do Mental Anki com Painel de Comandos...")
    bot.run(TOKEN, log_handler=None)
