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
        if len(competitors) == 0:
            return False
        else:
            for player_id in player_list:
                self.db.insert_competitor(tour_id, player_id)
            return True

    def display_player(self):
        return self.db.get_players()

    def display_ranked_player(self):
        return self.db.get_ranked_players()

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

    def display_round(self, tour_num, round_num):
        tour_table_size = self.db.get_table_size('tournaments')
        if tour_table_size != 0:
            return (True, tour_table_size,  self.db.get_rounds(tour_num, round_num))
        else:
            return (False, 0, None)
