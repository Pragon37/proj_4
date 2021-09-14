from database import *


insert_player('John', 'Doe', '2002-01-25', 'M', 1024)
insert_player('Bill', 'Bee', '2003-02-06', 'M', 1124)
insert_player('Jack', 'Dog', '2001-03-15', 'M', 1224)
insert_player('Mary', 'Cat', '2000-02-28', 'F', 1324)
insert_player('Tess', 'Lee', '2002-09-02', 'F', 1224)
insert_player('Cam',  'Yeo', '2001-12-17', 'M', 1124)
insert_player('Josh', 'Teo', '2001-09-20', 'M', 1024)
insert_player('Kate', 'Pike', '2000-01-15', 'F', 1624)
insert_player('Ken', 'Owen', '2004-12-07', 'M', 1022)
insert_player('Nick', 'Ryan', '2004-03-09', 'M', 1101)
insert_player('Len', 'West', '2005-06-25', 'M', 1004)
insert_player('Dale', 'Yale', '2002-08-14', 'M', 1050)
insert_player('Ben', 'Page', '2001-09-11', 'M', 1118)
insert_player('Jim', 'Day', '2000-10-23', 'M', 1128)
insert_player('Liz', 'Roy', '2003-01-30', 'F', 1204)
insert_player('Abby', 'Cox', '2003-04-16', 'F', 1080)
insert_player('Jane', 'Gay', '2004-03-14', 'F', 1115)
insert_player('Jay', 'Lam', '2003-03-02', 'F', 1150)
insert_player('Amy', 'Lam', '2000-10-10', 'F', 1150)
insert_player('Joe', 'Lam', '2000-10-10', 'M', 1150)
insert_player('Ash', 'Abb', '2005-08-27', 'M', 1124)



insert_competitor(1, 1)
insert_competitor(1, 2)
insert_competitor(1, 3)
insert_competitor(1, 4)

insert_competitor(1, 5)
insert_competitor(1, 6)
insert_competitor(1, 7)
insert_competitor(1, 8)

insert_competitor(2, 10)
insert_competitor(2, 11)
insert_competitor(2, 12)
insert_competitor(2, 13)

insert_competitor(2, 14)
insert_competitor(2, 15)
insert_competitor(2, 16)
insert_competitor(2, 17)

print(3 * '\n')
insert_competitor(1, 1)
print(3 * '\n')

x = c.execute("SELECT player_id, first_name, last_name, birth_date, sex, ranking FROM player WHERE player_id == 8")
print(x.fetchone())
x = c.execute("SELECT player_id, first_name, last_name, birth_date, sex, ranking FROM player WHERE player_id == 3")
print(x.fetchone())
x = c.execute("SELECT player_id, first_name, last_name, birth_date, sex, ranking FROM player WHERE player_id == 7")
print(x.fetchone())


insert_match('tie', 1, 1, 7, 2)
insert_match('pl2', 1, 1, 3, 4)
insert_match('pl1', 1, 1, 6, 9)
insert_match('pl1', 1, 1, 5, 8)

insert_match('pl1', 2, 1, 7, 3)
insert_match('pl1', 2, 1, 2, 4)
insert_match('pl2', 2, 1, 6, 5)
insert_match('pl2', 2, 1, 9, 8)

insert_match('pl2', 3, 1, 7, 8)
insert_match('tie', 3, 1, 3, 9)
insert_match('tie', 3, 1, 6, 4)
insert_match('pl1', 3, 1, 5, 2)

insert_match('tie', 4, 1, 7, 9)
insert_match('tie', 4, 1, 3, 8)
insert_match('pl2', 4, 1, 6, 2)
insert_match('pl1', 4, 1, 5, 4)

y = c.execute("SELECT match_id FROM  matches ")
print(y.fetchall())
z = c.execute("SELECT first_name,last_name FROM player WHERE player_id IN (SELECT player2_id FROM MATCHES)")
print(z.fetchall())
ze = c.execute("SELECT player_id FROM  player WHERE player_id = 9 ")
print(ze.fetchall())



display_player()
display_ranked_player()

"""The tour id (tour_id) is stringified and then subsituted in the QUERY"""

display_player(QUERY_COMPETITORS.replace('num', str(2)))
display_ranked_player(QUERY_RANKED_COMPETITORS.replace('num', str(1)))

insert_tour('Paris_21','Paris','2021-06-01')
insert_tour('Rome_21','Rome','2021-05-01')
insert_tour('London_21','London','2021-04-01')
insert_tour('Berlin_21','Berlin','2021-03-01')
insert_tour('Zurich_21','Zurich','2021-02-01')

display_tour()

print(3 * '\n')
display_round(QUERY_ROUNDS.replace('tour_num', str(1)).replace('round_num', str(1)))

print(3 * '\n')
display_round(QUERY_ROUNDS.replace('tour_num', str(1)).replace('round_num', str(2)))

print(3 * '\n')
display_round(QUERY_ROUNDS.replace('tour_num', str(1)).replace('round_num', str(3)))

print(3 * '\n')
display_round(QUERY_ROUNDS.replace('tour_num', str(1)).replace('round_num', str(4)))

print(3 * '\n')
display_match(QUERY_MATCHES.replace('tour_num', str(1)))
