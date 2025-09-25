// JS para página de playlists
function confirmSpotifyRedirect(spotifyUrl, playlistName) {
    Swal.fire({
        title: 'Redirecionar para o Spotify?',
        html: `Você será direcionado para a playlist <strong>${playlistName}</strong> no Spotify.`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sim, abrir Spotify',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#1db954',
        cancelButtonColor: '#d33',
        focusCancel: true
    }).then((result) => {
        if (result.isConfirmed) {
            window.open(spotifyUrl, '_blank');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('criarPlaylistForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            try {
                const res = await axios.post('/criar_playlist', formData);
                if (res.data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Playlist criada!',
                        showConfirmButton: false,
                        timer: 1800
                    });
                    setTimeout(() => { window.location.reload(); }, 2000);
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Erro ao criar playlist',
                        text: res.data.message || 'Tente novamente.',
                    });
                }
            } catch (err) {
                Swal.fire({
                    icon: 'error',
                    title: 'Erro ao criar playlist',
                    text: err.response?.data?.message || 'Tente novamente.',
                });
            }
        });
    }
});
