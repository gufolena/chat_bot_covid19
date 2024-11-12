import customtkinter as ctk
import requests
import unicodedata
import re
import pyttsx3

class Chatbot:
    def __init__(self, master):
        self.master = master
        master.title("Artemis")
        master.geometry("600x500")

        # Configuração do ícone
        master.iconbitmap("vacinaa.ico")

        # Configuração do sintetizador de fala
        self.engine = pyttsx3.init()
        self.engine.say("Seja bem-vindo e bem-vinda ao chat bot de COVID19. Pergunte-me sobre dados de COVID-19 ")
        self.engine.runAndWait()

        # Configuração da janela
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=0)
        master.grid_rowconfigure(2, weight=0)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Texto inicial
        self.initial_text = ("Olá! Eu sou a Artemis, sua assistente virtual de COVID-19. "
                             "Pergunte-me sobre dados de COVID-19 com as seguintes opções:\n"
                             "1 - Para dados globais, digite: 'global'\n"
                             "2 - Para dados de um país específico, digite: 'nome_do_país' (ex.: 'Brazil' ou 'USA')\n"
                             "3 - Para dados históricos de um país, digite: 'histórico nome_do_país' (ex.: 'histórico Japan')\n"
                             "4 - Para dados de vacinação de um país, digite: 'vacinação nome_do_país' (ex.: 'vacinação Germany')\n\n"
                             "Observação: Certifique-se de escrever o nome dos países em inglês para garantir que os dados sejam exibidos corretamente.\n")

        # Área de texto
        self.text_area = ctk.CTkTextbox(master, width=500, height=300, wrap="word")
        self.text_area.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.text_area.insert(ctk.END, self.initial_text)
        self.text_area.configure(state="disabled")

        # Campo de entrada
        self.entry = ctk.CTkEntry(master, width=400, placeholder_text="Digite sua solicitação...")
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", self.process_input)

        # Botão de envio
        self.send_button = ctk.CTkButton(master, text="Enviar", fg_color="blue", command=self.process_input)
        self.send_button.grid(row=2, column=0, padx=20, pady=10)

        # Botão de limpar
        self.clear_button = ctk.CTkButton(master, text="Limpar", fg_color="green", command=self.clear_text_area)
        self.clear_button.grid(row=3, column=0, padx=20, pady=10)

    def process_input(self, event=None):
        user_input = self.entry.get()
        if not user_input:
            return

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "Você: " + user_input + "\n")
        self.text_area.yview(ctk.END)  # Rolagem automática para o final
        self.text_area.configure(state="disabled")

        # Processar a entrada do usuário
        response = self.get_response(user_input)

        self.text_area.configure(state="normal")
        self.text_area.insert(ctk.END, "Artemis: " + response + "\n")
        self.text_area.yview(ctk.END)
        self.text_area.configure(state="disabled")

        self.entry.delete(0, ctk.END)

    def clear_text_area(self):
        # Limpar a área de texto e reinserir o texto inicial
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", ctk.END)
        self.text_area.insert(ctk.END, self.initial_text)
        self.text_area.configure(state="disabled")

    def normalize_string(self, s):
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('utf-8').lower()

    def get_response(self, user_input):
        # Normalizar a entrada do usuário
        user_input_normalized = self.normalize_string(user_input)

        if user_input_normalized == "global":
            return self.get_global_data()

        elif user_input_normalized.startswith("por pais") or user_input_normalized.startswith("por país"):
            return "Para obter dados de um país específico, use o nome do país. Exemplo: 'Brasil'."

        elif user_input_normalized.startswith("historico") or user_input_normalized.startswith("histórico"):
            # Extrair o nome do país após o comando 'historico' ou 'histórico'
            match = re.search(r"historico ([\w\s]+)", user_input_normalized) or re.search(r"histórico ([\w\s]+)", user_input_normalized)
            if match:
                country = match.group(1)
                return self.get_country_history(country)
            else:
                return "Por favor, forneça o nome de um país após o comando 'histórico'."

        elif user_input_normalized.startswith("vacinacao") or user_input_normalized.startswith("vacinação"):
            # Extrair o nome do país após o comando 'vacinacao' ou 'vacinação'
            match = re.search(r"vacinacao ([\w\s]+)", user_input_normalized) or re.search(r"vacinação ([\w\s]+)", user_input_normalized)
            if match:
                country = match.group(1)
                return self.get_vaccination_data(country)
            else:
                return "Por favor, forneça o nome de um país após o comando 'vacinação'."

        elif user_input_normalized.isalpha():  # Assumimos que seja o nome de um país
            return self.get_country_data(user_input_normalized)

        return "Não entendi sua solicitação. Você pode perguntar sobre dados globais, de um país específico, histórico ou vacinação."

    def get_global_data(self):
        try:
            response = requests.get("https://disease.sh/v3/covid-19/all")
            data = response.json()
            return (f"Dados Globais de COVID-19:\n"
                    f"Casos: {data.get('cases', 'Dados indisponíveis')}\n"
                    f"Mortes: {data.get('deaths', 'Dados indisponíveis')}\n"
                    f"Recuperados: {data.get('recovered', 'Dados indisponíveis')}")
        except requests.exceptions.RequestException:
            return "Erro ao obter dados globais de COVID-19. Verifique sua conexão."

    def get_country_data(self, country):
        try:
            response = requests.get(f"https://disease.sh/v3/covid-19/countries/{country}")
            if response.status_code == 200:
                data = response.json()
                return (f"Dados de COVID-19 em {country.capitalize()}:\n"
                        f"Casos: {data.get('cases', 'Dados indisponíveis')}\n"
                        f"Mortes: {data.get('deaths', 'Dados indisponíveis')}\n"
                        f"Recuperados: {data.get('recovered', 'Dados indisponíveis')}")
            elif response.status_code == 404:
                return "País não encontrado. Verifique o nome e tente novamente."
            else:
                return "Erro ao obter dados para o país especificado."
        except requests.exceptions.RequestException:
            return "Erro ao acessar a API para dados de países. Verifique sua conexão."

    def get_country_history(self, country):
        try:
            response = requests.get(f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=30")
            if response.status_code == 200:
                data = response.json()
                timeline = data["timeline"]["cases"]
                history = "\n".join([f"{date}: {cases} casos" for date, cases in timeline.items()])
                return f"Histórico dos últimos 30 dias para {country.capitalize()}:\n{history}"
            elif response.status_code == 404:
                return "País não encontrado. Verifique o nome e tente novamente."
            else:
                return "Erro ao obter dados históricos para o país especificado."
        except requests.exceptions.RequestException:
            return "Erro ao acessar a API para dados históricos. Verifique sua conexão."

    def get_vaccination_data(self, country):
        try:
            response = requests.get(f"https://disease.sh/v3/covid-19/vaccine/coverage/countries/{country}?lastdays=1")
            if response.status_code == 200:
                data = response.json()
                country_name = data["country"]
                vaccinations = list(data["timeline"].values())[0]
                return f"Dados de vacinação para {country_name}:\nTotal de doses administradas: {vaccinations}"
            elif response.status_code == 404:
                return "País não encontrado. Verifique o nome e tente novamente."
            else:
                return "Erro ao obter dados de vacinação para o país especificado."
        except requests.exceptions.RequestException:
            return "Erro ao acessar a API para dados de vacinação. Verifique sua conexão."

if __name__ == "__main__":
    root = ctk.CTk()
    chatbot = Chatbot(root)
    root.mainloop()

