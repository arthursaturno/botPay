import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import tempfile
import time
import psutil
import threading  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class AppGUI:
    def __init__(self):
        self.open_processes = []
        self.name_counter = 1 
        self.root = tk.Tk()
        self.root.title("botPay")
        self.root.geometry("400x400")
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal para organizar os widgets
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Fonte para reduzir a altura das caixas de entrada
        small_font = ("Arial", 10)

        # Campo para o nome de usuário
        tk.Label(main_frame, text="Usuário:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(main_frame, font=small_font, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)

        # Campo para a senha
        tk.Label(main_frame, text="Senha:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(main_frame, font=small_font, width=30)
        self.password_entry.grid(row=1, column=1, pady=5)

        # Campo para confirmar a senha
        tk.Label(main_frame, text="Senha2:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.confirm_password_entry = tk.Entry(main_frame, font=small_font, width=30)
        self.confirm_password_entry.grid(row=2, column=1, pady=5)

        # Campo para o nome completo
        tk.Label(main_frame, text="Nome:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
        self.full_name_entry = tk.Entry(main_frame, font=small_font, width=30)
        self.full_name_entry.grid(row=3, column=1, pady=5)

        # Campo para o número de instâncias
        tk.Label(main_frame, text="Instâncias:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)

        # Spinbox otimizado
        self.num_browsers_spinbox = tk.Spinbox(
            main_frame,
            from_=1,  # Valor mínimo
            to=10,    # Valor máximo
            font=("Arial", 10),  # Fonte menor
            width=5,  # Largura ajustada
            justify="center"  # Texto centralizado
        )
        self.num_browsers_spinbox.grid(row=4, column=1, pady=5)
        
        # Campo para o site
        tk.Label(main_frame, text="Site:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", pady=5)
        self.url_entry = tk.Entry(main_frame, font=small_font, width=30)
        self.url_entry.grid(row=5, column=1, pady=5)

        # Campo para a senha de saque
        tk.Label(main_frame, text="Senha Saque:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", pady=5)
        self.withdraw_password_entry = tk.Entry(main_frame, font=small_font, width=30)
        self.withdraw_password_entry.grid(row=6, column=1, pady=5)

        tk.Label(main_frame, text="Senha Saque2:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", pady=5)
        self.confirm_withdraw_password_entry = tk.Entry(main_frame, font=small_font, width=30)
        self.confirm_withdraw_password_entry.grid(row=7, column=1, pady=5)

        # Botões de abrir e fechar
        button_frame = tk.Frame(main_frame, pady=10)
        button_frame.grid(row=8, column=0, columnspan=2)

        open_chrome_button = tk.Button(button_frame, text="Abrir", font=("Arial", 12), command=self.open_chrome)
        open_chrome_button.pack(side=tk.LEFT, padx=10)

        close_chrome_button = tk.Button(button_frame, text="Fechar", font=("Arial", 12), command=self.close_chrome)
        close_chrome_button.pack(side=tk.LEFT, padx=10)

    def close_chrome(self):
        try:
            if not self.open_processes:
                messagebox.showinfo("Informação", "Não há janelas do bot abertas.")
                return

            for process in self.open_processes:
                try:
                    pid = process["process"].pid
                    p = psutil.Process(pid)
                    p.terminate()
                except psutil.NoSuchProcess:
                    continue

            self.open_processes.clear()
            messagebox.showinfo("Informação", "Todos os navegadores foram fechados com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar fechar as janelas do Chrome.\n{e}")

    def open_chrome(self):
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()
            confirm_password = self.confirm_password_entry.get()
            full_name = self.full_name_entry.get()
            withdraw_password = self.withdraw_password_entry.get() 

            if not all([username, password, confirm_password, full_name, withdraw_password]): 
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
                return

            if password != confirm_password:
                messagebox.showerror("Erro", "As senhas não coincidem.")
                return

            num_browsers = int(self.num_browsers_spinbox.get())
            url_input = self.url_entry.get()

            if not url_input.startswith("http://") and not url_input.startswith("https://"):
                url_input = "https://" + url_input

            chrome_path = r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            if os.path.exists(chrome_path):
                threads = [] 
                for i in range(num_browsers):
                    username_with_number = f"{username}{self.name_counter}"

                    temp_dir = tempfile.mkdtemp()
                    window_size = "360,640"
                    user_agent = "Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Mobile Safari/537.36"
                    debug_port = 9222 + i

                    process = subprocess.Popen([chrome_path, "--new-window", "--incognito", f"--user-data-dir={temp_dir}",
                                                f"--remote-debugging-port={debug_port}", f"--window-size={window_size}",
                                                f"--user-agent={user_agent}", f"--app={url_input}", "--disable-infobars"])

                    time.sleep(2)
                    self.open_processes.append({"process": process, "port": debug_port})

                    thread = threading.Thread(target=self.fill_registration_forms, args=(url_input, username_with_number, password, full_name, debug_port, withdraw_password))
                    threads.append(thread)
                    thread.start()  
                    self.name_counter += 1

                for thread in threads:
                    thread.join()

                #  messagebox.showinfo("Sucesso", "Cadastro realizado em todas as instâncias!")
            else:
                messagebox.showerror("Erro", "O Chrome não foi encontrado no caminho especificado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao tentar abrir o Chrome.\n{e}")



    def fill_registration_forms(self, url, username, password, full_name, debug_port, withdraw_password):
        try:
            options = Options()
            options.add_experimental_option("debuggerAddress", f"localhost:{debug_port}")
            driver = webdriver.Chrome(options=options)

            driver.get(url)

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, '_itemContent_cavdu_42')]//span[text()='Perfil']")))
            profile_button = driver.find_element(By.XPATH, "//div[contains(@class, '_itemContent_cavdu_42')]//span[text()='Perfil']")
            profile_button.click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-input-name='account']")))

            driver.find_element(By.CSS_SELECTOR, "input[data-input-name='account']").send_keys(username)
            driver.find_element(By.CSS_SELECTOR, "input[data-input-name='userpass']").send_keys(password)
            driver.find_element(By.CSS_SELECTOR, "input[data-input-name='confirmPassword']").send_keys(password)
            driver.find_element(By.CSS_SELECTOR, "input[data-input-name='realName']").send_keys(full_name)

            register_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ui-button--primary') and .//span[text()='Registro']]"))
            )
            register_button.click()

            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ui-popup') and .//h3[text()='Registrado com sucesso']]"))
            )

            time.sleep(2)

            close_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//i[@class='ui-dialog-close-box__icon']"))
            )
            close_button.click()

            WebDriverWait(driver, 10).until(EC.invisibility_of_element(close_button))
            time.sleep(1) 

            try:
                close_popup_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "_close_c6t8a_74"))
                )
                close_popup_button.click()
                print("Pop-up fechado com sucesso.")
                
                close_dialog_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "ui-dialog-close-box__icon"))
                )
                close_dialog_button.click()
                print("Dialog fechado com sucesso.")
                
                confirm_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[8]/div/div[1]/div[3]/button"))
                )
                confirm_button.click()
                
                print("Ação confirmada com sucesso.")
                
            except NoSuchElementException:
                print("Nenhum pop-up encontrado, continuando o processo.")
                
            except TimeoutException:
                print("O tempo de espera para fechar o pop-up expirou, continuando o processo.")

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//p[contains(@class, '_label_28b5j_62') and text()='Saques']"))
            )

            withdraw_button = driver.find_element(By.XPATH, "//p[contains(@class, '_label_28b5j_62') and text()='Saques']")
            withdraw_button.click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lobby-form-item--withdrawPass"))
            )

            withdraw_pass_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lobby-form-item--withdrawPass"))
            ).find_element(By.TAG_NAME, "input")
            withdraw_pass_field.send_keys(withdraw_password)

            confirm_pass_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lobby-form-item--confirmWithdrawPass"))
            ).find_element(By.TAG_NAME, "input")
            confirm_pass_field.send_keys(withdraw_password)

            print("Senha para saque preenchida com sucesso.")

            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ui-button') and .//span[text()='Confirmar']]"))
            )
            confirm_button.click()

            print("Botão 'Confirmar' clicado com sucesso.")

            add_account_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "_addAccountInputBtn_1o4yf_17"))
            )
            add_account_button.click()

            print("Botão 'Adicionar Conta' clicado com sucesso.")

            add_pix_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "_cell_13fxl_24"))
            )
            add_pix_button.click()

            print("Botão 'Adicionar Pix' clicado com sucesso.")

            withdraw_pass_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "_form_1xh6r_17"))
            ).find_element(By.TAG_NAME, "input")
            withdraw_pass_field.send_keys(withdraw_password)
            
            driver.execute_script("arguments[0].scrollIntoView();", withdraw_pass_field)

            # Espera até que o botão 'Próximo' esteja visível e clicável
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']//span[text()='Próximo']"))
            )

            driver.execute_script("arguments[0].click();", next_button)
            print("Botão 'Próximo' clicado com sucesso.")
                
        except Exception as e:
            print(f"Erro ao preencher o formulário ou clicar em botões: {e}")

   
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AppGUI()
    app.run() 