import requests
import random
import time
import threading
from flask import Flask

# ==============================
# CONFIGURAÇÃO
# ==============================

BASE_URL = "https://hot-academy-kappa.vercel.app/"

LANGS = [
    "pt-BR,pt;q=0.9", "en-US,en;q=0.9", "es-ES,es;q=0.9", "fr-FR,fr;q=0.9",
    "de-DE,de;q=0.9", "it-IT,it;q=0.9", "ja-JP,ja;q=0.9", "ko-KR,ko;q=0.9"
]

REFERERS = [
    "https://www.google.com/", "https://www.bing.com/", 
    "https://duckduckgo.com/", "https://facebook.com/", "https://t.co/", "https://x.com/"
]

# User-Agents Variados (Desktop e Mobile)
UA_LIST = [
# --- Windows Chrome (25) ---
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.0.0 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.0.0 Safari/537.36",

# --- Windows Firefox (15) ---
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:114.0) Gecko/20100101 Firefox/114.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:111.0) Gecko/20100101 Firefox/111.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:110.0) Gecko/20100101 Firefox/110.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",

# --- macOS (10) ---
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 Version/16.0 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 Version/15.0 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 Version/14.0 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 Version/13.0 Safari/605.1.15",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36",

# --- Linux (10) ---
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/113.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/112.0.0.0 Safari/537.36",
"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/111.0.0.0 Safari/537.36",

# --- Android (20) ---
"Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/119.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 Chrome/118.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 Chrome/117.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 10; Pixel 4) AppleWebKit/537.36 Chrome/116.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 9; Pixel 3) AppleWebKit/537.36 Chrome/115.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 8; Pixel 2) AppleWebKit/537.36 Chrome/114.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 7; Nexus 6P) AppleWebKit/537.36 Chrome/113.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 6; Nexus 5X) AppleWebKit/537.36 Chrome/112.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 5; Nexus 5) AppleWebKit/537.36 Chrome/111.0.0.0 Mobile Safari/537.36",

"Mozilla/5.0 (Linux; Android 14; Samsung S23) AppleWebKit/537.36 Chrome/110.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 13; Samsung S22) AppleWebKit/537.36 Chrome/109.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 12; Samsung S21) AppleWebKit/537.36 Chrome/108.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 11; Samsung S20) AppleWebKit/537.36 Chrome/107.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 10; Samsung S10) AppleWebKit/537.36 Chrome/106.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 9; Samsung S9) AppleWebKit/537.36 Chrome/105.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 8; Samsung S8) AppleWebKit/537.36 Chrome/104.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 7; Samsung S7) AppleWebKit/537.36 Chrome/103.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 6; Samsung S6) AppleWebKit/537.36 Chrome/102.0.0.0 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 5; Samsung S5) AppleWebKit/537.36 Chrome/101.0.0.0 Mobile Safari/537.36",

# --- iPhone (10) ---
"Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Version/16.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 Version/15.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 Version/14.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/605.1.15 Version/13.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 Version/12.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/605.1.15 Version/11.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 10_0 like Mac OS X) AppleWebKit/605.1.15 Version/10.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 9_0 like Mac OS X) AppleWebKit/605.1.15 Version/9.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/605.1.15 Version/8.0 Mobile/15E148 Safari/604.1",

# --- iPad (10) ---
"Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Version/16.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 Version/15.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15 Version/14.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPad; CPU OS 13_0 like Mac OS X) AppleWebKit/605.1.15 Version/13.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPad; CPU OS 12_0 like Mac OS X) AppleWebKit/605.1.15 Version/12.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/605.1.15 Version/11.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPad; CPU OS 10_0 like Mac OS X) AppleWebKit/605.1.15 Version/10.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPad; CPU OS 9_0 like Mac OS X) AppleWebKit/605.1.15 Version/9.0 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPad; CPU OS 8_0 like Mac OS X) AppleWebKit/605.1.15 Version/8.0 Mobile/15E148 Safari/604.1",
]

# ==============================
# FLASK (Para o Render manter o serviço vivo)
# ==============================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Turbo Camaleão: Online ✅", 200

@app.route("/health")
def health():
    return "OK", 200

# ==============================
# LÓGICA DO BOT
# ==============================

def montar_headers():
    return {
        "User-Agent": random.choice(UA_LIST),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": random.choice(LANGS),
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": random.choice(REFERERS),
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
    }

def visita():
    # Criar uma nova sessão (cookies novos) para cada visita
    sess = requests.Session()
    try:
        headers = montar_headers()
        
        # 1. Visita a Home com um parâmetro aleatório para evitar Cache
        url_final = f"{BASE_URL}?ref=search_{random.randint(100,999)}"
        response = sess.get(url_final, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Simular tempo de leitura (2 a 5 segundos)
            time.sleep(random.uniform(2, 5))
            
            # 2. Simular carregamento de um asset ou subpágina
            # Isso faz com que a sessão seja validada nos logs do servidor
            sess.get(f"{BASE_URL}favicon.ico", headers=headers, timeout=5)
            
            print(f"✅ Visita concluída com sucesso! Status: {response.status_code}")
        else:
            print(f"⚠️ Servidor respondeu com status: {response.status_code}")

    except Exception as e:
        print(f"❌ Erro durante a visita: {e}")
    finally:
        sess.close() # Finaliza a sessão e limpa cookies

def bot_loop():
    print("🚀 Iniciando loop de 4 acessos por minuto...")
    while True:
        inicio_minuto = time.time()

        # Define 4 momentos aleatórios dentro deste minuto
        momentos = sorted(random.uniform(0, 55) for _ in range(4))

        for m in momentos:
            agora = time.time() - inicio_minuto
            espera = m - agora
            if espera > 0:
                time.sleep(espera)
            
            # Executa a visita
            threading.Thread(target=visita).start()

        # Espera o minuto acabar para resetar o ciclo
        tempo_passado = time.time() - inicio_minuto
        if tempo_passado < 60:
            time.sleep(60 - tempo_passado)

# ==============================
# EXECUÇÃO
# ==============================

if __name__ == "__main__":
    # Inicia o bot em uma thread separada
    bot_thread = threading.Thread(target=bot_loop, daemon=True)
    bot_thread.start()
    
    # Inicia o servidor Flask na porta exigida pelo Render
    app.run(host="0.0.0.0", port=10000)
