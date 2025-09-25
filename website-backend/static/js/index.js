// JS para tela inicial (index.html)
function favoritarMusica(trackId, trackName) {
    axios.post('/adicionar_favorito', new URLSearchParams({track_id: trackId}))
        .then(function(response) {
            Swal.fire({
                icon: 'success',
                title: 'Favorito adicionado!',
                html: `<strong>${trackName}</strong> foi adicionado aos favoritos.`,
                showConfirmButton: false,
                timer: 1800,
                background: '#fffbe6',
                color: '#222',
                customClass: {
                    popup: 'shadow-lg rounded',
                    title: 'fw-bold',
                }
            });
        })
        .catch(function(error) {
            Swal.fire({
                icon: 'error',
                title: 'Erro ao favoritar',
                text: 'Não foi possível adicionar aos favoritos.',
                showConfirmButton: true
            });
        });
}
