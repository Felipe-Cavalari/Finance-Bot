import pandas as pd
from datetime import datetime
import logging
from pathlib import Path

# Caminho para coletar o arquivo
date = datetime.now().strftime("%d_%m_%Y")
file_path = "../reports"
file_name = "altas_e_baixas"
full_path = f"{file_path}/{file_name}_{date}.csv"

print(file_path)


# Configuração de logging para registrar erros e informações
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)







# Iniciando pandas
def load_csv(file):
    logger.info(f"Coletando arquivo em: {file}")
    try:
        df = pd.read_csv(file)
    except:
        logger.error("Algo deu errado ao ler o arquivo")

    

    # coletando as 5 maiores altas
    top5 = df.head(5)
    top5.to_html('./top.html', index=False, border=0, classes='dataframe', justify='center')

    # coletando as 5 maiores baixas
    bottom5 = df.tail(5).sort_values(by='Var. Dia (%)', ascending=False)
    bottom5_html_table = bottom5.to_html('./bottom.html', index=False, border=0, classes='dataframe', justify='center')




load_csv(full_path)