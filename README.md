# 🤖 RogersBot - Bot de Discord para consultar estatísticas do VALORANT

RogersBot é um bot de Discord simples e funcional que permite consultar o **elo** e outras **estatísticas básicas** de um jogador de **VALORANT** usando comandos de slash (/) diretamente no seu servidor. Ele utiliza a API pública do [HenrikDev.xyz](https://docs.henrikdev.xyz/) para obter os dados.

> ⚠️ **Aviso de segurança:** este bot foi desenvolvido para uso pessoal. Recomenda-se não compartilhar suas **chaves de API** ou **tokens de bot** em repositórios públicos. Para mais detalhes sobre a API utilizada, consulte a [documentação oficial da HenrikDev](https://docs.henrikdev.xyz/).

---

## ✨ Funcionalidades

### 📡 Comando `/ping`
Comando simples que retorna a **latência atual do bot** no servidor. Útil para verificar se o bot está responsivo.

### 🎮 Comando `/info <nickname> <tag>`
Este é o **principal comando** do bot. Ele retorna um embed contendo:

- 🌎 Região do jogador
- ⭐ Nível da conta
- 🏆 Elo atual (ex: Gold 1)
- 📈 Progresso no elo atual (em %)
- 🔝 Maior elo já atingido pela conta

---

## 🧩 Estrutura do Projeto

O projeto é dividido em **dois arquivos principais**:

### 1. `main.py` (Programa principal)
Responsável por carregar o bot, autenticar com o Discord e iniciar o processo de sincronização dos comandos. Esse arquivo geralmente contém o token (que deve ser armazenado com segurança via `.env`).

### 2. `commands.py` (Comandos)
Contém os comandos slash utilizados no bot, organizados com a biblioteca `discord.app_commands`. Inclui os comandos `/ping` e `/info`.

---

## 📦 Dependências

Certifique-se de instalar as dependências necessárias listadas no `requirements.txt`:

```txt
discord.py
requests
python-dotenv

## 🔥 Novidades na v1.2.0

- Novo comando: `/ranked`
  - Mostra dados do modo competitivo do jogador (nível, vitórias, partidas e taxa de vitória).
  - Mostra a **taxa de headshots (%HS) da última partida**.

### ⚠️ Observações técnicas
- O cálculo da Taxa de HS só é possível para **a última partida** devido a limitações da API da HenrikDev:
  - Não há suporte eficiente para cálculo histórico completo.
  - A estrutura JSON exigiria processamento excessivo e iteração por dezenas de partidas manualmente.

