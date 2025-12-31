// Função para atualizar a página com novo limite de jogos
function updateLimit() {
    const selector = document.getElementById('limit-selector');
    const limit = selector.value;
    window.location.href = `/?limit=${limit}`;
}

// Função para criar uma grade 5x5 da cartela
function createCartelaGrid(numeros, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '';

    // Criar grade 5x5
    for (let i = 1; i <= 25; i++) {
        const cell = document.createElement('div');
        cell.className = 'cartela-cell';
        cell.textContent = i;

        // Marcar se o número foi sorteado
        if (numeros.includes(i)) {
            cell.classList.add('selected');
        }

        container.appendChild(cell);
    }
}

// Inicializar grades quando a página carregar
document.addEventListener('DOMContentLoaded', function () {
    // Definir o valor correto no seletor
    const urlParams = new URLSearchParams(window.location.search);
    const currentLimit = urlParams.get('limit') || '15';
    const selector = document.getElementById('limit-selector');
    if (selector) {
        selector.value = currentLimit;
    }
});
