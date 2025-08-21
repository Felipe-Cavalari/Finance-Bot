import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

# Carrega o .env especificando o caminho
config_path = os.path.join(os.getcwd(), 'config', '.env')
load_dotenv(config_path)


# Configuração de logging para registrar erros e informações
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Configurações do e-mail
date = datetime.now().strftime("%d/%m/%Y")
from_email = "fecavalaridev@gmail.com"
to_email = ["felipe.cavalari89@gmail.com"]
subject = "Relatório Diário - Ações em Alta"
password = os.getenv("gmail_password")  # Use senha de app no Gmail

def html_config(top, bottom):
    # Corpo do e-mail com HTML
    html_content = f"""
    <html>
    <head>
    <style>
        .dataframe {{
            border-collapse: collapse;
            width: 100%;
        }}
        .dataframe th, .dataframe td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }}
        .dataframe th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}

        #title {{
            
        }}
    </style>
    </head>
    <body>

    <h2 id="title"> Fechamento do dia - {date} </h1>

    <br>
    <br>

    <h2>📈 Principais altas do IBOV</h2>
    {top}

    <br>
    <br>

    <h2>📉 Principais baixas do IBOV</h2>
    {bottom}
    </body>
    </html>
    """

    return html_content
    

def email_send(html_content):
    try:
        message = MIMEMultipart("alternative")
        message["From"] = from_email
        message["To"] = ", ".join(to_email)
        message["Subject"] = subject
        message.attach(MIMEText(html_content, "html"))

        # Envio via SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, password)
            server.send_message(message)
        
        logger.info("Email enviado!")

    except smtplib.SMTPAuthenticationError:
        logger.error("Falha na autenticação SMTP - verifique suas credenciais")
        raise
    except smtplib.SMTPRecipientsRefused:
        logger.error("Todos os destinatários foram recusados")
        raise
    except smtplib.SMTPException as e:
        logger.error(f"Erro ao enviar email: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar email: {str(e)}")
        raise
