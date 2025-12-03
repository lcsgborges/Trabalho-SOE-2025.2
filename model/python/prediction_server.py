# Servidor de Predição de Temperatura
# Baseado no loadproof.py - adaptado para ler dados do sensor BME280

import tensorflow as tf
import pandas as pd
import numpy as np
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import threading
import time

# Configurações
MODEL_24H_PATH = os.path.join(os.path.dirname(__file__), '..', 't24v1.keras')
MODEL_120H_PATH = os.path.join(os.path.dirname(__file__), '..', 't120v1.keras')
DATA_CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'database', 'data.csv')

# Constantes do modelo (devem corresponder ao treinamento)
CONV_WIDTH = 3
INPUT_WIDTH = 120  # Janela de entrada esperada pelo modelo
OUT_STEPS_24H = 24
OUT_STEPS_120H = 120

# Variáveis globais para cache
model_24h = None
model_120h = None
last_predictions = {
    "temp_24h": None,
    "temp_120h": None,
    "timestamp": None,
    "status": "not_ready",
    "message": "Aguardando dados suficientes"
}

def load_testing_csv(range: list = None) -> pd.DataFrame :
    df.read_csv(MINICSV)
    if(range != None):
        df = df[range[0]:range[1]]

    return df

def load_models():
    """Carrega os modelos Keras"""
    global model_24h, model_120h
    
    tf.keras.config.enable_unsafe_deserialization()
    
    try:
        if os.path.exists(MODEL_24H_PATH):
            model_24h = tf.keras.models.load_model(MODEL_24H_PATH)
            print(f"[OK] Modelo 24h carregado: {MODEL_24H_PATH}")
        else:
            print(f"[AVISO] Modelo 24h não encontrado: {MODEL_24H_PATH}")
    except Exception as e:
        print(f"[ERRO] Falha ao carregar modelo 24h: {e}")
    
    try:
        if os.path.exists(MODEL_120H_PATH):
            model_120h = tf.keras.models.load_model(MODEL_120H_PATH)
            print(f"[OK] Modelo 120h carregado: {MODEL_120H_PATH}")
        else:
            print(f"[AVISO] Modelo 120h não encontrado: {MODEL_120H_PATH}")
    except Exception as e:
        print(f"[ERRO] Falha ao carregar modelo 120h: {e}")

def read_sensor_data():
    """
    Lê os dados do CSV do sensor BME280
    Formato esperado: Date,Time,Temperature,Pressure,Humidity
    """
    if not os.path.exists(DATA_CSV_PATH):
        print(f"[ERRO] Arquivo não encontrado: {DATA_CSV_PATH}")
        return None
    
    try:
        df = pd.read_csv(DATA_CSV_PATH)
        
        if df.empty:
            print("[AVISO] CSV vazio")
            return None
        
        # Verificar se tem a coluna de temperatura
        # O CSV do sensor tem: Date,Time,Temperature,Pressure,Humidity
        temp_col = None
        for col in df.columns:
            if 'temp' in col.lower():
                temp_col = col
                break
        
        if temp_col is None:
            # Tentar pela posição (terceira coluna)
            if len(df.columns) >= 3:
                temp_col = df.columns[2]
            else:
                print("[ERRO] Coluna de temperatura não encontrada")
                return None
        
        temperatures = df[temp_col].values.astype(float)
        return temperatures
    
    except Exception as e:
        print(f"[ERRO] Falha ao ler CSV: {e}")
        return None

def prepare_input_data(temperatures, input_size=120):
    """
    Prepara os dados de temperatura para entrada no modelo.
    
    O modelo espera 3 colunas (Temp Ins, Temp Max, Temp Min).
    Como o sensor BME280 só fornece uma temperatura, vamos:
    - Usar a temperatura atual como Temp Ins
    - Calcular Temp Max como máximo em janela móvel
    - Calcular Temp Min como mínimo em janela móvel
    """
    if len(temperatures) < input_size:
        print(f"[AVISO] Dados insuficientes: {len(temperatures)}/{input_size}")
        return None, None, None
    
    # Pegar as últimas 'input_size' leituras
    temps = temperatures[-input_size:]
    
    # Criar as 3 features simuladas
    # Para uma aproximação, usamos janelas móveis
    window_size = min(24, len(temps))  # Janela de 24 horas ou menos
    
    temp_ins = temps  # Temperatura instantânea
    
    # Calcular max/min em janela móvel
    temp_max = np.array([
        np.max(temps[max(0, i-window_size):i+1]) 
        for i in range(len(temps))
    ])
    temp_min = np.array([
        np.min(temps[max(0, i-window_size):i+1]) 
        for i in range(len(temps))
    ])
    
    # Empilhar as 3 features: shape (input_size, 3)
    inp = np.column_stack([temp_ins, temp_min, temp_max])
    
    # Normalizar
    mean = inp.mean()
    std = inp.std()
    
    if std == 0:
        std = 1  # Evitar divisão por zero
    
    inp_normalized = (inp - mean) / std
    
    # Reshape para batch: (1, input_size, 3)
    inp_batch = inp_normalized.reshape(1, input_size, 3)
    
    return inp_batch, mean, std

