import requests
import random

from torrent import Torrent

def n_random(n: int) -> str:
    return ''.join(str(random.randint(0, 9)) for _ in range(n))

class Tracker:
    def __init__(self, url: str, torrent: Torrent):
        self.url = url
        self.torrent = torrent
        self.peer_list = []
        
    def fetch_peers(self) -> None:
        params = {
            'info_hash': self.torrent.info_hash,
            'pee': f'-TB0001{n_random(13)}',
            'left': self.torrent.total_length
        }
        
        # resp = requests.get(self.url, params=params)

if __name__ == '__main__':
    torrent = Torrent('../files/count.torrent')
    tracker = Tracker(torrent=torrent)
    
    print(tracker.fetch_peers())