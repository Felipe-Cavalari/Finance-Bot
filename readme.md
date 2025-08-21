# Finance Bot

**Finance Bot** é um projeto em Python que automatiza a coleta e envio das principais informações do mercado financeiro do dia. Ele combina as bibliotecas **Selenium**, **Pandas** e **smtplib** para extrair, processar e enviar dados financeiros por email de forma prática e automatizada.

<br>

## Funcionalidades

- Acessa a página da [InfoMoney](https://www.infomoney.com.br/ferramentas/altas-e-baixas/) e extrai os dados de **altas e baixas do dia**.
- Identifica as **5 maiores altas** e **5 maiores baixas** usando **Pandas**.
- Gera **tabelas em HTML** com os resultados.
- Envia os relatórios automaticamente via **email** utilizando **smtplib**.

<br>

## Tecnologias

- **Python**
- **Selenium** – para automação de navegação web.
- **Pandas** – para manipulação e análise de dados.
- **smtplib** – para envio automático de emails.

<br>

## Como usar

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/finance-bot.git
   ```

2. Crie o ambiente virtual e instale as dependências:

   ```bash
   python -m venv nome_env
   pip install -r requirements.txt
   ```

3. Configure os emails e credenciais no arquivo de configuração.
4. Execute o bot:

   ```bash
   python main.py
   ```

<br>>

## Estrutura do Projeto

```
finance-bot/
│
├─ main.py           # Script principal
├─ utils/            # Funções auxiliares
│  ├─ send_email.py       # Envio de emails
│  ├─ analise_report.py       # Pandas para analise do report
│  └─ report_download.py     # Extração de dados do InfoMoney
├─ requirements.txt  # Dependências do projeto
└─ README.md         # Documentação
```

<br>

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias.

<br>

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
