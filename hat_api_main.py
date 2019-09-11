TABLE_DEFAULT_SIZE = 7
CURRENT_CUP_NUMBER = 3

import argparse

parser = argparse.ArgumentParser()
api_actions = parser.add_mutually_exclusive_group()
api_actions.add_argument("-add-results", action="store_true", help="Добавить результаты стола")
api_actions.add_argument("-add-player", action="store_true", help="Добавить игрока в базу")
api_actions.add_argument("-compile-grid", action="store_true", help="Сформировать сетку")
api_actions.add_argument("-write-results", action="store_true", help="Распечатать результаты")
api_actions.add_argument("-write-grid", action="store_true", help="Распечатать сетку")
args = parser.parse_args()
