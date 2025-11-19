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

        table.innerHTML = "";

        const last_rows = rows.slice(-MAX_ROWS);

        last_rows.forEach((row, idx) => {
            const data = row.split(",");

            // Ignorar linha de cabeçalho
            if (idx == 0 && data[0].toLowerCase() === "date") return;

            const tr = document.createElement("tr");

            data.forEach(cell => {
                const td = document.createElement("td");
                td.textContent = cell.trim();
                tr.appendChild(td);
            })
            table.appendChild(tr);
        })
        
        console.log(`Tabela atualizada com sucesso - ${last_rows.length} linhas`);
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

