document.addEventListener('DOMContentLoaded', function () {
    let recommendedFilms = [];
    let randomFilms = [];

    function fetchFilms() {
        fetch('/api/movies/')
            .then(response => response.json())
            .then(data => {
                recommendedFilms = data.recommended_filmes;
                randomFilms = data.random_filmes;

                displayFilms(recommendedFilms, '#recommended-movies .row');
                displayFilms(randomFilms, '#three-movies .list-group');
            })
            .catch(error => console.error('Error:', error));
    }

    function displayFilms(films, containerSelector) {
        const container = document.querySelector(containerSelector);
        container.innerHTML = '';

        films.forEach(filme => {
            const item = containerSelector === '#three-movies .list-group'
                ? document.createElement('li')
                : document.createElement('div');

            item.classList.add(containerSelector === '#three-movies .list-group' ? 'list-group-item' : 'col', 'mb-2');

            const card = document.createElement('div');
            card.classList.add(containerSelector === '#three-movies .list-group' ? 'other-card' : 'movie-card');
            card.innerHTML = `
                <img src="${filme.imagem_url}" class="card-image" alt="${filme.titulo}">
                <h6 class="${containerSelector === '#three-movies .list-group' ? 'other-title' : 'card-text'}">${filme.titulo}</h6>
            `;

            card.addEventListener('click', () => {
                window.location.href = `/movie/${filme.id}`;
            });

            item.appendChild(card);
            container.appendChild(item);
        });
    }

    function filterFilms() {
        const query = document.getElementById('search').value.toLowerCase();

        const filteredRecommended = recommendedFilms.filter(filme =>
            filme.titulo.toLowerCase().includes(query)
        );
        const filteredRandom = randomFilms.filter(filme =>
            filme.titulo.toLowerCase().includes(query)
        );

        displayFilms(filteredRecommended, '#recommended-movies .row');
        displayFilms(filteredRandom, '#three-movies .list-group');
    }

    document.getElementById('search').addEventListener('input', filterFilms);

    fetchFilms();
});
