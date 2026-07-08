# Como o Mental Anki Funciona 🧠

Este documento serve para você (ou qualquer desenvolvedor) entender a arquitetura do projeto no futuro.

## 1. Fluxo Principal
1. O usuário salva uma imagem no **Pinterest**.
2. Uma automação externa (como Zapier ou Make) envia essa imagem para um canal específico no **Discord**.
3. O nosso bot local (`main.py`) escuta esse canal 24h por dia (enquanto o PC estiver ligado).
4. Ao detectar uma imagem, o bot captura a URL dessa imagem e passa para o `AnkiManager`.
5. O `AnkiManager` se comunica com o plugin **AnkiConnect** (rodando localmente na porta `8765`).
6. Um novo cartão do tipo "Mental Anki" (focado apenas na imagem) é criado no baralho.

## 2. A Fila Inteligente (SQLite)
A maior dor de cabeça de automações locais é: *E se o Anki estiver fechado?*

Para resolver isso, o sistema possui uma fila inteligente embutida em `anki_manager.py`:
- Se o bot tentar enviar a imagem e o Anki estiver fechado, a requisição falha.
- Imediatamente, o script salva a URL da imagem em um banco de dados local super leve (`queue.db`).
- Uma thread (tarefa em segundo plano) roda a cada 10 segundos verificando se o Anki voltou a ficar online.
- Assim que você abre o Anki, essa thread percebe, pega todas as imagens que estavam no banco de dados, cria os cartões e limpa a fila.

## 3. Os Arquivos
- **`main.py`**: É o coração do bot do Discord. Gerencia os eventos de nova mensagem, comandos e interações de chat.
- **`anki_manager.py`**: É a classe isolada que lida *apenas* com o Anki e o Banco de Dados. Ela contém os endpoints de chamadas HTTP para o AnkiConnect.
- **`start.bat`**: Atalho simples do Windows para inicializar o ambiente Python e rodar o bot sem precisar usar o terminal de comando manualmente.
