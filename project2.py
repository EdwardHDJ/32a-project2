import connectfour
import project2_interface

def run():
    current_game_state = project2_interface.create_game()
    project2_interface.print_game(current_game_state)
    while True:
        project2_interface.print_turn(current_game_state)
        user_input = project2_interface.get_user_input()
        user_input = project2_interface.check_user_input(current_game_state,user_input)
        current_game_state = project2_interface.do_action(current_game_state,user_input)
        project2_interface.print_game(current_game_state)
        if connectfour.winner(current_game_state)!=0:
            break
    winner = project2_interface.check_winner(current_game_state)
    print(winner)

if __name__ == '__main__' :
    run()
