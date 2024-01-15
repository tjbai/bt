from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path
from hashlib import sha1

from bencode import decode_file, encode


class MissingMetadataError(Exception): pass

@dataclass
class File:
    length: int
    path: Optional[str] = None

class Torrent:
    announce: str
    piece_length: int
    pieces: List[str]
    name: str
    files: List[File]
    
    def __init__(self, path: Path) -> None:
        torrent = decode_file(path)
        
        try:
            self.announce = torrent['announce']
            
            info = torrent['info']
            self.piece_length = info['piece length']
            self.pieces = info['pieces']
            self.name = info['name']
            self.info_hash = sha1(encode(info).encode('utf-8')).digest()
            
            if 'files' in info.keys(): self.files = [File(d) for d in info['files']]
            else: self.files = [File(length=info['length'])]
                
            self.total_length = sum(f.length for f in self.files)
            
        except KeyError as e: 
            raise MissingMetadataError(e)
        
class Client:
    pass