import os
import pandas as pd
from datetime import datetime
import logging
from pathlib import Path
from .send_email import html_config, email_send
from dotenv import load_dotenv

# Carrega o .env especificando o caminho
config_path = os.path.join(os.getcwd(), 'config', '.env')
load_dotenv(config_path)

# Configuração de logging para registrar erros e informações
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Caminho para coletar o arquivo
date = datetime.now().strftime("%d_%m_%Y")
root_path = Path(__file__).parent.parent
file_path = root_path / "reports"
file_name = "altas_e_baixas"
full_path = f"{file_path}/{file_name}_{date}.csv"
html_table_path = root_path / "html_tables"
# os.makedirs(html_table_path, exist_ok=True)


# Iniciando pandas
def load_csv(file):
    logger.info(f"Coletando arquivo em: {file}")
    try:
        df = pd.read_csv(file)
        logger.info("Tabela extraida do projeto")
        print(df)
    except FileNotFoundError as e:
        logger.error(f"Arquivo não encontrado: {e}")
        raise
    except pd.errors.EmptyDataError:
        logger.error("Arquivo CSV vazio ou corrompido")
        raise
    except pd.errors.ParserError as e:
        logger.error(f"Erro ao parsear o arquivo CSV: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao ler o arquivo: {e}")
        raise

    # coletando as 5 maiores altas
    logger.info("Iniciando coleta das 5 maiores altas \n")
    top5 = df.head(5)
    top5_html = top5.to_html(index=False, border=0, classes='dataframe', justify='center')

    # coletando as 5 maiores baixas
    logger.info("Iniciando coleta das 5 maiores baixas \n")
    bottom5 = df.tail(5).sort_values(by='Var. Dia (%)', ascending=False)
    bottom5_html = bottom5.to_html(index=False, border=0, classes='dataframe', justify='center')


    # Enviando e-mail
    html = html_config(top=top5_html, bottom=bottom5_html)
    logger.info("Iniciando envio de e-mail")
    email_send(html)
