import socket
from threading import Thread
from multiprocessing import Process
import select

players = {}


def is_data_exist(cs, t=10):
    assert type(cs) == socket.socket, 'wrong type.'
    ready = select.select([cs], [], [], t)
    return bool(ready[0])

def game(cs1, cs2):
    while is_data_exist(cs, 20):
        cs2.send(cs1.recv(1000))
    cs1.send('end game'.encode())
    cs2.send('end game'.encode())

    cs1.close()
    cs2.close()


def player(cs):
    data = cs.recv(100).decode('utf-8')
    if data == ',lp':
        # players list
        cs.send(','.join(players).encode())
        cs.close()
        return

    if data == ',wfp':
        # wait for players
        cs.send('send your name'.encode())
        player_name = cs.recv(1000).decode('utf-8')
        if ',' in player_name:
            cs.send('You shouldn\'t use , in your name.'.encode())
            cs.close()
            return
        else:
            players[player_name] = cs
            while True:
                if is_data_exist(cs, 10):
                    data = cs.recv(10000)
                    if not data:
                        players.pop(player_name)
                        break

                if len(players) > 1:
                    players2= players.copy()
                    players2.pop(player_name)
                    cs.send(','.join(players2).encode())

                # play and data is player name
                if data in players.keys():
                    Process(target=game, args=(cs, players[data])).start()
                    Process(target=game, args=(players[data], cs)).start()
                else:
                    cs.send('player name not exist.'.encode())
    


s = socket.socket()
s.bind(('localhost', 5614))
s.listen(2**10)

while True:
    cs, a = s.accept()
    print('connected')
    Thread(target=player, args=(cs,)).start()
