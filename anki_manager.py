import json
import sqlite3
import requests
import os
import time
import logging
from threading import Thread

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AnkiManager:
    def __init__(self, anki_url="http://localhost:8765"):
        self.anki_url = anki_url
        self.deck_name = "Mental Anki"
        self.model_name = "Mental Anki"
        self.db_path = "queue.db"
        self.init_db()
        self.start_queue_worker()

    def init_db(self):
        """Inicializa o banco de dados SQLite para a fila."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                filename TEXT NOT NULL,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def _invoke(self, action, **params):
        """Função auxiliar para fazer requisições para o AnkiConnect."""
        requestJson = json.dumps({'action': action, 'version': 6, 'params': params}).encode('utf-8')
        try:
            response = requests.post(self.anki_url, data=requestJson, timeout=5)
            response.raise_for_status()
            response_json = response.json()
            if len(response_json) != 2:
                raise Exception('A resposta tem um número inesperado de campos')
            if 'error' not in response_json:
                raise Exception('A resposta não contém o campo de erro')
            if response_json['error'] is not None:
                raise Exception(response_json['error'])
            if 'result' not in response_json:
                raise Exception('A resposta não contém o campo de resultado')
            return response_json['result']
        except Exception as e:
            return None  # Retorna None indicando falha na comunicação

    def is_online(self):
        """Verifica se o AnkiConnect está respondendo."""
        try:
            requests.get(self.anki_url, timeout=2)
            return True
        except:
            return False

    def setup_anki(self):
        """Garante que o baralho e o tipo de nota existam."""
        if not self.is_online():
            logging.warning("Anki está offline. Não foi possível configurar o baralho no momento.")
            return False

        # Criar Baralho
        self._invoke('createDeck', deck=self.deck_name)

        # Criar Tipo de Nota (Modelo)
        model_names = self._invoke('modelNames')
        if model_names and self.model_name not in model_names:
            self._invoke('createModel',
                         modelName=self.model_name,
                         inOrderFields=["Imagem"],
                         css=".card { font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white; }",
                         isCloze=False,
                         cardTemplates=[
                             {
                                 "Name": "Cartão Principal",
                                 "Front": "{{Imagem}}",
                                 "Back": "{{Imagem}}"
                             }
                         ])
            logging.info(f"Modelo '{self.model_name}' criado com sucesso.")
        return True

    def add_to_queue(self, url, filename):
        """Adiciona a imagem na fila do banco de dados local."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO queue (url, filename) VALUES (?, ?)", (url, filename))
        conn.commit()
        conn.close()
        logging.info(f"Imagem enfileirada: {filename}")

    def add_image_note(self, url, filename):
        """Tenta enviar a imagem para o Anki. Se falhar, coloca na fila."""
        if self.is_online():
            self.setup_anki() # Garante que o baralho existe antes de adicionar
            note = {
                "deckName": self.deck_name,
                "modelName": self.model_name,
                "fields": {
                    "Imagem": ""
                },
                "options": {
                    "allowDuplicate": False,
                    "duplicateScope": "deck"
                },
                "picture": [{
                    "url": url,
                    "filename": filename,
                    "fields": [
                        "Imagem"
                    ]
                }]
            }
            result = self._invoke('addNote', note=note)
            if result:
                logging.info(f"Cartão criado com sucesso para: {filename}")
                return True
            else:
                logging.error(f"Falha ao criar o cartão. Enfileirando. URL: {url}")
                self.add_to_queue(url, filename)
                return False
        else:
            logging.warning(f"AnkiConnect não encontrado. Enfileirando imagem: {filename}")
            self.add_to_queue(url, filename)
            return False

    def process_queue(self):
        """Processa a fila se o Anki estiver online."""
        while True:
            try:
                if self.is_online():
                    conn = sqlite3.connect(self.db_path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, url, filename FROM queue ORDER BY id ASC")
                    items = cursor.fetchall()

                    if items:
                        self.setup_anki()
                        for item in items:
                            item_id, url, filename = item
                            note = {
                                "deckName": self.deck_name,
                                "modelName": self.model_name,
                                "fields": {
                                    "Imagem": ""
                                },
                                "picture": [{
                                    "url": url,
                                    "filename": filename,
                                    "fields": [
                                        "Imagem"
                                    ]
                                }]
                            }
                            result = self._invoke('addNote', note=note)
                            if result:
                                cursor.execute("DELETE FROM queue WHERE id = ?", (item_id,))
                                conn.commit()
                                logging.info(f"Processado da fila: {filename}")
                            else:
                                logging.error(f"Falha ao processar a fila para: {filename}")
                    conn.close()
            except Exception as e:
                logging.error(f"Erro no worker da fila: {e}")
            
            time.sleep(10) # Tenta novamente a cada 10 segundos

    def get_queue_size(self):
        """Retorna o número de itens atualmente na fila local."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM queue")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            return 0

    def start_queue_worker(self):
        """Inicia a thread em background para processar a fila."""
        thread = Thread(target=self.process_queue, daemon=True)
        thread.start()
        logging.info("Trabalhador de fila do Anki iniciado em segundo plano.")
