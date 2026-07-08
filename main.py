import os
import discord
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

# Configura o Bot do Discord
intents = discord.Intents.default()
intents.message_content = True  # Necessário para ler o conteúdo da mensagem e anexos
intents.messages = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'Bot logado como {client.user}')
    logging.info(f'Escutando mensagens no canal ID: {CHANNEL_ID}')
    # Verifica inicialização do AnkiConnect
    if anki_manager.is_online():
        logging.info("AnkiConnect detectado! O baralho está pronto para uso.")
    else:
        logging.warning("AnkiConnect está offline no momento. O Anki está fechado? As imagens recebidas irão para a fila e aguardarão o Anki ser aberto.")

@client.event
async def on_message(message):
    # Ignora as próprias mensagens do bot (se aplicável)
    if message.author == client.user:
        return

    # Apenas processa mensagens do canal específico
    if message.channel.id != CHANNEL_ID:
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

    # 2. Verifica embeds (caso a automação do Pinterest envie um link que gera um embed de imagem)
    if message.embeds:
        for i, embed in enumerate(message.embeds):
            # Tenta pegar a imagem do embed
            if embed.image and embed.image.url:
                filename = f"embed_image_{message.id}_{i}.jpg"
                images_found.append({
                    'url': embed.image.url,
                    'filename': filename
                })
            # Tenta pegar thumbnail se não tiver imagem direta
            elif embed.thumbnail and embed.thumbnail.url:
                filename = f"embed_thumb_{message.id}_{i}.jpg"
                images_found.append({
                    'url': embed.thumbnail.url,
                    'filename': filename
                })
            
    # Processa as imagens encontradas
    for img in images_found:
        logging.info(f"Nova imagem detectada no Discord: {img['filename']} - URL: {img['url']}")
        # Adiciona ao Anki (ou coloca na fila se o Anki estiver fechado)
        anki_manager.add_image_note(url=img['url'], filename=img['filename'])
        
        # Opcional: Reagir à mensagem para mostrar que foi processada
        try:
            await message.add_reaction('✅')
        except:
            pass # Ignora se não tiver permissão para reagir

if __name__ == "__main__":
    logging.info("Iniciando o Bot do Mental Anki...")
    client.run(TOKEN, log_handler=None) # Passando None para usar o logger raiz configurado no início
