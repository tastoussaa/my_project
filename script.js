document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const datasetInfoSection = document.getElementById('dataset-info');
    const cleanedDataSection = document.getElementById('cleaned-data');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        })   
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Afficher les informations générales
                const info = data.info;
                datasetInfoSection.innerHTML = `
                    <h3>Informations Générales</h3>
                    <p>Lignes : ${info.numRows}</p>
                    <p>Colonnes : ${info.numCols}</p>
                    <h4>Noms des Colonnes et Types</h4>
                    <ul>
                        ${info.columns.map((col, index) => `<li>${col} : ${info.dtypes[index]}</li>`).join('')}
                    </ul>
                `;
        
                // Afficher un lien pour télécharger le fichier nettoyé
                cleanedDataSection.innerHTML = `
                    <h3>Données Nettoyées</h3>
                    <a href="${data.cleaned_file}" download>Télécharger les données nettoyées</a>
                `;
            } else {
                alert(data.message);
            }
        })
        
        .catch(error => console.error('Erreur:', error));
    });
});

function createBubbles() {
    const bubbleCount = 20; // Nombre de bulles
    const container = document.body;

    for (let i = 0; i < bubbleCount; i++) {
        const bubble = document.createElement('div');
        bubble.classList.add('bubble');
        const size = Math.random() * 50 + 20; // Taille aléatoire entre 20px et 70px
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        bubble.style.left = `${Math.random() * 100}vw`; // Positionnement horizontal aléatoire
        bubble.style.bottom = `${Math.random() * 100}vh`; // Positionnement vertical aléatoire
        bubble.style.animationDuration = `${Math.random() * 5 + 5}s`; // Durée aléatoire de l'animation
        container.appendChild(bubble);
    }
}

window.onload = function() {
    createBubbles(); // Crée les bulles après que la page est chargée
};