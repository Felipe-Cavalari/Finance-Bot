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
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
import logging

# Configuração de logging para registrar erros e informações
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Variaveis da automação
url = "https://www.infomoney.com.br/ferramentas/altas-e-baixas/"
project_path = Path(__file__).parent.parent
download_path = os.path.join(project_path, 'reports')

# Cria a pasta se ela não existir
os.makedirs(download_path, exist_ok=True)


# Função de renomear o arquivo para adicionar a data atual
def esperar_download_concluir(download_path, timeout=30):
    tempo_inicial = time.time()
    pasta = Path(download_path)
    arquivo_alvo = pasta / "altas_e_baixas.csv"
    while time.time() - tempo_inicial < timeout:
        if arquivo_alvo.exists() and arquivo_alvo.is_file():
            if arquivo_alvo.stat().st_size > 0:
                print("✓ Arquivo disponível!")
                return True
        
        print(". ", end="", flush=True)
        time.sleep(1)

def renomear_arquivo_altas(download_path):
    nome_original = "altas_e_baixas.csv"
    caminho_original = os.path.join(download_path, nome_original)

    # esperar_download_concluir(caminho_original)

    time.sleep(3)
    if os.path.exists(caminho_original):
        data = datetime.now().strftime("%d_%m_%Y")
        novo_nome = f"altas_e_baixas_{data}.csv"
        caminho_novo = os.path.join(download_path, novo_nome)

        os.rename(caminho_original, caminho_novo)
        logger.info(f"\n Arquivo renomeado para: {novo_nome}")
    else:
        logger.error(f"\n Arquivo {nome_original} não encontrado.")


def webdriver_configurations(download_path):
    logger.info("Iniciando configuração do driver")
    options = Options()
    options.browser_version = "140"
    options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
})
    options.add_argument("--headless=new")  # 👈 novo modo headless do Chrome
    options.add_argument("--window-size=1920,1080")  # Define tamanho da janela (evita bugs de layout)
    options.add_argument("--disable-gpu")
    return options



def click_download_btn(driver):
    # Verificação de ADS
    try:
        logger.info("Verificando se existe anuncio no inicio da pagina")
        anuncio = driver.find_element(By.ID, "OutOfPage")
        if anuncio != None:
            logger.info("Encontrado anuncio na página")
            driver.execute_script(""" 
        const element = document.getElementById("OutOfPage")
        if (element) {
            element.style.display = 'none'}
    """)
    except:
        logger.info("Não encontrei anuncio, seguindo execução")
    try:
        logger.info("Iniciando funçao de clicar no botão")
        btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "export_altas_e_baixas_mobile")))
        btn.click()
        logger.info("Botão encontrado e download realizado")
    except TimeoutException:
        logger.error("Não encontrou o formato mobile, tentando no formato Web")
        try:
            btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "export_altas_e_baixas")))
            btn.click()
            logger.info("encontrou o botão em formato web")
        except:
            logger.error('Não encontrou nem no Web, Encerrando execução')
            driver.quit()
            exit()


def execute_automation(url, download_path):
    logger.info("Iniciando fluxo da automação")
    options = webdriver_configurations(download_path)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Iniciando automação
    driver.get(url)
    driver.maximize_window()

    # Aguarda carregamento completo da tabela
    time.sleep(5)

    # Chama a função do download
    click_download_btn(driver)

    ## Renomeia o arquivo
    renomear_arquivo_altas(download_path)

    driver.close()

