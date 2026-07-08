# Mental Anki 🧠

An automated background service that bridges Discord and Anki, optimizing your visual learning experience.

**Mental Anki** listens to a specific Discord channel for incoming images (such as those synced from Pinterest) and automatically injects them into your local Anki application as image-only cards. It's built for rapid visual absorption without the hassle of manual card creation.

## 🚀 Features

- **Real-time Discord Listening**: Instantly captures images posted in your designated Discord channel (supports direct attachments and embedded image links).
- **Automated Anki Injection**: Communicates directly with the `AnkiConnect` plugin to create cards on the fly.
- **Smart Local Queue**: If Anki is closed when an image arrives, the bot securely stores the image URL in a local SQLite database (`queue.db`). As soon as Anki is opened, it automatically flushes the queue and generates the pending cards.
- **Pure Visual Format**: Automatically sets up the "Mental Anki" deck and card model, optimizing the card face for image-only display (no text on the back).

## 🛠️ Prerequisites

1. **Python 3.8+**
2. **Anki** with the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed.
3. A **Discord Bot Token**.

## ⚙️ Setup

1. **Clone the repository:**
   ```bash
   git clone git@github.com:Andr3wGustavo/mental-anki.git
   cd mental-anki
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Rename `.env.example` to `.env` and fill in your details:
   ```env
   DISCORD_TOKEN=your_discord_bot_token_here
   DISCORD_CHANNEL_ID=your_channel_id_here
   ANKI_CONNECT_URL=http://localhost:8765
   ```

4. **Configure AnkiConnect:**
   Ensure Anki is open. Go to `Tools -> Add-ons -> AnkiConnect -> Config` and ensure your CORS origins allow localhost (usually `"webCorsOriginList": ["*"]`).

## ▶️ Usage

Simply run the `start.bat` script (on Windows) or execute the bot manually:

```bash
python main.py
```

Leave the bot running in the background. Whenever an image drops into the configured Discord channel, it will instantly be transformed into an Anki card!

## 📄 License

This project is open-source and available under the MIT License.
