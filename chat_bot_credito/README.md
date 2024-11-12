# Chatbot COVID-19 - Artemis

Este projeto é um chatbot interativo, chamado **Artemis**, que fornece informações sobre dados de COVID-19. A Artemis utiliza uma interface gráfica criada com `customtkinter` para exibir dados globais, de países específicos, histórico de casos e dados de vacinação sobre a COVID-19. O chatbot utiliza a API [disease.sh](https://disease.sh/) para obter informações atualizadas e inclui suporte de áudio para saudar o usuário ao iniciar o aplicativo.

## Funcionalidades

- Exibe dados globais sobre COVID-19.
- Exibe dados de COVID-19 para um país específico.
- Fornece histórico dos últimos 30 dias de casos para um país específico.
- Exibe dados de vacinação para um país.
- Saudação de boas-vindas com síntese de voz ao iniciar o aplicativo.

## Tecnologias Utilizadas

- `customtkinter`: Biblioteca para criar a interface gráfica do chatbot.
- `requests`: Para fazer requisições HTTP à API de dados de COVID-19.
- `pyttsx3`: Para síntese de voz no Python.
- `unicodedata`, `re`: Para normalização e manipulação de strings.

## Pré-requisitos

- Python 3.7 ou superior instalado.
- `pipenv` instalado para gerenciar o ambiente virtual.

## Configuração do Ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/seu_usuario/chatbot-covid19.git
cd chatbot-covid19