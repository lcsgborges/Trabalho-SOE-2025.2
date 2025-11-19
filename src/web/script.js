const table = document.querySelector("#sensorTable tbody");
const MAX_ROWS = 15;

async function attData() {
    try {
        // Busca o arquivo CSV do mesmo servidor (path relativo)
        const response = await fetch("/data.csv");
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const text = await response.text();
        
        if (!text || text.trim() === "") {
            console.warn("CSV vazio");
            return;
        }
        
        const rows = text.trim().split("\n");
        
        // Separar cabeçalho e dados
        let header = null;
        let dataRows = [];
        
        rows.forEach((row, idx) => {
            const data = row.split(",");
            if (idx === 0 && data[0].toLowerCase() === "date") {
                header = row; // Guardar cabeçalho
            } else {
                dataRows.push(row);
            }
        });

        // Pegar as últimas MAX_ROWS linhas
        const last_rows = dataRows.slice(-MAX_ROWS);
        
        // INVERTER para mostrar as mais recentes primeiro
        last_rows.reverse();

        table.innerHTML = "";

        last_rows.forEach((row) => {
            const data = row.split(",");
            const tr = document.createElement("tr");

            data.forEach(cell => {
                const td = document.createElement("td");
                td.textContent = cell.trim();
                tr.appendChild(td);
            })
            table.appendChild(tr);
        })
        
        console.log(`Tabela atualizada com sucesso - ${last_rows.length} linhas (mais recentes primeiro)`);
    } catch(err) {
        console.error("Erro ao ler CSV: ", err);
        // Mostrar mensagem de erro na tabela
        table.innerHTML = '<tr><td colspan="5" style="text-align:center; color:red;">Erro ao carregar dados. Verifique se o servidor está rodando.</td></tr>';
    }
}

// Atualiza a cada 10 segundos
setInterval(attData, 10000);

// Primeira carga
attData();


