document.addEventListener('DOMContentLoaded', () => {
    const urlBase = "https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-horizon-projects-entities/records";
    const limit = 20;
    let currentPage = 0;
    let totalPages = 0;

    // Fonction pour créer une ligne de tableau
    function createRow(data) {
        const row = document.createElement('tr');

        const projectIdCell = document.createElement('td');
        projectIdCell.textContent = data.project_id || "N/A";
        row.appendChild(projectIdCell);

        const frameworkCell = document.createElement('td');
        frameworkCell.textContent = data.framework || "N/A";
        row.appendChild(frameworkCell);

        const countryCell = document.createElement('td');
        countryCell.textContent = data.country_name_en || "N/A";
        row.appendChild(countryCell);

        const entityNameCell = document.createElement('td');
        entityNameCell.textContent = data.entities_name || "N/A";
        row.appendChild(entityNameCell);

        const roleCell = document.createElement('td');
        roleCell.textContent = data.role || "N/A";
        row.appendChild(roleCell);

        return row;
    }

    // Fonction pour afficher les données dans le tableau
    function displayData(data) {
        const tableBody = document.querySelector('#data-table tbody');
        tableBody.innerHTML = ''; // Vider le corps du tableau avant de le remplir

        data.results.forEach(record => {
            const row = createRow(record);
            tableBody.appendChild(row);
        });

        document.getElementById('page-info').textContent = `Page ${currentPage + 1} de ${totalPages}`;
        document.getElementById('prev-page').disabled = currentPage === 0;
        document.getElementById('next-page').disabled = currentPage === totalPages - 1;
    }

    // Fonction pour récupérer les données de API et les afficher dans le tableau
    function fetchData(page) {
        const url = `${urlBase}?limit=${limit}&offset=${page * limit}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                totalPages = Math.ceil(data.total_count / limit);
                if (data.results) {
                    displayData(data);
                } else {
                    console.error('La structure des données n\'est pas celle attendue:', data);
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
            });
    }

    document.getElementById('prev-page').addEventListener('click', () => {
        if (currentPage > 0) {
            currentPage--;
            fetchData(currentPage);
        }
    });

    document.getElementById('next-page').addEventListener('click', () => {
        if (currentPage < totalPages - 1) {
            currentPage++;
            fetchData(currentPage);
        }
    });

    // Initial fetch
    fetchData(currentPage);
});
