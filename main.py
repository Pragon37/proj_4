"""Entry point."""
from model.database import Database
from controller.controller import Controller
from views.menu import Menu


chessdb = Database("chess.db")
cont = Controller(chessdb)
menu = Menu(cont)
