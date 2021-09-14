"""This file contains the database definition.It consists of 4 tables : players, competitors,
   matches, tournaments"""

import sqlite3

"""Connect the database (memory located for the time being) and setup access cursor"""
conn = sqlite3.connect(":memory:")
c = conn.cursor()

"""player table consists of players that already have participated to a tournament"""
c.execute("""CREATE TABLE player (
            player_id integer PRIMARY KEY,
            first_name  text NOT NULL,
            last_name   text NOT NULL,
            birth_date  text NOT NULL,
            sex         text NOT NULL,
            ranking     integer  NOT NULL
            )""")


def insert_player(first_name, last_name, birth_date, sex, ranking):
    """insert_player records new player"""
    with conn:
        c.execute("INSERT INTO player VALUES (NULL, :first_name, :last_name, :birth_date, :sex, :ranking)",
                  {'first_name': first_name, 'last_name': last_name, 'birth_date': birth_date, 'sex': sex,
                   'ranking': ranking})


"""competitors table records players engaged in a tournament identified by tour_id.
   Parent table : tournaments, player. A player can only be at most once in a competitors table.
   There is only one competitors table per tournament"""
c.execute("""CREATE TABLE competitors (
             id INTEGER PRIMARY KEY,
             tour_id   INTEGER NOT NULL REFERENCES tournaments(tour_id),
             player_id INTEGER NOT NULL REFERENCES player(player_id),
             UNIQUE(tour_id, player_id)
            )""")


def insert_competitor(tour_id, player_id):
    """insert_competitors adds one player at a time to the competitors table.
       Fires an exception if attempting to add a player already recorded"""
    with conn:
        try:
            c.execute("INSERT INTO competitors VALUES (NULL, :tour_id, :player_id)",
                      {'tour_id': tour_id, 'player_id': player_id})
        except sqlite3.IntegrityError as error:
            print('sqlite3.IntegrityError', error)
            get_player_name(player_id, tour_id)


def get_player_name(player_id, tour_id):
    """Reports name of a player from player_id"""
    name_query = "SELECT first_name,last_name FROM player WHERE  player_id = " + str(player_id)
    name = c.execute(name_query)
    print(' '.join(name.fetchone()), ": Player already enrolled in tour : ", tour_id)


"""matches table records 2 players enaged in a match and the match result (TIE,PL1,PL2).
   Parent table : tournaments, player."""

c.execute("""CREATE TABLE matches (
            match_id    INTEGER PRIMARY KEY,
            result      TEXT NOT NULL,
            round       INTEGER NOT NULL,
            tour_id     INTEGER  NOT NULL REFERENCES tournaments(tour_id),
            player1_id  INTEGER  NOT NULL REFERENCES player(player_id),
            player2_id  INTEGER  NOT NULL REFERENCES player(player_id)
            )""")


def insert_match(result, round, tour_id, player1_id, player2_id):
    """Insert match result, round, tournament and match participant in the matches table"""
    with conn:
        c.execute("INSERT INTO matches VALUES (NULL, :result, :round, :tour_id, :player1_id, :player2_id)",
                  {'result': result,
                   'round': round,
                   'tour_id': tour_id,
                   'player1_id': player1_id,
                   'player2_id': player2_id})


"""Records the tournaments list. Consists of tournamet name, venue and date"""
c.execute("""CREATE TABLE tournaments (
            tour_id        INTEGER PRIMARY KEY,
            name           TEXT NOT NULL,
            venue          TEXT NOT NULL UNIQUE,
            date           TEXT NOT NULL UNIQUE
            )""")


def insert_tour(name, venue, date):
    """insert a tournament in the tournaments table"""
    with conn:
        c.execute("INSERT INTO tournaments VALUES (NULL, :name, :venue, :date)",
                  {'name': name,
                   'venue': venue,
                   'date': date})


"""query to get the player list sorted by names"""
QUERY_PLAYERS = """SELECT last_name, first_name
                   FROM player
                   ORDER BY last_name, first_name"""

