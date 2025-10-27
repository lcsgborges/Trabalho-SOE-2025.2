const table = document.querySelector("#sensorTable tbody");
const MAX_ROWS = 15;

async function attData() {
    try {
        const response = await fetch("../database/data.csv");
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
    } catch(err) {
        console.error("Erro ao ler CSV: ", err);
    }
}

setInterval(attData, 60000);

attData();