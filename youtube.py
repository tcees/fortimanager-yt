from requests import Session
from math import ceil

class YouTube:
    """Simboliza uma instância da API do YouTube"""
    
    def __init__(self, api_key, verify=True):
        """Construtor

        Args:
            api_key(str): A APIkey da API do YouTube
            verify(bool): Verificar certificado SSL durante requisições
        """
        self.url = "https://www.googleapis.com/youtube/v3"
        self.chave = api_key
        self.sessao = Session()
        self.sessao.verify = verify

    def obterVideosPlaylist(self, playlist_id, quantidade=50):
        """Obtém os ids dos videos do YouTube por PlayList
        
        Args:
            playlist_id(str): O id da PlayList a se obter os videos
            quantidade(int): A quantidade de videos a ser obtida da
                playlist
        
        Returns:
            `list` de ids dos videos obtidos
        """
        
        parametros = {
            "key": self.chave,
            "playlistId": playlist_id,
            "part": "snippet",
            "order": "date",
            "maxResults": "50"
        }

        videos = list()

        while len(videos) < quantidade:
            json = self.sessao.get(
                    self.url+"/playlistItems", 
                    params=parametros).json()
            
            for video in json["items"]:
                videos.append(video["snippet"]["resourceId"]["videoId"])
            
            if not "nextPageToken" in json: 
                break
            
            else: 
                parametros["pageToken"] = json["nextPageToken"]

        if len(videos) < quantidade:
            return videos
        else:
            return videos[:quantidade]