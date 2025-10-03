let updateInterval;

        function updateStatus(status) {
            const statusDot = document.getElementById('statusDot');
            const statusText = document.getElementById('statusText');
            
            statusDot.className = 'status-dot';
            
            switch(status) {
                case 'online':
                    statusDot.classList.add('online');
                    statusText.textContent = 'Online';
                    break;
                case 'offline':
                    statusDot.classList.add('offline');
                    statusText.textContent = 'Offline';
                    break;
                case 'error':
                    statusDot.classList.add('error');
                    statusText.textContent = 'Erro';
                    break;
                default:
                    statusDot.classList.add('offline');
                    statusText.textContent = 'Desconectado';
            }
        }

        function updateData(data) {
            updateStatus(data.status);
            document.getElementById('temperature').textContent = data.temperature || '--';
            document.getElementById('pressure').textContent = data.pressure || '--';
            document.getElementById('humidity').textContent = data.humidity || '--';
            document.getElementById('lastUpdate').textContent = `Última atualização: ${data.timestamp || '--'}`;
        }

        function fetchData() {
            fetch('/api/data')
                .then(response => response.json())
                .then(data => updateData(data))
                .catch(error => updateStatus('error'));
        }

        function startSensor() {
            fetch('/api/start')
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    if (data.success) {
                        startAutoUpdate();
                    }
                })
                .catch(error => alert('Erro ao iniciar: ' + error.message));
        }

        function stopSensor() {
            fetch('/api/stop')
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    if (data.success) {
                        stopAutoUpdate();
                        updateStatus('offline');
                    }
                })
                .catch(error => alert('Erro ao parar: ' + error.message));
        }

        function startAutoUpdate() {
            fetchData();
            updateInterval = setInterval(fetchData, 10000);
        }

        function stopAutoUpdate() {
            if (updateInterval) {
                clearInterval(updateInterval);
            }
        }

        // Inicia automaticamente quando a página carrega
        document.addEventListener('DOMContentLoaded', startAutoUpdate);