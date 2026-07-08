# Guia de Configuração e Instalação Definitivo

Se você precisar instalar este bot em outro computador, ou reconfigurar, siga exatamente estes passos.

## Parte 1: O Anki e o AnkiConnect
O bot não consegue falar com o Anki sem um tradutor. O AnkiConnect é esse tradutor (uma API local).
1. Abra o Anki.
2. Vá em `Ferramentas` -> `Extensões` -> `Obter Extensões...`
3. Cole o código do plugin AnkiConnect: **`2055492159`** e confirme.
4. Reinicie o Anki.
5. Volte em `Ferramentas` -> `Extensões`, clique em `AnkiConnect` e depois no botão `Configuração`.
6. Altere a linha de CORS para aceitar conexões amplas:
   ```json
   "webCorsOriginList": ["*"]
   ```
7. Pronto! A partir de agora, sempre que o Anki estiver aberto, ele estará "escutando" na porta 8765.

## Parte 2: O Token do Discord
Para o bot ler seu canal, ele precisa existir oficialmente no Discord.
1. Vá para o [Discord Developer Portal](https://discord.com/developers/applications).
2. Clique em **New Application** e chame de "Mental Anki".
3. Vá no menu esquerdo em **Bot**.
4. Clique em **Reset Token** e copie o token gerado. **(Nunca compartilhe este token publicamente)**.
5. **ATENÇÃO:** Role a tela para baixo até a seção `Privileged Gateway Intents` e ATIVE a opção **Message Content Intent**. Se não fizer isso, o bot não consegue ver imagens!
6. Salve.
7. Para convidar o bot pro seu servidor: Vá no menu esquerdo em **OAuth2 -> URL Generator**. Marque o escopo `bot`, e nas permissões marque `Read Messages/View Channels`, `Send Messages` e `Add Reactions`.
8. Copie a URL gerada, cole no navegador e adicione o bot ao seu servidor onde está o canal de imagens.

## Parte 3: Configuração do Projeto (.env)
1. Crie um arquivo chamado `.env` na pasta raiz (onde fica o `main.py`).
2. Adicione estas linhas e preencha com seus dados reais:
   ```env
   DISCORD_TOKEN=cole_seu_token_aqui
   DISCORD_CHANNEL_ID=id_numerico_do_canal_de_imagens
   ANKI_CONNECT_URL=http://localhost:8765
   ```
   *(Para pegar o ID do canal, ative o Modo Desenvolvedor no seu Discord, clique com botão direito no canal e clique em 'Copiar ID').*

## Parte 4: Rodando
Com tudo configurado e o Anki aberto:
1. Dê dois cliques em `start.bat`.
2. O terminal preto abrirá avisando que o bot está logado. Pode minimizá-lo!
