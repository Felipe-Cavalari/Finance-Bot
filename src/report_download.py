import os
import time
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging

# --- Configurações ---
# URL da página
URL = "https://www.infomoney.com.br/ferramentas/altas-e-baixas/"

# Caminho para salvar o arquivo
PROJECT_PATH = Path(__file__).parent.parent
DOWNLOAD_PATH = os.path.join(PROJECT_PATH, 'reports')
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Nome do arquivo baixado originalmente
NOME_ARQUIVO_ORIGINAL = "altas_e_baixas.csv"

# Timeout para espera de elementos e download (em segundos)
TIMEOUT_DEFAULT = 10
TIMEOUT_DOWNLOAD = 30

# Configuração de logging para registrar erros e informações
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Funções Auxiliares ---

def esperar_download_concluir(pasta_download, timeout=TIMEOUT_DOWNLOAD):
    """Verifica se o download foi concluído aguardando o desaparecimento do .crdownload."""
    logger.info(f"Aguardando conclusão do download em: {pasta_download}")
    for _ in range(timeout):
        if not any(f.endswith(".crdownload") for f in os.listdir(pasta_download)):
            logger.info("Download concluído.")
            return True
        time.sleep(1)
    logger.error("Timeout: Download não finalizado a tempo.")
    raise TimeoutException("Download não finalizado a tempo.")

def renomear_arquivo_altas(caminho_download):
    """Renomeia o arquivo baixado adicionando a data atual."""
    caminho_original = os.path.join(caminho_download, NOME_ARQUIVO_ORIGINAL)

    if os.path.exists(caminho_original):
        data_atual = datetime.now().strftime("%d_%m_%Y")
        novo_nome = f"altas_e_baixas_{data_atual}.csv"
        caminho_novo = os.path.join(caminho_download, novo_nome)

        try:
            os.rename(caminho_original, caminho_novo)
            logger.info(f"Arquivo renomeado para: {novo_nome}")
            return caminho_novo # Retorna o novo caminho
        except OSError as e:
            logger.error(f"Falha ao renomear o arquivo: {e}")
            raise
    else:
        logger.warning(f"Arquivo {NOME_ARQUIVO_ORIGINAL} não encontrado em {caminho_download}.")
        return None # Indica que o arquivo não foi encontrado/renomeado

def setup_driver(download_path, headless=True):
    """Configura e retorna uma instância do WebDriver."""
    options = Options()
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    # Adiciona mais opções para estabilidade em headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        logger.info("WebDriver inicializado com sucesso.")
        return driver
    except Exception as e:
        logger.error(f"Erro ao inicializar o WebDriver: {e}")
        raise

def clicar_botao_download(driver, timeout=TIMEOUT_DEFAULT):
    """Tenta clicar no botão de download."""
    # IDs potenciais para o botão de download
    # A página parece ter um ID específico para mobile, mas vamos tentar um ID mais genérico primeiro
    # Se o ID correto for diferente, ajuste aqui.
    ids_para_tentar = ["export_altas_e_baixas", "export_altas_e_baixas_mobile"] # Ajuste os IDs conforme inspecionado

    for botao_id in ids_para_tentar:
        try:
            logger.info(f"Tentando encontrar e clicar no botão com ID: {botao_id}")
            botao = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.ID, botao_id))
            )
            botao.click()
            logger.info(f"Botão '{botao_id}' clicado com sucesso.")
            return # Sai da função se o clique for bem-sucedido
        except TimeoutException:
             logger.warning(f"Botão com ID '{botao_id}' não encontrado ou não clicável.")
             continue # Tenta o próximo ID

    # Se nenhum ID funcionar
    logger.error("Nenhum botão de download encontrado com os IDs fornecidos.")
    raise TimeoutException("Botão de download não encontrado.")

# --- Função Principal da Automação ---

def executar_automacao(url=URL, download_path=DOWNLOAD_PATH, headless=True):
    """
    Executa a automação completa: abre o navegador, navega, clica no botão,
    espera o download e renomeia o arquivo.
    """
    driver = None
    try:
        logger.info("Iniciando automação...")
        driver = setup_driver(download_path, headless=headless)
        logger.info(f"Acessando URL: {url}")
        driver.get(url)

        # Tenta clicar no botão de download
        clicar_botao_download(driver)

        # Espera o download terminar
        esperar_download_concluir(download_path)

        # Renomeia o arquivo
        caminho_arquivo_renomeado = renomear_arquivo_altas(download_path)
        
        logger.info("Automação concluída com sucesso.")
        return caminho_arquivo_renomeado # Retorna o caminho do arquivo final

    except TimeoutException as te:
        logger.error(f"Timeout durante a automação: {te}")
        raise
    except WebDriverException as wde:
        logger.error(f"Erro do WebDriver: {wde}")
        raise
    except Exception as e:
         logger.error(f"Erro inesperado durante a automação: {e}")
         raise
    finally:
        if driver:
            try:
                driver.quit() # Fecha o navegador e encerra o driver
                logger.info("WebDriver encerrado.")
            except Exception as e:
                 logger.warning(f"Erro ao encerrar o WebDriver: {e}")

# --- Ponto de Entrada (para execução direta ou via main.py) ---
if __name__ == "__main__":
    try:
        caminho_final = executar_automacao()
        if caminho_final:
             print(f"Processo finalizado. Arquivo disponível em: {caminho_final}")
        else:
             print("Processo finalizado, mas o arquivo não pôde ser renomeado.")
    except Exception as e:
        print(f"Erro na execução principal: {e}")
