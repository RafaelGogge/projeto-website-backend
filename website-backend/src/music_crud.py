import json
import os
from typing import List, Optional
from .spotify_client import SpotifyClient
from .models import Track, Playlist, Artist

class MusicCRUD:
    """
    Classe principal para operações CRUD com músicas do Spotify
    
    Funcionalidades:
    - Buscar músicas, artistas e álbuns
    - Gerenciar favoritos locais
    - Criar e gerenciar playlists
    - Análise de dados musicais
    """
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.spotify_public = SpotifyClient(use_auth=False)
        self.spotify_auth = None  # Será inicializado quando necessário
        
        # Arquivos de dados locais
        self.favorites_file = os.path.join(data_dir, "favorites.json")
        self.playlists_file = os.path.join(data_dir, "my_playlists.json")
        self.history_file = os.path.join(data_dir, "search_history.json")
        
        # Criar diretório e arquivos se não existirem
        self._init_files()
    
    def _init_files(self):
        """Inicializa arquivos JSON se não existirem"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        if not os.path.exists(self.favorites_file):
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
        
        if not os.path.exists(self.playlists_file):
            with open(self.playlists_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
        
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _get_auth_client(self):
        """Obtém cliente autenticado (inicializa se necessário)"""
        if self.spotify_auth is None:
            self.spotify_auth = SpotifyClient(use_auth=True)
        return self.spotify_auth.get_spotify_instance()
    
    def _save_search_history(self, query: str, result_count: int):
        """Salva histórico de buscas"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            from datetime import datetime
            history.append({
                'query': query,
                'timestamp': datetime.now().isoformat(),
                'result_count': result_count
            })
            
            # Manter apenas os últimos 100 registros
            history = history[-100:]
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar histórico: {e}")
    
    # ==================== BUSCAR MÚSICAS ====================
    
    def search_tracks(self, query: str, limit: int = 20) -> List[Track]:
        """Busca músicas no Spotify"""
        try:
            sp = self.spotify_public.get_spotify_instance()
            results = sp.search(q=query, type='track', limit=limit)
            
            tracks = []
            for track in results['tracks']['items']:
                tracks.append(Track.from_spotify_data(track))
            
            # Salvar no histórico
            self._save_search_history(query, len(tracks))
            
            return tracks
        except Exception as e:
            print(f"Erro ao buscar tracks: {e}")
            return []
    
    def search_artists(self, query: str, limit: int = 10) -> List[Artist]:
        """Busca artistas no Spotify"""
        try:
            sp = self.spotify_public.get_spotify_instance()
            results = sp.search(q=query, type='artist', limit=limit)
            
            artists = []
            for artist in results['artists']['items']:
                artists.append(Artist.from_spotify_data(artist))
            
            return artists
        except Exception as e:
            print(f"Erro ao buscar artistas: {e}")
            return []
    
    def get_track_by_id(self, track_id: str) -> Optional[Track]:
        """Obtém uma música específica por ID"""
        try:
            sp = self.spotify_public.get_spotify_instance()
            track_data = sp.track(track_id)
            return Track.from_spotify_data(track_data)
        except Exception as e:
            print(f"Erro ao obter track: {e}")
            return None
    
    def get_artist_top_tracks(self, artist_id: str, country: str = 'BR') -> List[Track]:
        """Obtém as principais músicas de um artista"""
        try:
            sp = self.spotify_public.get_spotify_instance()
            results = sp.artist_top_tracks(artist_id, country=country)
            
            tracks = []
            for track in results['tracks']:
                tracks.append(Track.from_spotify_data(track))
            
            return tracks
        except Exception as e:
            print(f"Erro ao obter top tracks do artista: {e}")
            return []
    
    # ==================== FAVORITOS (LOCAL) ====================
    
    def add_to_favorites(self, track: Track) -> bool:
        """Adiciona música aos favoritos locais"""
        try:
            with open(self.favorites_file, 'r', encoding='utf-8') as f:
                favorites = json.load(f)
            
            # Verifica se já existe
            if any(fav['id'] == track.id for fav in favorites):
                print("Música já está nos favoritos!")
                return False
            
            favorites.append(track.to_dict())
            
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(favorites, f, ensure_ascii=False, indent=2)
            
            print(f"'{track.name}' adicionada aos favoritos!")
            return True
        except Exception as e:
            print(f"Erro ao adicionar aos favoritos: {e}")
            return False
    
    def get_favorites(self) -> List[Track]:
        """Obtém todas as músicas favoritas"""
        try:
            with open(self.favorites_file, 'r', encoding='utf-8') as f:
                favorites_data = json.load(f)
            
            favorites = []
            for track_data in favorites_data:
                track = Track.from_dict(track_data)
                favorites.append(track)
            
            return favorites
        except Exception as e:
            print(f"Erro ao obter favoritos: {e}")
            return []
    
    def remove_from_favorites(self, track_id: str) -> bool:
        """Remove música dos favoritos"""
        try:
            with open(self.favorites_file, 'r', encoding='utf-8') as f:
                favorites = json.load(f)
            
            original_count = len(favorites)
            favorites = [fav for fav in favorites if fav['id'] != track_id]
            
            if len(favorites) == original_count:
                print("Música não encontrada nos favoritos!")
                return False
            
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(favorites, f, ensure_ascii=False, indent=2)
            
            print("Música removida dos favoritos!")
            return True
        except Exception as e:
            print(f"Erro ao remover dos favoritos: {e}")
            return False
    
    def is_favorite(self, track_id: str) -> bool:
        """Verifica se uma música está nos favoritos"""
        favorites = self.get_favorites()
        return any(track.id == track_id for track in favorites)
    
    # ==================== PLAYLISTS (SPOTIFY) ====================
    
    def create_playlist(self, name: str, description: str = "", public: bool = False) -> Optional[str]:
        """Cria uma playlist no Spotify"""
        try:
            sp = self._get_auth_client()
            user_id = sp.current_user()['id']
            
            playlist = sp.user_playlist_create(
                user=user_id,
                name=name,
                public=public,
                description=description
            )
            
            print(f"Playlist '{name}' criada com sucesso!")
            return playlist['id']
        except Exception as e:
            print(f"Erro ao criar playlist: {e}")
            return None
    
    def get_my_playlists(self) -> List[dict]:
        """Obtém playlists do usuário"""
        try:
            sp = self._get_auth_client()
            playlists = sp.current_user_playlists(limit=50)
            
            my_playlists = []
            for playlist in playlists['items']:
                if playlist:  # Verificação adicional
                    my_playlists.append({
                        'id': playlist['id'],
                        'name': playlist['name'],
                        'description': playlist.get('description', ''),
                        'total_tracks': playlist['tracks']['total'],
                        'public': playlist.get('public', True),
                        'owner': playlist['owner']['display_name'],
                        'image_url': playlist['images'][0]['url'] if playlist.get('images') else None
                    })
            
            return my_playlists
        except Exception as e:
            print(f"Erro ao obter playlists: {e}")
            return []
    
    def add_track_to_playlist(self, playlist_id: str, track_id: str) -> bool:
        """Adiciona música a uma playlist"""
        try:
            sp = self._get_auth_client()
            sp.playlist_add_items(playlist_id, [track_id])
            print("Música adicionada à playlist!")
            return True
        except Exception as e:
            print(f"Erro ao adicionar à playlist: {e}")
            return False
    
    def remove_track_from_playlist(self, playlist_id: str, track_id: str) -> bool:
        """Remove música de uma playlist"""
        try:
            sp = self._get_auth_client()
            sp.playlist_remove_all_occurrences_of_items(playlist_id, [track_id])
            print("Música removida da playlist!")
            return True
        except Exception as e:
            print(f"Erro ao remover da playlist: {e}")
            return False
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Track]:
        """Obtém músicas de uma playlist"""
        try:
            sp = self.spotify_public.get_spotify_instance()
            results = sp.playlist_tracks(playlist_id)
            
            tracks = []
            for item in results['items']:
                if item['track'] and item['track']['id']:
                    tracks.append(Track.from_spotify_data(item['track']))
            
            return tracks
        except Exception as e:
            print(f"Erro ao obter tracks da playlist: {e}")
            return []
    
    # ==================== ANÁLISES E ESTATÍSTICAS ====================
    
    def get_favorites_stats(self) -> dict:
        """Obtém estatísticas dos favoritos"""
        favorites = self.get_favorites()
        
        if not favorites:
            return {"total": 0, "artists": [], "total_duration": "0min"}
        
        # Contagem por artista
        artists = {}
        total_duration = 0
        
        for track in favorites:
            artist = track.artist
            artists[artist] = artists.get(artist, 0) + 1
            total_duration += track.duration_ms
        
        # Artistas mais ouvidos
        top_artists = sorted(artists.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Duração formatada
        duration_minutes = total_duration // (1000 * 60)
        duration_hours = duration_minutes // 60
        duration_remaining_minutes = duration_minutes % 60
        
        if duration_hours > 0:
            duration_str = f"{duration_hours}h {duration_remaining_minutes}min"
        else:
            duration_str = f"{duration_minutes}min"
        
        return {
            "total": len(favorites),
            "top_artists": top_artists,
            "total_duration": duration_str,
            "avg_popularity": sum(t.popularity for t in favorites) / len(favorites) if favorites else 0
        }
    
    def get_search_history(self) -> List[dict]:
        """Obtém histórico de buscas"""
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    
    # ==================== UTILITÁRIOS ====================
    
    def test_connection(self) -> bool:
        """Testa conexão com Spotify"""
        try:
            success, message = self.spotify_public.test_connection()
            print(message)
            return success
        except Exception as e:
            print(f"Erro no teste de conexão: {e}")
            return False