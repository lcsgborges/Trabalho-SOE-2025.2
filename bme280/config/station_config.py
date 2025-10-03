"""
Configurações da Estação Meteorológica BME280
Arquivo centralizado de configurações do sistema.
"""

# Configurações do Sensor BME280
SENSOR_CONFIG = {
    'address': 0x76,           # Endereço I2C do sensor
    'i2c_bus': 1,              # Barramento I2C
    'collect_interval': 60,    # Intervalo de coleta em segundos
    'retry_attempts': 3,       # Tentativas de reconexão
    'retry_delay': 5,          # Delay entre tentativas em segundos
}

# Configurações do Servidor Web
SERVER_CONFIG = {
    'host': '0.0.0.0',         # Host do servidor
    'port': 5000,              # Porta do servidor
    'debug': False,            # Modo debug
    'threaded': True,          # Servidor multi-thread
    'use_reloader': False,     # Não usar reloader automático
}

# Configurações de Logging
LOGGING_CONFIG = {
    'level': 'INFO',           # Nível de log
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file': 'logs/bme280.log', # Arquivo de log
    'max_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5,         # Número de arquivos de backup
}

# Configurações do Sistema
SYSTEM_CONFIG = {
    'pid_file': '/var/run/bme280-station.pid',
    'service_name': 'bme280-station',
    'user': 'pi',
    'group': 'pi',
    'i2c_group': 'i2c',
}

# Configurações da Interface Web
UI_CONFIG = {
    'title': 'Estação Meteorológica BME280',
    'update_interval': 10,     # Intervalo de atualização da UI em segundos
    'timeout': 30,             # Timeout de conexão em segundos
    'theme': {
        'primary_color': '#667eea',
        'secondary_color': '#764ba2',
        'success_color': '#4CAF50',
        'error_color': '#f44336',
        'warning_color': '#ff9800',
    }
}

# Configurações de Rede
NETWORK_CONFIG = {
    'discovery_port': 5001,    # Porta para descoberta de rede
    'broadcast_interval': 30,  # Intervalo de broadcast em segundos
    'timeout': 5,              # Timeout de rede em segundos
}

# Configurações de Dados
DATA_CONFIG = {
    'history_size': 1000,      # Tamanho do histórico em memória
    'backup_interval': 3600,   # Intervalo de backup em segundos
    'export_formats': ['json', 'csv'],  # Formatos de exportação
}

# Configurações de Segurança
SECURITY_CONFIG = {
    'enable_auth': False,      # Habilitar autenticação
    'session_timeout': 3600,   # Timeout de sessão em segundos
    'max_connections': 100,    # Máximo de conexões simultâneas
    'rate_limit': 60,          # Limite de requisições por minuto
}

# Configurações de Monitoramento
MONITORING_CONFIG = {
    'health_check_interval': 30,  # Intervalo de verificação de saúde
    'alert_thresholds': {
        'temperature_min': -10,   # Temperatura mínima em °C
        'temperature_max': 60,    # Temperatura máxima em °C
        'humidity_min': 0,        # Umidade mínima em %
        'humidity_max': 100,      # Umidade máxima em %
        'pressure_min': 800,      # Pressão mínima em hPa
        'pressure_max': 1200,     # Pressão máxima em hPa
    },
    'enable_alerts': False,    # Habilitar alertas
    'alert_email': None,       # Email para alertas
}

# Configurações de Performance
PERFORMANCE_CONFIG = {
    'max_workers': 4,          # Máximo de workers
    'queue_size': 100,         # Tamanho da fila
    'cache_size': 1000,        # Tamanho do cache
    'gc_interval': 300,        # Intervalo de garbage collection em segundos
}

# Configurações de Desenvolvimento
DEV_CONFIG = {
    'enable_debug': False,     # Habilitar modo debug
    'enable_profiling': False, # Habilitar profiling
    'log_level': 'DEBUG',      # Nível de log para desenvolvimento
    'auto_reload': False,      # Auto-reload em desenvolvimento
}

# Função para obter configuração completa
def get_config():
    """Retorna todas as configurações em um dicionário"""
    return {
        'sensor': SENSOR_CONFIG,
        'server': SERVER_CONFIG,
        'logging': LOGGING_CONFIG,
        'system': SYSTEM_CONFIG,
        'ui': UI_CONFIG,
        'network': NETWORK_CONFIG,
        'data': DATA_CONFIG,
        'security': SECURITY_CONFIG,
        'monitoring': MONITORING_CONFIG,
        'performance': PERFORMANCE_CONFIG,
        'dev': DEV_CONFIG,
    }

# Função para validar configurações
def validate_config():
    """Valida se as configurações estão corretas"""
    errors = []
    
    # Validações básicas
    if SENSOR_CONFIG['collect_interval'] < 1:
        errors.append("Intervalo de coleta deve ser >= 1 segundo")
    
    if SERVER_CONFIG['port'] < 1024 and not (SERVER_CONFIG['port'] in [80, 443]):
        errors.append("Porta do servidor deve ser >= 1024 ou 80/443")
    
    if SENSOR_CONFIG['address'] < 0x08 or SENSOR_CONFIG['address'] > 0x77:
        errors.append("Endereço I2C deve estar entre 0x08 e 0x77")
    
    return errors

# Função para obter configuração específica
def get_config_value(section, key, default=None):
    """Obtém valor específico de configuração"""
    config = get_config()
    return config.get(section, {}).get(key, default)