"""query to get the player list sorted by ranking"""
QUERY_RANKED_PLAYERS = """SELECT last_name, first_name, ranking
                          FROM player
                          ORDER BY ranking, last_name, first_name"""

"""query to get the competitors(group of players participant in a tournament) sorted by names"""
QUERY_COMPETITORS = """SELECT last_name, first_name
                       FROM player
                       WHERE player_id
                       IN
                       (SELECT player_id FROM competitors WHERE tour_id = num)
                       ORDER BY last_name, first_name"""

"""query to get the competitors(group of players participant in a tournament) sorted by ranking"""
QUERY_RANKED_COMPETITORS = """SELECT last_name, first_name, ranking
                              FROM player
                              WHERE player_id
                              IN (SELECT player_id FROM competitors WHERE tour_id = num)
                              ORDER BY ranking, last_name, first_name"""


def display_player(query=QUERY_PLAYERS):
    """print (all) the player list sorted by name"""
    with conn:
        name = c.execute(query)
        print(25 * '-')
        print('{0:<20s}'.format('Player'))
        print(25 * '-')
        for last_first in (name.fetchall()):
            print('{0:<20s}'.format(' '.join(last_first[0:2])))


def display_ranked_player(query=QUERY_RANKED_PLAYERS):
    """print (all) the player list sorted by ranking"""
    with conn:
        name = c.execute(query)
        print(40 * '-')
        print('{0:<20s}{1:<4s}'.format('Player', 'Ranking'))
        print(40 * '-')
        for last_first_rank in (name.fetchall()):
            print('{0:<20s}{1:<4d}'.format(' '.join(last_first_rank[0:2]), last_first_rank[2]))


"""Query to get all the recorded tournaments"""
QUERY_TOURS = """SELECT name, venue, date
                   FROM tournaments
                   ORDER BY date"""


def display_tour(query=QUERY_TOURS):
    """print (all) the tournaments sorted by date"""
    with conn:
        name = c.execute(query)
        print(37 * '-')
        print('{0:<16s}{1:<16s}{2:<16s}'.format('Name', 'Venue', 'Date'))
        print(37 * '-')
        for tour in (name.fetchall()):
            print('{0:<16s} {1:<16s}{2:<16s}'.format(tour[0], tour[1], tour[2]))


QUERY_ROUNDS = """SELECT result, player1.first_name, player1.last_name, player2.first_name, player2.last_name
                  FROM
                  matches
                  JOIN player AS player1 ON player1.player_id = matches.player1_id
                  JOIN player AS player2 ON player2.player_id = matches.player2_id
                  WHERE matches.tour_id = tour_num AND matches.round = round_num
                  """


def display_round(query=QUERY_ROUNDS):
    """print all matches results and contestants in a round"""
    print(50 * '-')
    print('{0:<10s}{1:<20s}{2:<20s}'.
          format('Result', 'Player1', 'Player2'))
    print(50 * '-')
    with conn:
        result = c.execute(query)
        for round in (result.fetchall()):
            print('{0:<10s}{1:<20s}{2:<20s}'.format(round[0], ' '.join(round[1:3]), ' '.join(round[3:5])))


QUERY_MATCHES = """SELECT round,
                   result,
                   player1.first_name,
                   player1.last_name,
                   player2.first_name,
                   player2.last_name
                  FROM
                  matches
                  JOIN player AS player1 ON player1.player_id = matches.player1_id
                  JOIN player AS player2 ON player2.player_id = matches.player2_id
                  WHERE matches.tour_id = tour_num
                  """


def display_match(query=QUERY_MATCHES):
    """print all matches results and contestants in a tournament"""
    print(50 * '-')
    print('{0:<7s}{1:<10s}{2:<20s}{3:<20s}'.
          format('Round', 'Result', 'Player1', 'Player2'))
    print(50 * '-')
    with conn:
        result = c.execute(query)
        for match in (result.fetchall()):
            print('{0:<7d}{1:<10s}{2:<20s}{3:<20s}'.
                  format(match[0], match[1], ' '.join(match[2:4]), ' '.join(match[4:6])))
