"""This file contains the database definition.It consists of 4 tables : players, competitors,
   matches, tournaments. It contains all the interface layer with sqlite database"""
import sqlite3


class Database():

    def __init__(self, dbfile):
        self.conn = sqlite3.connect(dbfile)
        self.c = self.conn.cursor()

        # Following instructions setup the database structure
        self.create_table(Database.QUERY_PLAYERS_TABLE)
        self.create_table(Database.QUERY_COMPETITORS_TABLE)
        self.create_table(Database.QUERY_MATCHES_TABLE)
        self.create_table(Database.QUERY_TOURNAMENTS_TABLE)

    """player table consists of players that already have participated to a tournament"""
    QUERY_PLAYERS_TABLE = """CREATE TABLE IF NOT EXISTS player (
                            player_id integer PRIMARY KEY,
                            first_name  text NOT NULL,
                            last_name   text NOT NULL,
                            birth_date  text NOT NULL,
                            sex         text NOT NULL,
                            ranking     integer  NOT NULL
                            )"""

    """competitors table records players engaged in a tournament identified by tour_id.
        Parent table : tournaments, player. A player can only be at most once in a competitors table.
        There is only one competitors table per tournament"""
    QUERY_COMPETITORS_TABLE = """CREATE TABLE IF NOT EXISTS competitors (
                                 id INTEGER PRIMARY KEY,
                                 tour_id   INTEGER NOT NULL REFERENCES tournaments(tour_id),
                                 player_id INTEGER NOT NULL REFERENCES player(player_id),
                                 UNIQUE(tour_id, player_id)
                                 )"""
    """matches table records 2 players engaged in a match and the match result (TIE,PL1,PL2).
       Parent table : tournaments, player."""
    QUERY_MATCHES_TABLE = """CREATE TABLE IF NOT EXISTS matches (
                                match_id    INTEGER PRIMARY KEY,
                                result      TEXT NOT NULL,
                                round       INTEGER NOT NULL,
                                tour_id     INTEGER  NOT NULL REFERENCES tournaments(tour_id),
                                player1_id  INTEGER  NOT NULL REFERENCES player(player_id),
                                player2_id  INTEGER  NOT NULL REFERENCES player(player_id)
                                )"""

    """Records the tournaments list. Consists of tournament name, venue and date"""
    QUERY_TOURNAMENTS_TABLE = """CREATE TABLE IF NOT EXISTS tournaments (
                                tour_id        INTEGER PRIMARY KEY,
                                name           TEXT NOT NULL,
                                venue          TEXT NOT NULL UNIQUE,
                                date           TEXT NOT NULL UNIQUE
                                )"""

    def create_table(self, query):
        """generic wrapper to execute a query"""
        self.c.execute(query)

    def get_table_size(self, table_name):
        """return table_name number of rows"""
        with self.conn:
            return self.c.execute("SELECT COUNT(*) from {0}".format(table_name)).fetchone()[0]

    def insert_player(self, first_name, last_name, birth_date, sex, ranking):
        """insert_player records new player"""
        with self.conn:
            self.c.execute("INSERT INTO player VALUES (NULL, :first_name, :last_name, :birth_date, :sex, :ranking)",
                           {'first_name': first_name, 'last_name': last_name, 'birth_date': birth_date, 'sex': sex,
                            'ranking': ranking})
        print("New Player inserted")

    def update_player(self, player_id, ranking):
        """Update player ranking"""
        with self.conn:
            new_ranking = (ranking, player_id)
            self.c.execute("UPDATE player SET ranking = ? WHERE player_id = ?", new_ranking)

    def update_match(self, match_id, result):
        """Update match_id result"""
        with self.conn:
            new_result = (result, match_id)
            self.c.execute("UPDATE matches SET result = ? WHERE match_id = ?", new_result)

    def insert_competitor(self, tour_id, player_id):
        """insert_competitors adds one player at a time to the competitors table"""
        with self.conn:
            self.c.execute("INSERT INTO competitors VALUES (NULL, :tour_id, :player_id)",
                           {'tour_id': tour_id, 'player_id': player_id})

    def get_player_name(self, player_id, tour_id):
        """Reports name of a player from player_id"""
        name_query = "SELECT first_name,last_name FROM player WHERE  player_id = " + str(player_id)
        name = self.c.execute(name_query)
        print(' '.join(name.fetchone()), ": Player already enrolled in tour : ", tour_id)

    def insert_match(self, result, round, tour_id, player1_id, player2_id):
        """Insert match result, round, tournament and match participant in the matches table"""
        with self.conn:
            self.c.execute("INSERT INTO matches VALUES (NULL, :result, :round, :tour_id, :player1_id, :player2_id)",
                           {'result': result,
                            'round': round,
                            'tour_id': tour_id,
                            'player1_id': player1_id,
                            'player2_id': player2_id})

    def insert_tour(self, name, venue, date):
        """insert a tournament in the tournaments table"""
        with self.conn:
            self.c.execute("INSERT INTO tournaments VALUES (NULL, :name, :venue, :date)",
                           {'name': name,
                            'venue': venue,
                            'date': date})

    def get_player(self, player_id):
        """Retrieve player data for player_id"""
        with self.conn:
            name = self.c.execute(f"SELECT player_id, first_name, last_name, birth_date, sex, ranking FROM player\
                                    WHERE player_id == {player_id}")
            return(name.fetchone())

    def exist_player(self, last_name):
        """Checks if player with last_name exists"""
        with self.conn:
            name = self.c.execute(f"SELECT first_name, last_name FROM player\
                                    WHERE last_name = \"{last_name}\"")
            return(name.fetchall())

    def exist_tour(self, tour_name):
        """Checks if  tour = tour_name exists"""
        with self.conn:
            name = self.c.execute(f"SELECT name FROM tournaments\
                                    WHERE name = \"{tour_name}\"")
            return(name.fetchall())

    def exist_competition(self, tour_id):
        """Checks if competitors have been added for tour = tour_id"""
        with self.conn:
            name = self.c.execute(f"SELECT player_id FROM competitors\
                                    WHERE tour_id = {tour_id}")
            return(name.fetchall())

    def get_players(self):
        """return all the players sorted by name"""
        with self.conn:
            name = self.c.execute("""SELECT player_id, last_name, first_name
                                     FROM player
                                     ORDER BY last_name, first_name""")
            return(name.fetchall())

    def get_ranked_players(self):
        """return all the players sorted by ranking"""
        with self.conn:
            name = self.c.execute("""SELECT player_id, last_name, first_name, ranking
                                     FROM player
                                     ORDER BY ranking, last_name, first_name""")
            return(name.fetchall())

    def get_tour(self):
        """get (all) the tournaments sorted by date"""
        with self.conn:
            name = self.c.execute("""SELECT rowid, name, venue, date
                                     FROM tournaments
                                     ORDER BY date""")
            return(name.fetchall())

    def get_rounds(self, tour_num, round_num):
        """get all matches results and contestants in a round"""
        with self.conn:
            result = self.c.execute(f"SELECT result, player1.first_name, player1.last_name, player2.first_name, player2.last_name\
                                        FROM\
                                        matches\
                                        JOIN player AS player1 ON player1.player_id = matches.player1_id\
                                        JOIN player AS player2 ON player2.player_id = matches.player2_id\
                                        WHERE matches.tour_id == {tour_num} AND matches.round == {round_num}")
            return(result.fetchall())

    def get_match(self, tour_num):
        """get all matches results and contestants in tournament tour_num"""
        with self.conn:
            result = self.c.execute(f"SELECT round,\
                                      result,\
                                      player1.first_name,\
                                      player1.last_name,\
                                      player2.first_name,\
                                      player2.last_name,\
                                      tournaments.name,\
                                      player1.player_id,\
                                      player2.player_id,\
                                      player1.ranking,\
                                      player2.ranking,\
                                      match_id\
                                      FROM\
                                      matches\
                                      JOIN player AS player1 ON player1.player_id = matches.player1_id\
                                      JOIN player AS player2 ON player2.player_id = matches.player2_id\
                                      JOIN tournaments  ON tournaments.tour_id = matches.tour_id\
                                      WHERE matches.tour_id = {tour_num}")
            return(result.fetchall())

    def get_unk_match(self):
        """get all matches which result is unk and contestants in tournament tour_num"""
        with self.conn:
            result = self.c.execute("SELECT round,\
                                     result,\
                                     player1.first_name,\
                                     player1.last_name,\
                                     player2.first_name,\
                                     player2.last_name,\
                                     tournaments.name,\
                                     player1.player_id,\
                                     player2.player_id,\
                                     player1.ranking,\
                                     player2.ranking,\
                                     match_id\
                                     FROM\
                                     matches\
                                     JOIN player AS player1 ON player1.player_id = matches.player1_id\
                                     JOIN player AS player2 ON player2.player_id = matches.player2_id\
                                     JOIN tournaments  ON tournaments.tour_id = matches.tour_id\
                                     WHERE matches.result = 'unk'")
            return(result.fetchall())

    def get_competitors(self, tour_num):
        """return all the competitors sorted by name"""
        with self.conn:
            name = self.c.execute(f"SELECT player_id, first_name, last_name, ranking\
                                     FROM player\
                                     WHERE player_id\
                                     IN\
                                     (SELECT player_id FROM competitors WHERE tour_id = {tour_num})\
                                     ORDER BY last_name, first_name")
            return(name.fetchall())

    def get_ranked_competitors(self, tour_num):
        """return all the competitors sorted by rank. Suppose that competitors are already added"""
        with self.conn:
            name = self.c.execute(f"SELECT player_id, ranking\
                                    FROM player\
                                    WHERE player_id\
                                    IN (SELECT player_id FROM competitors WHERE tour_id = {tour_num})\
                                    ORDER BY ranking DESC, last_name, first_name")
            return(name.fetchall())
