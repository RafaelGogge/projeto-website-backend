from dataclasses import dataclass
from typing import List, Optional
import json

@dataclass
class Track:
    """
    Modelo para representar uma música
    """
    id: str
    name: str
    artist: str
    album: str
    duration_ms: int
    preview_url: Optional[str]
    spotify_url: str
    image_url: Optional[str] = None
    popularity: int = 0
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'artist': self.artist,
            'album': self.album,
            'duration_ms': self.duration_ms,
            'preview_url': self.preview_url,
            'spotify_url': self.spotify_url,
            'image_url': self.image_url,
            'popularity': self.popularity
        }
    
    @classmethod
    def from_spotify_data(cls, track_data):
        """Cria um objeto Track a partir dos dados da API do Spotify"""
        return cls(
            id=track_data['id'],
            name=track_data['name'],
            artist=', '.join([artist['name'] for artist in track_data['artists']]),
            album=track_data['album']['name'],
            duration_ms=track_data['duration_ms'],
            preview_url=track_data.get('preview_url'),
            spotify_url=track_data['external_urls']['spotify'],
            image_url=track_data['album']['images'][0]['url'] if track_data['album']['images'] else None,
            popularity=track_data.get('popularity', 0)
        )
    
    @classmethod
    def from_dict(cls, data):
        """Cria um objeto Track a partir de um dicionário"""
        return cls(**data)
    
    def get_duration_formatted(self):
        """Retorna a duração formatada em MM:SS"""
        total_seconds = self.duration_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    def __str__(self):
        return f"{self.name} - {self.artist} ({self.album})"

@dataclass
class Playlist:
    """
    Modelo para representar uma playlist
    """
    id: str
    name: str
    description: str
    tracks: List[Track]
    total_tracks: int
    public: bool = True
    owner: str = ""
    image_url: Optional[str] = None
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'tracks': [track.to_dict() for track in self.tracks],
            'total_tracks': self.total_tracks,
            'public': self.public,
            'owner': self.owner,
            'image_url': self.image_url
        }
    
    @classmethod
    def from_spotify_data(cls, playlist_data, tracks_data=None):
        """Cria um objeto Playlist a partir dos dados da API do Spotify"""
        tracks = []
        if tracks_data:
            for item in tracks_data['items']:
                if item['track'] and item['track']['id']:
                    tracks.append(Track.from_spotify_data(item['track']))
        
        return cls(
            id=playlist_data['id'],
            name=playlist_data['name'],
            description=playlist_data.get('description', ''),
            tracks=tracks,
            total_tracks=playlist_data['tracks']['total'],
            public=playlist_data.get('public', True),
            owner=playlist_data['owner']['display_name'] if playlist_data.get('owner') else '',
            image_url=playlist_data['images'][0]['url'] if playlist_data.get('images') else None
        )
    
    def add_track(self, track: Track):
        """Adiciona uma música à playlist"""
        if track.id not in [t.id for t in self.tracks]:
            self.tracks.append(track)
            self.total_tracks = len(self.tracks)
            return True
        return False
    
    def remove_track(self, track_id: str):
        """Remove uma música da playlist"""
        original_count = len(self.tracks)
        self.tracks = [track for track in self.tracks if track.id != track_id]
        self.total_tracks = len(self.tracks)
        return len(self.tracks) < original_count
    
    def get_total_duration(self):
        """Retorna a duração total da playlist em milissegundos"""
        return sum(track.duration_ms for track in self.tracks)
    
    def get_total_duration_formatted(self):
        """Retorna a duração total formatada"""
        total_ms = self.get_total_duration()
        total_seconds = total_ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}min"
        else:
            return f"{minutes}min"
    
    def __str__(self):
        return f"{self.name} ({self.total_tracks} músicas)"

@dataclass
class Artist:
    """
    Modelo para representar um artista
    """
    id: str
    name: str
    genres: List[str]
    popularity: int
    followers: int
    image_url: Optional[str] = None
    spotify_url: str = ""
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'genres': self.genres,
            'popularity': self.popularity,
            'followers': self.followers,
            'image_url': self.image_url,
            'spotify_url': self.spotify_url
        }
    
    @classmethod
    def from_spotify_data(cls, artist_data):
        """Cria um objeto Artist a partir dos dados da API do Spotify"""
        return cls(
            id=artist_data['id'],
            name=artist_data['name'],
            genres=artist_data.get('genres', []),
            popularity=artist_data.get('popularity', 0),
            followers=artist_data['followers']['total'] if artist_data.get('followers') else 0,
            image_url=artist_data['images'][0]['url'] if artist_data.get('images') else None,
            spotify_url=artist_data['external_urls']['spotify'] if artist_data.get('external_urls') else ''
        )
    
    def __str__(self):
        return f"{self.name} ({self.followers} seguidores)"