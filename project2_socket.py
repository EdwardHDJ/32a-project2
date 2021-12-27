import socket
from collections import namedtuple
import project2_interface
import connectfour

GameConnection=namedtuple('GameConnection',['socket','game_input','game_output'])

class ConnectionError(Exception):
    pass
class ProtocolError(Exception):
    pass

def connect(host:str,port:int)->GameConnection:
    'connect to the specific server, if connection fail raise ConnectionError'
    try:
        game_socket= socket.socket()
        game_socket.connect((host,port))
        input = game_socket.makefile('r')
        output = game_socket.makefile('w')
        return GameConnection(
                socket = game_socket,
                game_input =input,
                game_output = output)
    except:
        raise ConnectionError('The host or the port is not correct')

def send_user_move(current_state:connectfour.GameState,connection:GameConnection,user_input)->str:
    'send user\'s move to the server and check the server reply'
    _write_line(connection,user_input)
    winner =  project2_interface.check_winner(current_state)
##    print(_readline(connection))
    _expect_line(connection,winner)
    return winner
    
def _write_line(connection:GameConnection,line:int)->None:
    'send message to server'
##    print('write:'+line)
    connection.game_output.write(line+'\n\r')
    connection.game_output.flush()
	
def _readline(connection:GameConnection)->str:
    'read message from server'
    line = connection.game_input.readline()[0:-1]
##    print('print'+line)
    return line
    
def _expect_line(connection:GameConnection,expected:str)->None:
    'read message and check the message from the server'
    line = _readline(connection)
    if line != expected:
            raise ConnectionError

def close(connection: GameConnection) -> None:
        'Closes the connection to the Polling server'
        connection.game_input.close()
        connection.game_output.close()
        connection.socket.close()

def hello(connection:GameConnection,username:str)->None:
        'do the hello protocol part'
        _write_line(connection,'I32CFSP_HELLO '+username)
        _expect_line(connection,'WELCOME '+username)
        
def request_game(connection:GameConnection,current_state:connectfour.GameState)->None:
        'request game from the server'
        col = connectfour.columns(current_state)
        row = connectfour.rows(current_state)
        _write_line(connection,f'AI_GAME {col} {row}')
        _expect_line(connection,'READY')

def check_server_reply(connection:connectfour.GameState,current_state:connectfour.GameState):
    'check the server\'s reply, if server doesn\'t follow the protocol, raise ProtocolError'
    line = _readline(connection)
    print(f'Oppoent move: {line}')
    try:
        if line.startswith('POP') and line[3]==' ' and type(eval(line[4:]))==int:
                project2_interface.check_user_move_validity(current_state,line)
        if line.startswith('DROP') and line[4]==' ' and type(eval(line[5:]))==int:
                project2_interface.check_user_move_validity(current_state,line)
        return line
    except: 
        raise ProtocolError

def check_server_win(connection:connectfour.GameState,current_state:connectfour.GameState)->str:
    ' check the winner '
    winner = project2_interface.check_winner(current_state)
##    print('winner')
##    print(winner)
    if winner != 'OKAY':
        _expect_line(connection,winner)
    else:
        _expect_line(connection,'READY')
    return winner 
