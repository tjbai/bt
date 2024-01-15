from typing import Tuple, Union
from pathlib import Path


class DecodeError(Exception): pass

type Encoded = Union[dict, list, str, int]

def decode(s: str, offset: int) -> Tuple[Encoded, int]:
    if offset >= len(s):
        raise DecodeError
    
    match s[0]:
        case 'd': return decode_dict(s, offset)
        case 'l': return decode_list(s, offset)
        case 'i': return decode_int(s, offset)
        case _: return decode_str(s, offset)

def decode_file(p: Path) -> Encoded:
    with open(p, 'r') as f:
        res, _ = decode(f.read(), 0)
        return res
    
def decode_int(s: str, offset: int) -> Tuple[int, int]:
    if (e := s.find('e', offset)) == -1:
        raise DecodeError('could not match int')

    return int(s[offset+1:e]), e+1

def decode_str(s: str, offset: int) -> Tuple[str, int]:
    if (delim := s.find(':', offset)) == -1:
        raise DecodeError('could not delim string')
    
    len = int(s[offset:delim])
    return s[delim+1:delim+len+1], delim+len+1

def decode_list(s: str, offset: int) -> Tuple[list, int]:
    offset += 1
    res = []
    
    while offset < len(s) and s[offset] != 'e':
        obj, offset = decode(s, offset)
        res.append(obj)
    
    return res, offset+1

def decode_dict(s: str, offset: int) -> Tuple[dict, int]:
    offset += 1
    res = {}
    
    while offset < len(s) and s[offset] != 'e':
        key, offset = decode_str(s, offset)
        value, offset = decode(s, offset)
        res[key] = value

    return res, offset+1

def encode(e: Encoded) -> str:
    match = {
        dict: encode_dict,
        list: encode_list,
        str: encode_str,
        int: encode_int
    }
    
    return match[type(e)](e)
        
def encode_dict(d: dict) -> str:
    return f'd{''.join(encode_str(k) + encode(v) for k, v in d.items())}e'
        
def encode_list(l: list) -> str:
    return f'l{''.join(encode(i) for i in l)}e'
        
def encode_str(s: str) -> str:
    return f'{len(s)}:{s}'
        
def encode_int(i: int) -> str:
    return f'i{i}e'