from operator import itemgetter, attrgetter

class Controller:
    def __init__(self, db):
        """Has a deck, a list of players and a view."""
        # models
        self.db = db

    def check_add_player(self, first_name, last_name, date, sex, ranking):
        name = self.db.exist_player(last_name)
        for i in range(0, len(name)):
            if name[i][0] == first_name and name[i][1] == last_name:
                return False
        self.db.insert_player(first_name, last_name, date, sex, ranking)
        return True

    def check_add_tour(self, tour_name, venue, date):
        name = self.db.exist_tour(tour_name)
        for i in range(0, len(name)):
            if name[i][0] == tour_name:
                return False
        self.db.insert_tour(tour_name, venue, date)
        return True

    def check_add_competitors(self, tour_id, player_list):
        competitors = self.db.exist_competition(tour_id)
        print("Competitors : XXXX: ", len(competitors))
        if len(competitors) != 0:
            return False
        else:
            for player_id in player_list:
                self.db.insert_competitor(tour_id, player_id)
            return True

    def display_player(self):
        return self.db.get_players()

    def display_ranked_player(self):
        return self.db.get_ranked_players()

    def update_match(self, match_id, result):
        return self.db.update_match(match_id, result)

    def display_one_player(self, player_id):
        player_table_size = self.db.get_table_size('player')
        if int(player_id) <= player_table_size:
            return (True, player_table_size,  self.db.get_player(player_id))
        else:
            return (False, player_table_size, None)

    def display_tour(self):
        tour_table_size = self.db.get_table_size('tournaments')
        if tour_table_size != 0:
            return (True, tour_table_size,  self.db.get_tour())
        else:
            return (False, 0, None)

    def display_matches(self, tour_id):
        matches = self.db.get_match(tour_id)
        if len(matches) == 0:
            return (False, None)
        else:
            return (True, matches)

    def display_unk_matches(self):
        matches = self.db.get_unk_match()
        if len(matches) == 0:
            return (False, None)
        else:
            return (True, matches)

    def display_round(self, tour_num, round_num):
        tour_table_size = self.db.get_table_size('tournaments')
        if tour_table_size != 0:
            return (True, tour_table_size,  self.db.get_rounds(tour_num, round_num))
        else:
            return (False, 0, None)

    def display_competitors(self, tour_id):
        competitors = self.db.get_competitors(tour_id)
        if len(competitors) == 0:
            return (False, [])
        else:
            return (True, competitors)

    def make_status(self, tour_id):
        matches = Controller.display_matches(self, tour_id)
        match = matches[1]
        score_dict = {}
        score1 = 0
        score2 = 0
        played = 0
        if matches[0] is True and len(match) != 0:
            for i in range(0, len(match)):
                round_num = match[i][0]
                player1 = ' '.join(match[i][2:4])
                player2 = ' '.join(match[i][4:6])
                player1_id = match[i][7]
                player2_id = match[i][8]
                player1_rk = match[i][9]
                player2_rk = match[i][10]
                if player1 not in score_dict:
                    score_dict[player1] = (0,0)
                if player2 not in score_dict:
                    score_dict[player2] = (0,0)
                if match[i][1] == 'tie':
                    score1 = 0.5
                    score2 = 0.5
                    played = match[i][0]
                elif match[i][1] == 'pl1':
                    score1 = 1
                    score2 = 0
                    played = match[i][0]
                elif match[i][1] == 'pl2':
                    score1 = 0
                    score2 = 1
                    played = match[i][0]
                elif match[i][1] == 'unk':
                    """Match not yet played.Score unchanged."""
                    score1 = 0
                    score2 = 0
                score1 += score_dict[player1][0]
                score2 += score_dict[player2][0]
                score_dict[player1] = (score1, played, round_num, player1, player1_id, player1_rk)
                score_dict[player2] = (score2, played, round_num, player2, player2_id, player2_rk)
                round_summary = list(score_dict.values())
                sorted_summary = sorted(round_summary, key=itemgetter(0,5,3))
            return (True,sorted_summary)
        else:
            return(False, [])

    def get_round(self,tour_id):
        round_status = Controller.make_status(self, tour_id)
        print(round_status)
        print(round_status[0])
        print(round_status[1])
        """Round_complete is True is the round is complete,  Competitor_added is True if there are competitors"""
        round = {'Round_number': 0, 'Round_complete': True, 'Competitor_added':False}
        print("Round status:000000")
        """No round added yet"""
        if round_status[0] is False:
            competitors = self.db.get_competitors(tour_id)
            print("Round status:1")
            if len(competitors) == 0:
                """No matches,Round complete,no competitors added"""
                print("Round status:2")
                round = {'Round_number': 0, 'Round_complete': False, 'Competitor_added':False}
            else:
                """No matches,Round complete,competitors added"""
                print("Round status:3")
                round = {'Round_number': 0, 'Round_complete': False, 'Competitor_added':True}
        elif round_status[0] is True:
            print("Round status:400000")
            for status in round_status[1]:
                if status[1] == status[2] and round['Round_complete'] is True:
                    print("Round status:4")
                    print("Round :", status[2], " is complete")
                    round = {'Round_number':status[2], 'Round_complete': True, 'Competitor_added':True}
                elif status[1] != status[2]:
                    print("Round status:5")
                    print("Player :", status[3], "does not have result for round: ", status[2])
                    round = {'Round_number':status[2], 'Round_complete': False, 'Competitor_added':True}
        return round


             


    def add_round(self, tour_id):
        round = Controller.get_round(self, tour_id)
        if round['Competitor_added'] is False:
            """No competitors added : return request to add competitors"""
            return round
        elif round['Round_number'] == 0:
            """First round : create matches, matching competitors using rank"""
            competitors = self.db.get_ranked_competitors(tour_id)
            for idx in range(0, int(len(competitors) / 2)):
                """Create matches Player (0,4), (1,5), (2,6), (3,7)"""
                self.db.insert_match('unk', 1, tour_id, competitors[idx][0],competitors[idx + 4][0])
            return round
        elif round['Round_number'] != 0 and round['Round_complete'] is True:
            round_status = Controller.make_status(self, tour_id)
            """Need all matches already played and round scores"""
            """round_status[1] contains ordered by score,ranking : score, played,
            round_num, player, player_id, player_rk for the 8 players"""
            return round
        elif round['Round_number'] != 0 and round['Round_complete'] is False:
            """Return request to complete to complete round"""
            return round



