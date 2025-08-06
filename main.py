import os
from src.report_download import execute_automation, logger, download_path, url

def main():
    # Cria a pasta se ela não existir
    os.makedirs(download_path, exist_ok=True)
    
    try:
        execute_automation(url, download_path)            
    except Exception as e:
        logger.critical(f"Erro crítico na execução principal: {e}", exc_info=True)
        exit(1)

if __name__ == "__main__":
    main()