from gui.app_gui import AppGUI

def main():
    """
    Função principal para iniciar o aplicativo.
    """
    print("Iniciando o Bot Automático...")
    
    # Instancia o aplicativo GUI
    app = AppGUI()
    
    # Executa o loop principal da interface
    app.run()

if __name__ == "__main__":
    main()
