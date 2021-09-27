"""This class consists of the the Menu handling"""
import re
from datetime import datetime
import sys

# appending a path
sys.path.append('.')


class Menu():
    MAIN_MENU = ["Add player",
                 "Add tournament",
                 "Add competitors",
                 "Add result",
                 "Display tournament",
                 "Display Round",
                 "Display Players",
                 "Display matches",
                 "Display scores",
                 "Quit"]

    PLAYER_MENU = ["First name",
                   "Last name",
                   "Birth date",
                   "Sex",
                   "Ranking"]

    def __init__(self, cont):
        """ """
        self.cont = cont
        self.execute_menu()

    def get_number(self, prompt):
        """Requests a number and repeats until a valid input"""
        while True:
            try:
                value = int(input(prompt))
                break
            except:
                pass
        return value

    def validate_name(name):
        result = re.match('^[a-zA-Z]+[a-zA-Z -\']*[A-Za-z]+$', name)
        if result:
            return True
        else:
            return False

    def validate_date(date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_sex(sex):
        if sex.upper() == 'M' or sex.upper() == 'F':
            return True
        else:
            return False

    def validate_ranking(ranking):
        if ranking.isdigit():
            if int(ranking) >= 1000 and int(ranking) <= 3000:
                return True
            else:
                return False
        else:
            return False

    def add_player(self):
        first_name = input("Enter player first name:")
        while not Menu.validate_name(first_name) and first_name != 'q':
            print("First name should be an alphabetic string")
            first_name = input("Enter player first name:")
        if first_name.lower() == 'q':
            return

        last_name = input("Enter player last name:")
        while not Menu.validate_name(last_name) and last_name != 'q':
            print("Last name should be an alphabetic string")
            last_name = input("Enter player last name:")
        if last_name.lower() == 'q':
            return

        birth_date = input("Enter player birth date yyyy-mm-dd:")
        while (not Menu.validate_date(birth_date) and birth_date != 'q'):
            print("Birth date should be yyyy-mm-dd")
            birth_date = input("Enter player birth_date:")
        if birth_date.lower() == 'q':
            return

        sex = input("Enter player gender (M or F):")
        while (not Menu.validate_sex(sex) and sex != 'q'):
            print("Gender should be M or F")
            sex = input("Enter player gender (M or F):")
        if sex.lower() == 'q':
            return

        ranking = input("Enter ranking (nnnn):")
        while (not Menu.validate_ranking(ranking) and ranking != 'q'):
            print("Ranking should be 1000 <= ranking <= 3000")
            ranking = input("Enter ranking (nnnn):")
        if ranking.lower() == 'q':
            return
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        if self.cont.check_add_player(first_name, last_name, birth_date, sex, ranking) is True:
            print("\n")
            print("Adding new player: ", first_name, last_name, birth_date, sex, ranking)
            print("\n")
        else:
            print("\n")
            print("Cannot add existing player: ", first_name, last_name)
            print("\n")

    def add_tournament(self):
        name = input("Enter tournament name:")
        while not len(name) != 0 and name.lower() != 'q':
            name = input("Enter tournament name:")
        if name.lower() == 'q':
            return
        venue = input("Enter tournament venue:")
        while not len(venue) != 0 and venue.lower() != 'q':
            venue = input("Enter tournament venue:")
        if venue.lower() == 'q':
            return
        date = input("Enter tournament date:")
        while (not Menu.validate_date(date) and date.lower() != 'q'):
            date = input("Enter tournament date:")
        if date.lower() == 'q':
            return
        date = datetime.strptime(date, '%Y-%m-%d').date()
        if self.cont.check_add_tour(name, venue, date) is True:
            print("\n")
            print("Adding new tournament: ", name, venue, date)
            print("\n")
        else:
            print("\n")
            print("Cannot add existing tournament: ", name)
            print("\n")

    def add_competitors(self):
        print("Add_competitors called\n")
        result = self.cont.display_tour()
        number_of_tour = result[1]
        prompt = "Enter tournament id (<= " + str(number_of_tour) + ") :"
        tour_num = input(prompt)
        while not (tour_num.lower() == 'q' or re.match('^[0-9]+$', tour_num)):
            tour_num = input(prompt)
        if tour_num.lower() == 'q':
            return
        """Verif if already existing : To be done"""
        total_player = len(self.cont.display_player())
        prompt = "Enter 8 player id (1 <= id <= " + str(total_player) + ") separated by spaces or q:"
        competitors = input(prompt).split(' ')
        if competitors[0] == 'q':
            return
        done = False
        while not done:
            player_list = []
            if competitors[0] == 'q':
                return
            number_of_competitors = len(competitors)
            if number_of_competitors != 8:
                print("Please enter 8 competitors")
                competitors = input(prompt).split(' ')
                done = False
            else:
                for comp in competitors:
                    if not re.match('^[0-9]+$', comp):
                        """Check if a number"""
                        print("Player_id: ", comp, " is not a valid id.")
                        competitors = input(prompt).split(' ')
                        done = False
                        break
                    elif int(comp) < 1 or int(comp) > total_player:
                        """Check if player id exists"""
                        print("Player id", comp, " does not exist")
                        competitors = input(prompt).split(' ')
                        done = False
                        break
                    elif int(comp) in player_list:
                        """Check for duplicate"""
                        print("Player id", comp, " Player already enrolled")
                        competitors = input(prompt).split(' ')
                        done = False
                        break
                    else:
                        player_list.append(int(comp))
                        done = True
        if self.cont.check_add_competitors(tour_num, player_list) is True:
            print("\n")
            print("Adding competitors for tournament: ", tour_num)
            print("\n")
        else:
            print("\n")
            print("Competitors already enrolled for tournament: ", tour_num)
            print("\n")

    def add_result():
        print("Add_result called\n")

    def display_players(self):
        name = input("Enter a(ll) / r(ranked) / player ID :")
        while not (re.match('^[arq]$', name.lower()) or re.match('^[0-9]+$', name)):
            name = input("Enter a(ll) / r(ranked) / player ID :")
        if name.lower() == 'a':
            player_list = self.cont.display_player()
            print("\n")
            print(25 * '-')
            print('{0:<5s}{1:<20s}'.format('Pid', 'Player'))
            print(25 * '-')
            for last_first in player_list:
                print('{0:<5d}{1:<20s}'.format(last_first[0], ' '.join(last_first[1:3])))
            print(25 * '-', '\n')
        elif name.lower() == 'r':
            player_list = self.cont.display_ranked_player()
            print("\n")
            print(40 * '-')
            print('{0:<5s}{1:<20s}{2:<4s}'.format('Pid', 'Player', 'Ranking'))
            print(40 * '-')
            for last_first_rank in (player_list):
                print('{0:<5d}{1:<20s}{2:<4d}'.format(last_first_rank[0],
                      ' '.join(last_first_rank[1:3]), last_first_rank[3]))
            print(40 * '-', '\n')
        elif re.match('^[0-9]+$', name):
            result = self.cont.display_one_player(name)
            if result[0] is True:
                print("\n")
                print(80 * '-')
                print('{0:<5s}{1:<20s}{2:<20s}{3:<20s}{4:<5s}{5:20s}'
                      .format('Pid', 'first_name', 'last_name', 'birth_date', 'sex',  'Ranking'))
                print(80 * '-')
                print('{0:<5d}{1:<20s}{2:<20s}{3:<20s}{4:<5s}{5:4d}'
                      .format(result[2][0], result[2][1], result[2][2], result[2][3], result[2][4], result[2][5]))
                print(80 * '-')
                print("\n")
            else:
                print("\n")
                print("Player id should be <=  ", result[1], "\n")
                return

    def display_tournament(self):
        result = self.cont.display_tour()
        if result[0] is True:
            print("\n")
            print(80 * '-')
            print('{0:<5s}{1:<20s}{2:<20s}{3:<20s}'
                  .format('Tid', 'Name', 'Venue', 'date'))
            print(80 * '-')
            for i in range(0, result[1]):
                print('{0:<5d}{1:<20s}{2:<20s}{3:<20s}'
                      .format(result[2][i][0], result[2][i][1], result[2][i][2], result[2][i][3]))
            print(80 * '-')
            print("\n")
        else:
            print("\n")
            print("No recorded tournament")
            print("\n")
            return

    def display_matches(self):
        print("Display_matches called\n")
        # Use the display_tour function to return the number of tour
        result = self.cont.display_tour()
        number_of_tour = result[1]
        prompt = "Enter tournament id (<= " + str(number_of_tour) + ") :"
        tour_id = input(prompt)
        while not (tour_id.lower() == 'q' or re.match('^[0-9]+$', tour_id)):
            tour_id = input(prompt)
        if tour_id.lower() == 'q':
            return
        matches = self.cont.display_matches(tour_id)
        match = matches[1]
        if matches[0] is True and len(match) != 0:
            print(70 * '-')
            print('{0:<20s}{1:<7s}{2:<10s}{3:<20s}{4:<20s}'.
                  format('Tour', 'Round', 'Result', 'Player1', 'Player2'))
            print(70 * '-')
            for i in range(0, len(match)):
                print('{0:20s}{1:<7d}{2:<10s}{3:<20s}{4:<20s}'.
                      format(match[i][6], match[i][0], match[i][1], ' '.join(match[i][2:4]), ' '.join(match[i][4:6])))
            print("\n")
        else:
            print("\n")
            print("No recorded matches for tour:", tour_id, "\n")

    def display_scores(self):
        print("Display_scores called\n")
        """ Use the display_tour function to return the number of tour"""
        result = self.cont.display_tour()
        number_of_tour = result[1]
        prompt = "Enter tournament id (<= " + str(number_of_tour) + ") :"
        tour_id = input(prompt)
        while not (tour_id.lower() == 'q' or re.match('^[0-9]+$', tour_id)):
            tour_id = input(prompt)
        if tour_id.lower() == 'q':
            return
        matches = self.cont.display_matches(tour_id)
        match = matches[1]
        score_dict = {}
        score1 = 0
        score2 = 0
        if matches[0] is True and len(match) != 0:
            for i in range(0, len(match)):
                player1 = ' '.join(match[i][2:4])
                player2 = ' '.join(match[i][4:6])
                if player1 not in score_dict:
                    score_dict[player1] = 0
                if player2 not in score_dict:
                    score_dict[player2] = 0
                if match[i][1] == 'tie':
                    score1 = 0.5
                    score2 = 0.5
                elif match[i][1] == 'pl1':
                    score1 = 1
                    score2 = 0
                elif match[i][1] == 'pl2':
                    score1 = 0
                    score2 = 1
                score_dict[player1] += score1
                score_dict[player2] += score2
            print(70 * '-')
            print('{0:<5s}{1:<20s}{2:<5s}'.format('Tour', 'Player', 'Score'))
            for key in score_dict.keys():
                print('{0:<5s}{1:<20s}{2:<.1f}'.format(tour_id, key, score_dict[key]))
            print(70 * '-')
        else:
            print("\n")
            print("No recorded matches for tour:", tour_id, "\n")

    def display_round(self):
        print("Display_round called\n")
        result = self.cont.display_tour()
        number_of_tour = result[1]
        prompt = "Enter tournament id (<= " + str(number_of_tour) + ") :"
        tour_num = input(prompt)
        while not (tour_num.lower() == 'q' or re.match('^[0-9]+$', tour_num)):
            tour_num = input(prompt)
        if tour_num.lower() == 'q':
            return
        round_num = input("Enter round number :")
        while not (round_num.lower() == 'q' or re.match('^[0-9]+$', round_num)):
            round_num = input("Enter round number :")
        if round_num.lower() == 'q':
            return
        rounds = self.cont.display_round(tour_num, round_num)
        round = rounds[2]
        if rounds[0] is True and len(round) != 0:
            print(70 * '-')
            print('{0:<7s}{1:<7s}{2:<10s}{3:<20s}{4:<20s}'.
                  format('Tour', 'Round', 'Result', 'Player1', 'Player2'))
            print(70 * '-')
            for i in range(0, len(round)):
                print('{0:7s}{1:<7s}{2:<10s}{3:<20s}{4:<20s}'.
                      format(tour_num, round_num, round[i][0], ' '.join(round[i][1:3]), ' '.join(round[i][3:5])))
            print("\n")
        else:
            print("\n")
            print("No recorded round for tour:", tour_num, " round: ", round_num, "\n")

    def quit(self):
        print("quit called\n")

    MENU_DICT = {1: add_player,
                 2: add_tournament,
                 3: add_competitors,
                 4: add_result,
                 5: display_tournament,
                 6: display_round,
                 7: display_players,
                 8: display_matches,
                 9: quit}

    def display_menu(self, choices):
        """display menu choices"""
        for entry in choices:
            print("{:d} {:s}".format(choices.index(entry) + 1, entry))

        selection = 0
        while selection not in range(1, len(choices) + 1):
            selection = self.get_number("Select a menu item:")

        return selection

    def execute_menu(self):
        """execute the requested menu item"""
        # Executes the request action
        selection = 0
        while selection != 10:
            selection = self.display_menu(self.MAIN_MENU)
            """#self.MENU_DICT.get(selection, None)()"""
            if selection == 1:
                self.add_player()
            elif selection == 2:
                self.add_tournament()
            elif selection == 3:
                self.add_competitors()
            elif selection == 4:
                self.add_result()
            elif selection == 5:
                self.display_tournament()
            elif selection == 6:
                self.display_round()
            elif selection == 7:
                self.display_players()
            elif selection == 8:
                self.display_matches()
            elif selection == 9:
                self.display_scores()
            elif selection == '10':
                self.quit()
