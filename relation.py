import socket
import time
import select

def is_data_exist(cs, t=10):
    ready = select.select([cs], [], [], t)
    return bool(ready[0])
        

class Relation:
    def __init__(self, player) -> None:
        self.player = player
        self.cs = socket.socket()
        self.is_connected = False

    def connect(self):
        try:
            self.cs.connect(('localhost', 5614)) 
            self.is_connected = True
            return 1
        except:
            return 0

    def check_for_play(self):
        self.cs.send(self.player.encode())
        if is_data_exist(self.cs):
            data = self.recv(10).decode('utf-8')
        else:
            # server don't send response.
            return 2
        return int(data)

    def send_pos(self, pos):
        self.cs.send(f'{pos[0]},{pos[1]}'.encode())

    def get_pos(self):
        if is_data_exist(self.cs, 20):
            pos = self.cs.recv(1000)
            pos = pos.decode('utf-8')
            pos = pos.split(',')
            return pos
        else:
            # server don't send response.
            return None

    def wait_for_play(self, player_name):
        self.cs.send(',wfp'.encode())
        print(self.cs.recv(1000).decode('utf-8'))
        self.cs.send(player_name.encode())
        player_names = self.cs.recv(100000).decode('utf-8').split(',')
        return player_names
