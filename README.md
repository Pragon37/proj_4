# Proj_4 :Tournament manager

[Project 4](https://github.com/Pragon37/proj_4)

Tournament manager is an application that generates contests using the swiss pairing system,
and provides immediate record for the tournament participants and results.
t is designed after the specification of openclassroom project 4.

## Installing / Getting started

It is implemented as a python program. To setup the environment you need to execute the following instructions:

```shell
python -m venv env
env/Scripts/activate
pip install -r requirements.txt
python main.py
```

It will display a menu that serves as a user interface.

1 Add player
2 Add tournament
3 Add competitors
4 Add result
5 Display tournament
6 Display Round
7 Display Players
8 Display matches
9 Display scores
10 Display competitors
11 Add new round
12 Update ranking
13 Quit
Select a menu item:

## Developing


```shell
git clone https://github.com/Pragon37/proj_4
cd proj_4/
```

And state what happens step-by-step.


## Features

* What's the main functionality
The program lets you enter new tournaments, and add players to the existing databse.
Once a new tournament has been added, it is possible add the competitors for this
tournament and to pair the player for all the contests of  round. Once the matched
are terminated results of the match can be put in the record and a new round of contests
can be generated using a swiss pairing system. It is also possible to edit the ranking
of a player.
Menu are self explanatory and it is possible to give up an action at any intermediate step by
typing in 'q'.


 * At any time:
It is possible to display the recorded tournaments, the player list sorted alphabetically or by ranking.
Round and match results, competitors for a tournament, scores of an going can also be displayed.

* Any change or addition is recorded as soon as it has been entered in the menu.

## Usage examples:

1- Adding a player :
Select a menu item:1
Enter player first name:John
Enter player last name:Doe
Enter player birth date yyyy-mm-dd:2002-02-20
Enter player gender (M or F):M
Enter ranking (nnnn):1234

2-Adding a tournament
Select a menu item:2
Enter tournament name:Paris_21
Enter tournament venue:Paris
Enter tournament date:2021-11-20

3-Add competitors
Select a menu item:3
Enter tournament id (<= 1) :1
Enter 8 player id (1 <= id <= 8) separated by spaces or q:1 2 3 4 5 6 7 8

11-Add new round
Select a menu item:11
Enter tournament id (<= 1) :1

6-Display round
Enter tournament id (<= 1) :1
Enter round number :1

5-Display tournament
Select a menu item:5

7-Display Players
Select a menu item:7
Enter a(ll) / r(ranked) / player ID :a

8-Display matches
Select a menu item:8
Enter tournament id (<= 1) :1

4-Add result
Select a menu item:4

 ------------------------------------------------------------------------------------------
 Tour                Round  Result    Player1             Player2             match_id
 ------------------------------------------------------------------------------------------
 Paris_21            1      unk       Jos Carr            John Doe            1
 Paris_21            1      unk       Alf Lee             Sam Bat             2
 Paris_21            1      unk       Dan Shaw            Ron Catt            3
 Paris_21            1      unk       Jeff Hunt           Bill Bee            4


[1, 2, 3, 4]
Enter match_id in:[1, 2, 3, 4] or q:1
Enter match_id in:[1, 2, 3, 4] or q:1
Enter result (tie, pl1, pl2) for: 1 or q:pl1

12-Update ranking
Select a menu item:12
Enter player id (1 <= id <= 8) or q:1

 --------------------------------------------------------------------------------
 Pid  first_name          last_name           birth_date          sex  Ranking
 --------------------------------------------------------------------------------
 1    John                Doe                 2002-02-20          M    1234
 --------------------------------------------------------------------------------

Enter ranking (nnnn):1236

9-Display Scores
Select a menu item:9

 Enter tournament id (<= 1) :1
 ----------------------------------------------------------------------
 Tour Round  Played Player              Pid    Score     Ranking
 1    1      1      Jos Carr            6      1.0       1342
 1    1      0      Alf Lee             5      0.0       1322
 1    1      0      Dan Shaw            8      0.0       1301
 1    1      0      Jeff Hunt           3      0.0       1287
 1    1      1      John Doe            1      0.0       1236
 1    1      0      Sam Bat             4      0.0       1223
 1    1      0      Ron Catt            7      0.0       1199
 1    1      0      Bill Bee            2      0.0       1100
 ----------------------------------------------------------------------

## Links


- Project homepage : [Project 4](https://github.com/Pragon37/proj_4)
- Repository: https://github.com/Pragon37/proj_4.git


## Author

Pierre : pragon37@outlook.fr
