import connectfour
import socket
import project2_socket
import project2_interface


def get_host()->str:
    ' ask the user to type the host'
    host = input('Enter the host address\n')
    return host

def get_port()->int:
    ' ask the user to type the port'
    port = int(input('Enter the port number\n'))
    return port

def get_username()->str:
    'ask the user to type the username, if the username is invalid ask them to type again'
    username = input('please enter your username(no whitespace included)')
    while True:
            if username.find(' ') == -1:
                    return username
            username = input('invalid username, username should not include spaces')

def check_winner(game_state:connectfour.GameState)->str:
    'check winner'
    if connectfour.winner(game_state)==0:
        return 'OKAY'
    if connectfour.winner(game_state)==1:
        return 'WINNER_RED'
    if connectfour.winner(game_state)==2:
        return 'WINNER_YELLOW'

def create_game()->connectfour.GameState:
    'same as in project2_interface'
    return project2_interface.create_game()

def print_turn(game_state:connectfour.GameState):
    'same as in project2_interface'
    return project2_interface.print_turn(game_state)

def print_game(game_state:connectfour.GameState)->None:
    'same as in project2_interface'
    project2_interface.print_game(game_state)

def get_user_input()->str:
    'same as in project2_interface'
    return project2_interface.get_user_input() 

def get_user_input_column(user_input)->int:
    'same as in project2_interface'
    return project2_interface.get_user_input_column(user_input)

def check_user_move_validity(game_state:connectfour.GameState,user_input):
    'same as in project2_interface'
    return project2_interface.check_user_move_validity(game_state,user_input)
    
def do_action(current_state:connectfour.GameState,user_input:str)->connectfour.GameState:
    'same as in project2_interface'
    return project2_interface.do_action(current_state,user_input)
   
def check_user_input(current_state:connectfour.GameState,user_input)->str:
    'same as in project2_interface'
    return project2_interface.check_user_input(current_state,user_input)

def game_over(connection:project2_socket.GameConnection)->None:
    ' close the connection'
    project2_socket.close(connection)
    
def run()->None:    
##    host = 'circinus-32.ics.uci.edu'
##    port = 4444
    connection = None
    try:
        host = get_host()
        try:
            port = get_port()
        except:
            raise ValueError('port has to be a number')
        connection = project2_socket.connect(host,port)
        username = get_username()     
        project2_socket.hello(connection,username)
        current_state = create_game()
        project2_socket.request_game(connection,current_state)
        print_game(current_state)
        while True: 
            if connectfour.winner(current_state)!=0:
                break
            if current_state.turn == 1:
                user_input = get_user_input()
                user_input = check_user_input(current_state,user_input)
                current_state = do_action(current_state,user_input)
                print_game(current_state)
                project2_socket.send_user_move(current_state,connection,user_input)
                winner = check_winner(current_state)
                
            elif current_state.turn == 2:
                line = project2_socket.check_server_reply(connection,current_state)
                current_state = do_action(current_state,line)
                print_game(current_state)
                winner = project2_socket.check_server_win(connection,current_state)

        print(winner)
        game_over(connection)
    except project2_socket.ProtocolError:
        print('The protocol is wrong, end connection')
        project2_socket.close(connection)
    except project2_socket.ConnectionError:
        print('The server is not responding')
    except:
        if connection != None:
            project2_socket.close(connection)
    finally:
        if connection != None:  
            project2_socket.close(connection) 
if __name__ =='__main__':
    run()
          
