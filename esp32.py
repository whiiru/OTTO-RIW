import requests
from google import genai
from google.genai import types

# 1. Configurações Iniciais
API_KEY = "" # chave da API
ESP32_IP = "" # Exemplo: http://192.168.1.15, TEM QUE ESTAR CONECTADO NA MESMA REDE

# Inicializa o novo cliente oficial do Gemini
client = genai.Client(api_key=API_KEY)

# 2. Configurando o comportamento estrito do LLM
system_instruction = """
Você é um assistente de automação residencial. Seu único objetivo é analisar o comando do usuário e decidir se ele quer ligar ou desligar a luz.
Responda EXATAMENTE com uma das duas palavras, sem pontuação extra e sem texto adicional:
- LIGAR (se o usuário indicar que quer luz, clarear o ambiente, acender, etc)
- "DESLIGAR" (se o usuário quiser escuro, apagar, dormir, etc)
"""

def enviar_comando_esp32(acao):
    """Envia a requisição HTTP GET para o ESP32."""
    url = ""
    if acao == "LIGAR":
        url = f"{ESP32_IP}/led/on"
    elif acao == "DESLIGAR":
        url = f"{ESP32_IP}/led/off"
    else:
        print(f"Ação não reconhecida pelo sistema: {acao}")
        return

    try:
        print(f"Enviando pacote HTTP para: {url} ...")
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"Sucesso: {response.text}")
        else:
            print(f"Erro na requisição. Código: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Falha na comunicação de rede com o ESP32: {e}")

def main():
    print("=== Sistema LLM para ESP32 Iniciado (Novo SDK) ===")
    print("Digite seu comando (ex: 'Está muito escuro aqui' ou 'to indo dormir')")
    
    while True:
        comando_usuario = input("\nSeu comando: ")
        
        if comando_usuario.lower() in ['sair', 'exit', 'quit']:
            break

        try:
            # chamada da API do Gemini
            resposta = client.models.generate_content(
                model='gemini-2.5-flash', # Usando a versão Flash mais recente
                contents=comando_usuario,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=1.0 # Temperatura para respostas, varia de 0.0 a 2.0, sendo 0 o mais deterministico possivel
                )
            )
            
            decisao = resposta.text.strip().upper()
            print(f"[LLM Decidiu]: {decisao}")
            
            # Executa a ação na rede local
            enviar_comando_esp32(decisao)
            
        except Exception as e:
            print(f"\nErro ao processar com o Gemini: {e}")

if __name__ == "__main__":
    main()