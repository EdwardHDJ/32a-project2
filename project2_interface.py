import connectfour

def check_user_input(current_state:connectfour.GameState,user_input)->str:
    'check the user\'s input, if the input is uncorrect, ask user to type again'
    while True :
        try:
            if user_input.startswith('POP') and user_input[3]==' ' and type(eval(user_input[4:]))==int:
                check_user_move_validity(current_state,user_input)
                break
            if user_input.startswith('DROP') and user_input[4]==' ' and type(eval(user_input[5:]))==int:
                check_user_move_validity(current_state,user_input)
                break
            raise ValueError
        except:
            print('This move is not valid,please type again')
            user_input = get_user_input()
            continue
    return user_input

def check_user_move_validity(game_state:connectfour.GameState,user_input)->None:
    'check if the user\'s move is valid, if it is not, raise a error'
    current_state = game_state
    column = get_user_input_column(user_input)
    column -= 1
    if user_input.startswith('DROP'):
        try:
            current_state = connectfour.drop(current_state,column)
        except ValueError:
            print(f'column_number must be an int between 1 and {connectfour.columns(game_state)}')
            raise ValueError
        except connectfour.InvalidMoveError:
            print('This move is invalid, the column is full')
            raise connectfour.InvalidMoveError
    if user_input.startswith('POP'):
        try:
            current_state = connectfour.pop(game_state,column)
        except ValueError:
            print(f'column_number must be an int between 1 and {connectfour.columns(game_state)}')
            raise ValueError
        except connectfour.InvalidMoveError:
            print('This move is invalid, the discs at the bottom is not yours' )
            raise connectfour.InvalidMoveError

def check_winner(game_state:connectfour.GameState)->str:
    'check if there is a winner'
    if connectfour.winner(game_state)==0:
        return 'OKAY'
    if connectfour.winner(game_state)==1:
        return 'WINNER_RED'
    if connectfour.winner(game_state)==2:
        return 'WINNER_YELLOW'

def create_game()->connectfour.GameState:
    'ask the user to type the numbers of column and row, then create the board'
    columns = get_columns()
    rows = get_rows()
    game_state = connectfour.new_game(columns,rows)
    return game_state

def print_game(game_state:connectfour.GameState)->None:
    'print the current game board'
    num_col = connectfour.columns(game_state)
    for x in range(num_col) :
        if x<9:
            print(x+1,end= '  ')
        if x >=9:
            print(x+1,end= ' ')
    print()
    index = 0
    for y in range(connectfour.rows(game_state)):    
        for x in game_state.board:
            if x[index] == 0:
                print('.',end = '  ')
            if x[index] == 1:
                print('R',end = '  ')
            if x[index] == 2:
                print('Y',end = '  ')
        print()
        index+=1

def drop(game_state:connectfour.GameState,column:int)->connectfour.GameState:
    'drop a disc on the board'
    current_state = game_state
    try:
        current_state = connectfour.drop(current_state,column)
        print_game(current_state)
    except ValueError:
        print(f'column_number must be an int between 1 and {connectfour.columns(game_state)}')
        return None        
    except connectfour.InvalidMoveError:
        print('This move is invalid, the column is full')
        return None
    else:
        return current_state

def pop(game_state:connectfour.GameState,column:int)->connectfour.GameState:
    'pop a disc on the board'
    current_state = game_state
    try:
        current_state = connectfour.pop(game_state,column)
        print_game(current_state)
    except ValueError:
        print(f'column_number must be an int between 1 and {connectfour.columns(game_state)}')
    except connectfour.InvalidMoveError:
        print('This move is invalid, the discs at the bottom is not yours' )
    else:
        return current_state

def get_user_input()->str:
    'ask the user to type the correct input'
    s = input('please type POP or DROP with a space and a int like DROP 1\n' )
    return s

def do_action(current_state:connectfour.GameState,user_input:str)->connectfour.GameState:
    'do a action and return the new game board'
    if user_input.startswith('DROP'):
        current_state = connectfour.drop(current_state,int(user_input[5:])-1)
    if user_input.startswith('POP'):
        current_state = connectfour.pop(current_state,int(user_input[4:])-1)
    return current_state

def get_user_input_column(user_input)->int:
    'get the number of column from the user input'
    s = user_input
    if len(s)>4:
        if s.startswith('POP') and s[3]==' ' and type(eval(s[4:]))==int:
            return int(s[4:])
    if len(s)>5:
        if s.startswith('DROP') and s[4]==' ' and type(eval(s[5:]))==int:
            return int(s[5:])
    return None

def get_columns()->int:
    'ask user to type the number of column'
    while True:
        try:
            columns = int(input('Enter the number of columns\n'))
            if columns<connectfour.MIN_COLUMNS or columns > connectfour.MAX_COLUMNS:
                print(f'rows must be an int between {connectfour.MIN_COLUMNS} and {connectfour.MAX_COLUMNS}')
                continue
            return columns
        except:
            print('Invalid input,please type again')
            continue
def get_rows()->int:
    'ask the user to type the number of row'
    while True:
        try:
            rows = int(input('Enter the number of rows\n'))
            if rows<connectfour.MIN_ROWS or rows>connectfour.MAX_ROWS:
                print(f'rows must be an int between {connectfour.MIN_ROWS} and {connectfour.MAX_ROWS}')
                continue
            return rows
        except:
            print('Invalid input,please type again')
            continue

def print_turn(game_state):
    'show the user which player should move'
    if game_state.turn ==1:
        print('red turn')
    if game_state.turn ==2:
        print('yellow turn')
