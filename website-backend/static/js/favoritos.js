// JS para favoritos.html
function confirmRemove(trackId, trackName) {
    Swal.fire({
        title: 'Remover dos Favoritos',
        html: `Tem certeza que deseja remover <strong>${trackName}</strong> de seus favoritos?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sim, remover',
        cancelButtonText: 'Não',
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        focusCancel: true
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('removeForm' + trackId).submit();
        }
    });
}
