const table = document.querySelector("#sensorTable tbody");
const MAX_ROWS = 15;

// URL base do servidor (ajuste se necessário)
const SERVER_URL = "http://localhost:8080";

async function attData() {
    try {
        // Busca o arquivo CSV do servidor
        const response = await fetch(`${SERVER_URL}/data.csv`);
        const text = await response.text();
        const rows = text.trim().split("\n");

        table.innerHTML = "";

        const last_rows = rows.slice(-MAX_ROWS);

        last_rows.forEach((row, idx) => {
            const data = row.split(",");

            if (idx == 0 && data[0].toLowerCase() === "date") return;

            const tr = document.createElement("tr");

            data.forEach(cell => {
                const td = document.createElement("td");
                td.textContent = cell;
                tr.appendChild(td);
            })
            table.appendChild(tr);
        })
        
        console.log("Tabela atualizada com sucesso");
    } catch(err) {
        console.error("Erro ao ler CSV: ", err);
    }
}

// Atualiza a cada 10 segundos
setInterval(attData, 10000);

attData();
