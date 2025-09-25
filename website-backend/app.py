from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.music_crud import MusicCRUD
from src.models import Track

app = Flask(__name__)
crud = MusicCRUD()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q', '').strip()
    modo = request.args.get('modo', 'musica')
    artist_name = None
    artist_tracks = []
    similar_tracks = []
    if not query:
        return render_template('index.html', query=query, modo=modo)

    if modo == 'artista':
        artists = crud.search_artists(query, limit=3)
        main_artist = None
        main_artist_tracks = []
        other_tracks = []
        if artists:
            # Considera o primeiro artista retornado como principal
            main_artist = artists[0]
            all_artist_tracks = crud.get_artist_top_tracks(main_artist.id)
            main_artist_tracks = [t for t in all_artist_tracks if t.artist.lower() == main_artist.name.lower()]
        # Buscar todas as músicas relacionadas ao termo
        all_tracks = crud.search_tracks(query)
        # Recomendações: músicas que não são do artista principal
        other_tracks = [t for t in all_tracks if not main_artist or t.artist.lower() != main_artist.name.lower()]
        return render_template('index.html', query=query, modo=modo, main_artist=main_artist, main_artist_tracks=main_artist_tracks, other_tracks=other_tracks)
    else:  # modo == 'musica'
        tracks = crud.search_tracks(query)
        return render_template('index.html', query=query, modo=modo, other_tracks=tracks)

@app.route('/favoritos')
def favoritos():
    favs = crud.get_favorites()
    return render_template('favoritos.html', favorites=favs)

@app.route('/adicionar_favorito', methods=['POST'])
def adicionar_favorito():
    track_id = request.form.get('track_id')
    track = crud.get_track_by_id(track_id)
    if track:
        crud.add_to_favorites(track)
    return redirect(url_for('favoritos'))

@app.route('/remover_favorito', methods=['POST'])
def remover_favorito():
    track_id = request.form.get('track_id')
    crud.remove_from_favorites(track_id)
    return redirect(url_for('favoritos'))

@app.route('/playlists')
def playlists():
    playlists = crud.get_my_playlists()
    return render_template('playlists.html', playlists=playlists)


from flask import jsonify

@app.route('/criar_playlist', methods=['POST'])
def criar_playlist():
    name = request.form.get('name')
    description = request.form.get('description', '')
    public = request.form.get('public') == 'on'
    playlist_id = crud.create_playlist(name, description, public)
    if playlist_id:
        return jsonify(success=True)
    else:
        return jsonify(success=False, message='Erro ao criar playlist'), 400

if __name__ == '__main__':
    app.run(debug=True)