def make_predictions():
    """Faz as predições usando os modelos carregados"""
    global last_predictions
    
    temperatures = read_sensor_data()
    
    if temperatures is None or len(temperatures) < INPUT_WIDTH:
        last_predictions = {
            "temp_24h": None,
            "temp_120h": None,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "insufficient_data",
            "message": f"Dados insuficientes: {len(temperatures) if temperatures is not None else 0}/{INPUT_WIDTH} leituras necessárias"
        }
        return last_predictions
    
    inp_batch, mean, std = prepare_input_data(temperatures, INPUT_WIDTH)
    
    if inp_batch is None:
        last_predictions["status"] = "error"
        last_predictions["message"] = "Erro ao preparar dados"
        return last_predictions
    
    pred_24h = None
    pred_120h = None
    
    # Predição 24 horas
    if model_24h is not None:
        try:
            predictions_24h = model_24h.predict(inp_batch, verbose=0)
            # Desnormalizar
            predictions_24h = (predictions_24h * std) + mean
            # Pegar média da predição (ou o primeiro valor)
            pred_24h = float(np.mean(predictions_24h[0, :, 0]))  # Média da Temp Ins prevista
            print(f"[OK] Predição 24h: {pred_24h:.2f}°C")
        except Exception as e:
            print(f"[ERRO] Predição 24h falhou: {e}")
    
    # Predição 120 horas
    if model_120h is not None:
        try:
            predictions_120h = model_120h.predict(inp_batch, verbose=0)
            # Desnormalizar
            predictions_120h = (predictions_120h * std) + mean
            # Pegar média da predição
            pred_120h = float(np.mean(predictions_120h[0, :, 0]))  # Média da Temp Ins prevista
            print(f"[OK] Predição 120h: {pred_120h:.2f}°C")
        except Exception as e:
            print(f"[ERRO] Predição 120h falhou: {e}")
    
    last_predictions = {
        "temp_24h": round(pred_24h, 2) if pred_24h else None,
        "temp_120h": round(pred_120h, 2) if pred_120h else None,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ok" if (pred_24h or pred_120h) else "error",
        "message": "Predições atualizadas com sucesso",
        "data_points": len(temperatures)
    }
    
    return last_predictions

class PredictionHandler(BaseHTTPRequestHandler):
    """Handler HTTP para servir as predições"""
    
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()
    
    def do_GET(self):
        if self.path == "/api/predict" or self.path == "/predict":
            self._set_headers()
            # Fazer nova predição
            predictions = make_predictions()
            self.wfile.write(json.dumps(predictions).encode())
        
        elif self.path == "/api/status" or self.path == "/status":
            self._set_headers()
            status = {
                "server": "running",
                "model_24h": model_24h is not None,
                "model_120h": model_120h is not None,
                "data_path": DATA_CSV_PATH,
                "last_predictions": last_predictions
            }
            self.wfile.write(json.dumps(status).encode())
        
        elif self.path == "/":
            self._set_headers("text/html")
            html = """
            <html>
            <head><title>Servidor de Predicao</title></head>
            <body>
                <h1>Servidor de Predicao de Temperatura</h1>
                <p>Endpoints disponiveis:</p>
                <ul>
                    <li><a href="/api/predict">/api/predict</a> - Obter predicoes</li>
                    <li><a href="/api/status">/api/status</a> - Status do servidor</li>
                </ul>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
    
    def log_message(self, format, *args):
        print(f"[HTTP] {args[0]}")

def run_server(port=5000):
    """Inicia o servidor HTTP"""
    server_address = ("", port)
    httpd = HTTPServer(server_address, PredictionHandler)
    print(f"[OK] Servidor de predicao rodando em http://localhost:{port}")
    print(f"     Endpoints: /api/predict, /api/status")
    httpd.serve_forever()

if __name__ == "__main__":
    print("=" * 50)
    print("Servidor de Predicao de Temperatura - BME280 + IA")
    print("=" * 50)
    
    # Carregar modelos
    load_models()
    
    # Fazer predição inicial
    print("\n[INFO] Fazendo predicao inicial...")
    make_predictions()
    
    # Iniciar servidor
    print("\n[INFO] Iniciando servidor HTTP...")
    run_server(port=5000)
