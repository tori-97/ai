
import struct
import json

class WebSocketFrame():
    def __init__(self, data) -> None:
        if isinstance(data, dict):
            self._data = json.dumps(data)
        else:
            self._data = data


    def encode(self):
        msg_bytes = self._data

        if isinstance(msg_bytes, str):
            msg_bytes = msg_bytes.encode()

        token = b"\x81"
        length = len(msg_bytes)
        
        if length < 126:
            token += struct.pack("B", length)
        elif length <= 0xFFFF:
            token += struct.pack("!BH", 126, length)
        else:
            token += struct.pack("!BQ", 127, length)
        
        msg = token + msg_bytes

        return msg
    
    def decode(self, as_json: bool = True):
        if len(self._data) == 0:
            return "client-is-closed"

        payload_len = self._data[1] & 127

        if payload_len == 126:
            extend_payload_len = self._data[2:4]
            mask = self._data[4:8]
            decoded = self._data[8:]
        
        elif payload_len == 127:
            extend_payload_len = self._data[2:10]
            mask = self._data[10:14]
            decoded = self._data[14:]
        
        else:
            extend_payload_len = None
            mask = self._data[2:6]
            decoded = self._data[6:]
        
        bytes_list = bytearray()

        for i in range(len(decoded)):
            chunk = decoded[i] ^ mask[i % 4]
            bytes_list.append(chunk)

        message = None

        if bytes_list != b'\x03\xe9':
            message = str(bytes_list, encoding='utf-8')
        
        if as_json:
            try:
                message = json.loads(message)
            except json.decoder.JSONDecodeError:
                pass
            except TypeError:
                pass
        
        return message

    def __str__(self) -> str:
        return f"{self.decode()}"
    
    def __len__(self):
        return len(self._data)

    def is_none(self):
        if self.decode() is None:
            return True
        return False

    def __eq__(self, item):
        if item == self.decode():
            return True
        return False