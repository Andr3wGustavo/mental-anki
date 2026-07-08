# Ideias de Melhorias e Futuras Features 💡

Este projeto já está robusto graças à sua Fila Inteligente (SQLite), mas sempre há espaço para deixá-lo mais divertido e produtivo. Aqui estão algumas sugestões do que pode ser adicionado futuramente:

## 1. Sistema de Tags por Reações do Discord
- **Como funcionaria:** Você configura o bot para entender reações. Se você reagir a uma imagem com 🍎, ele envia para o Anki no baralho "Mental Anki" com a tag `comida`. Se reagir com 🚗, ele adiciona a tag `veiculos`.
- **Vantagem:** Organização perfeita dos baralhos no Anki diretamente pelo chat.

## 2. Separação de Múltiplos Baralhos
- **Como funcionaria:** Criar canais diferentes no Discord (ex: `#mental-anatomia`, `#mental-design`). O bot leria todos eles e encaminharia as imagens para baralhos com nomes correspondentes no Anki.

## 3. Modo de "Estudo Passivo" no Próprio Discord
- **Como funcionaria:** Um comando tipo `!revisar` onde o bot pega imagens antigas do banco de dados e as reposta no canal, simulando uma revisão espaçada dentro do próprio chat do Discord, para quando você não estiver no PC com o Anki aberto.

## 4. OCR (Reconhecimento Ótico de Caracteres)
- **Como funcionaria:** Integrar a API do Google Vision ou Tesseract. Se a imagem do Pinterest tiver algum texto motivacional ou termo em inglês, o bot lê o texto da imagem automaticamente e o coloca no verso do cartão do Anki!

---

*Nota: Um painel de comandos já foi implementado no `main.py`! Digite `!ajuda` no seu canal para ver.*
