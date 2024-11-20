document.addEventListener('DOMContentLoaded', function () {
    const heartButton = document.getElementById('heart-button');
    const filmeId = heartButton.getAttribute('data-filme-id');
    const isRelated = heartButton.getAttribute('data-is-related') === 'true';

    function updateButton(isRelated) {
        if (isRelated) {
            heartButton.classList.remove('btn-outline-danger');
            heartButton.classList.add('btn-danger');
            heartButton.textContent = 'Já assisti ❤️';
        } else {
            heartButton.classList.remove('btn-danger');
            heartButton.classList.add('btn-outline-danger');
            heartButton.textContent = 'Já assisti ❤️';
        }
    }

    updateButton(isRelated);

    heartButton.addEventListener('click', function () {
        fetch('/save-movie/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            },
            body: JSON.stringify({filme_id: filmeId})
        })
            .then(response => response.json())
            .then(data => {
                if (!data.error) {
                    window.location.reload();
                    updateButton(data.is_related);
                }
            })
            .catch(error => console.error('Error:', error));
    });
});
