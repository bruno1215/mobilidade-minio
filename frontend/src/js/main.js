document.addEventListener('DOMContentLoaded', () => {
    const analyzeButton = document.getElementById('analyzeButton');
    const resultsDiv = document.getElementById('results');
    const plotImage = document.getElementById('plotImage');
    const plotLinkContainer = document.getElementById('plotLinkContainer');
    const plotLink = document.getElementById('plotLink');
    const dataTableBody = document.querySelector('#dataTable tbody');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const errorMessageP = document.getElementById('errorMessage');

    // O backend estará em http://localhost:5000 se executado localmente via docker-compose
    // Se o frontend for servido pelo mesmo host/porta (ex: via proxy no Nginx), pode usar caminhos relativos.
    // Mas como são containers diferentes, é mais seguro usar a URL completa do host.
    const API_BASE_URL = 'http://localhost:5000/api'; // Ajuste se necessário

    analyzeButton.addEventListener('click', async () => {
        loadingDiv.style.display = 'block';
        errorDiv.style.display = 'none';
        resultsDiv.style.display = 'none';
        plotImage.style.display = 'none';
        plotLinkContainer.style.display = 'none';
        dataTableBody.innerHTML = ''; // Limpa a tabela

        try {
            const response = await fetch(`${API_BASE_URL}/analysis/passengers_by_neighborhood`);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
            }
            const data = await response.json();

            plotImage.src = data.plot_url; // MinIO presigned URL
            plotImage.style.display = 'block';

            plotLink.href = data.plot_url;
            plotLinkContainer.style.display = 'block';

            if (data.data && data.data.length > 0) {
                data.data.forEach(item => {
                    const row = dataTableBody.insertRow();
                    const cellBairro = row.insertCell();
                    const cellPassageiros = row.insertCell();
                    cellBairro.textContent = item.bairro;
                    cellPassageiros.textContent = item.passageiros;
                });
            }

            resultsDiv.style.display = 'block';
        } catch (err) {
            console.error("Erro ao buscar análise:", err);
            errorMessageP.textContent = err.message;
            errorDiv.style.display = 'block';
        } finally {
            loadingDiv.style.display = 'none';
        }
    });
});
