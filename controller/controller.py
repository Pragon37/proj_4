"""The controller consists mostly of functions that are used to interface between model and view.
   It sanitizes user inputs that come from the views/menu and processes requests whenever these
   are for adding or changing data in the sqlite3 repository"""
from operator import itemgetter


class Controller:
    def __init__(self, db):
        """Has a deck, a list of players and a view."""
        # models
        self.db = db

    def check_add_player(self, first_name, last_name, date, sex, ranking):
        """Check that no existing player (same last_name, first_name) is already recorded"""
        name = self.db.exist_player(last_name)
        for i in range(0, len(name)):
            if name[i][0] == first_name and name[i][1] == last_name:
                return False
        self.db.insert_player(first_name, last_name, date, sex, ranking)
        return True

    def check_add_tour(self, tour_name, venue, date):
        """Check that no existing tour (same name) is already recorded"""
        name = self.db.exist_tour(tour_name)
        for i in range(0, len(name)):
            if name[i][0] == tour_name:
                return False
        self.db.insert_tour(tour_name, venue, date)
        return True

    def check_add_competitors(self, tour_id, player_list):
        """Check if there competitors for tour = tour_id"""
        competitors = self.db.exist_competition(tour_id)
        # print("Competitors : XXXX: ", len(competitors))
        if len(competitors) != 0:
            return False
        else:
            for player_id in player_list:
                self.db.insert_competitor(tour_id, player_id)
            return True

    def display_player(self):
        """Provide all players for display"""
        return self.db.get_players()

    def display_ranked_player(self):
        """Provide all ranked players for display"""
        return self.db.get_ranked_players()

    def update_match(self, match_id, result):
        """To update a match result"""
        return self.db.update_match(match_id, result)

    def update_player(self, player_id, ranking):
        """To update a player ranking"""
        return self.db.update_player(player_id, ranking)

    def display_one_player(self, player_id):
        """Provide a player data for display"""
        player_table_size = self.db.get_table_size('player')
        if int(player_id) <= player_table_size:
            return (True, player_table_size,  self.db.get_player(player_id))
        else:
            return (False, player_table_size, None)

    def display_tour(self):
        """Provide tour data for display"""
        tour_table_size = self.db.get_table_size('tournaments')
        if tour_table_size != 0:
            return (True, tour_table_size,  self.db.get_tour())
        else:
            return (False, 0, None)

    def display_matches(self, tour_id):
        """Provide matches data of tour = tour_id for display"""
        matches = self.db.get_match(tour_id)
        if len(matches) == 0:
            return (False, None)
        else:
            return (True, matches)

    def display_unk_matches(self):
        """Provide matches data when match result is not yet known"""
        matches = self.db.get_unk_match()
        if len(matches) == 0:
            return (False, None)
        else:
            return (True, matches)

    def display_round(self, tour_num, round_num):
        """"Provide results and players of tour/round"""
        tour_table_size = self.db.get_table_size('tournaments')
        if tour_table_size != 0:
            return (True, tour_table_size,  self.db.get_rounds(tour_num, round_num))
        else:
            return (False, 0, None)

    def display_competitors(self, tour_id):
        """Provide data for competitors of tour = tour_id"""
        competitors = self.db.get_competitors(tour_id)
        if len(competitors) == 0:
            return (False, [])
        else:
            return (True, competitors)

    def make_status(self, tour_id):
        """For tour = tour_id it provides the (cumulated) score for each competitor and the number of matches played"""
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
                    score_dict[player1] = (0, 0)
                if player2 not in score_dict:
                    score_dict[player2] = (0, 0)
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
                    played = match[i][0] - 1
                score1 += score_dict[player1][0]
                score2 += score_dict[player2][0]
                score_dict[player1] = (score1, played, round_num, player1, player1_id, player1_rk)
                # print(score_dict[player1])
                score_dict[player2] = (score2, played, round_num, player2, player2_id, player2_rk)
                # print(score_dict[player2])
                round_summary = list(score_dict.values())
                sorted_summary = sorted(round_summary, key=itemgetter(0, 5, 3), reverse=True)
            return (True, sorted_summary)
        else:
            return(False, [])

    def get_round(self, tour_id):
        """For tour = tour_id it reports the round_number, if competirors have been added, if the round is complete,
        or to be completed (not all match results known), """
        round_status = Controller.make_status(self, tour_id)
        # print(round_status)
        # print(round_status[0])
        # print(round_status[1])
        """Round_complete is True if the round is complete,  Competitor_added is True if there are competitors"""
        round = {'Round_number': 0, 'Round_complete': True, 'Competitor_added': False}
        # print("Round status:000000")
        """No round added yet"""
        if round_status[0] is False:
            competitors = self.db.get_competitors(tour_id)
            # print("Round status:1")
            if len(competitors) == 0:
                """No matches,Round complete,no competitors added"""
                # print("Round status:2")
                round = {'Round_number': 0, 'Round_complete': False, 'Competitor_added': False}
            else:
                """No matches,Round complete,competitors added"""
                # print("Round status:3")
                round = {'Round_number': 0, 'Round_complete': False, 'Competitor_added': True}
        elif round_status[0] is True:
            # print("Round status:400000")
            for status in round_status[1]:
                if status[1] == status[2] and round['Round_complete'] is True:
                    # print("Round status:4")
                    # print("Round :", status[2], " is complete")
                    round = {'Round_number': status[2], 'Round_complete': True, 'Competitor_added': True}
                elif status[1] != status[2]:
                    # print("Round status:5")
                    # print("Player :", status[3], "does not have result for round: ", status[2])
                    round = {'Round_number': status[2], 'Round_complete': False, 'Competitor_added': True}
        return round

    def add_round(self, tour_id):
        """Add new round to an existing tour. Matches are added with results unknown. the players pair are defined
        using the swiss appairment method. Ranking for first tour and then scores."""
        round = Controller.get_round(self, tour_id)
        list_of_match_played = []
        list_player_score_rank = []
        list_new_matches = []
        if round['Competitor_added'] is False:
            """No competitors added : return request to add competitors"""
            return round
        elif round['Round_number'] == 0:
            """First round : create matches, matching competitors using rank"""
            competitors = self.db.get_ranked_competitors(tour_id)
            for idx in range(0, int(len(competitors) / 2)):
                """Create matches Player (0,4), (1,5), (2,6), (3,7)"""
                self.db.insert_match('unk', 1, tour_id, competitors[idx][0], competitors[idx + 4][0])
            return round
        elif round['Round_number'] != 0 and round['Round_complete'] is True:
            round_status = Controller.make_status(self, tour_id)
            for item in round_status[1]:
                """list element = (player_id, score, ranking)"""
                list_player_score_rank.append((item[4], item[0], item[5]))
            # print(list_player_score_rank)
            """Need all matches already played and round scores"""
            """round_status[1] contains ordered by score,ranking : score, played,
            round_num, player, player_id, player_rk for the 8 players"""
            matches = self.db.get_match(tour_id)
            """Extract a list of match already played: For a match P1_id vs P2_id add to the list (P1_id, P2_id)"""
            for item in matches:
                """Sanity check"""
                if item[1] == 'unk':
                    print("Round not completed : programming Error!!!")
                else:
                    list_of_match_played.append((item[7], item[8]))
                    # print("list_of_match_played: ",list_of_match_played)
            """Now we have got the list of match played and the list of scores:
                To create the list of new matches iterate player in list_player_score_rank,
                check if already enrolled in the new round, if not add player in pair, when pair complete
                check if pair has already played, if not add to new list otherwise replace players with
                next player in the list ranked by score and ranking"""
            pair = []
            # print("list_new_matches: ", list_new_matches)
            skipped_player = []
            while len(list_new_matches) != int(len(list_player_score_rank) / 2):
                for player in list_player_score_rank:
                    """Check if player already engaged.Skip for loop if list_new_matches empty"""
                    player_engaged = False
                    for matches in list_new_matches:
                        if player[0] in matches:
                            player_engaged = True
                            break
                    if player_engaged is False:
                        if len(pair) == 0:
                            """Add first player"""
                            pair.append(player[0])
                        elif len(pair) == 1:
                            """Add second player"""
                            pair.append(player[0])
                        else:
                            print("Pair complete : programming Error!!!")
                    if len(pair) == 2:
                        """A candidate pair has been found.Need checking if the pair already played"""
                        # print("pair: ", pair)
                        pair12 = (pair[0], pair[1])
                        pair21 = (pair[1], pair[0])
                        if pair[0] == pair[1]:
                            """No possible pair found. Undefined requirement. Choose to pair with last player checked
                            and rejected because the pair already played"""
                            pair[1] = skipped_player.pop()
                            list_new_matches.append(pair)
                            pair = []
                            skipped_player = []
                        elif pair12 in list_of_match_played or pair21 in list_of_match_played:
                            """Pair has already played, select another player2"""
                            # print("Pair already found: ", pair12)
                            skipped_player.append(pair[1])
                            pair = [pair[0], ]
                        else:
                            list_new_matches.append(pair)
                            pair = []
                            skipped_player = []
                            # print("list_of_new_matches: ", list_new_matches)
                            break
            for match in list_new_matches:
                """Create matches"""
                self.db.insert_match('unk', round['Round_number'] + 1, tour_id, match[0], match[1])
            return round
        elif round['Round_number'] != 0 and round['Round_complete'] is False:
            """Return request to complete to complete round"""
            return round
