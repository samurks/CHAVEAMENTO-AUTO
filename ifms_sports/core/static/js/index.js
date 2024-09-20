document.addEventListener('DOMContentLoaded', function () {
    const app = document.getElementById('app');

    function loadBracket(slug) {
        fetch(`/bracket/${slug}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro ao carregar conteúdo: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                console.log("Conteúdo carregado com sucesso");
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const content = doc.querySelector('.dynamic-content');
                if (content) {
                    console.log("Conteúdo dinâmico encontrado, atualizando DOM");
                    app.innerHTML = content.innerHTML;
                } else {
                    console.error("Conteúdo dinâmico não encontrado no HTML retornado.");
                    app.innerHTML = "<p>Conteúdo dinâmico não encontrado.</p>";
                }
            })
            .catch(error => {
                console.error("Erro ao carregar o conteúdo:", error);
                app.innerHTML = "<p>Erro ao carregar o conteúdo. Verifique o console para mais detalhes.</p>";
            });
    }

    console.log("JavaScript carregado com sucesso!");

    // Adicione um log para verificar se as modalidades estão sendo capturadas
    document.querySelectorAll('.dropdown-item').forEach(item => {
        console.log(`Modalidade encontrada: ${item.getAttribute('data-id')}`);
        item.addEventListener('click', function(event) {
            event.preventDefault();
            const modalidadeSlug = this.getAttribute('data-id');
            loadBracket(modalidadeSlug);
        });
    });
});
