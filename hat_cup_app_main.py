"""
ilya pogodaev, 2019
"""

import click
import json
import logging

TABLE_DEFAULT_SIZE = 7
CURRENT_CUP_NUMBER = 3

FIRST_QUALIFICATION_STAGE_ID = "qual_1"
SECOND_QUALIFICATION_STAGE_ID = "qual_2"
FINAL_STAGE_ID = "final_1"

DEFAULT_DATABASE_FILE_NAME = 'data.json'
LOG_FILE_NAME = "sample.log"


def setup_logger():
    logger = logging.getLogger('hat_cup_app')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('sample.log', mode='w')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logging.basicConfig(filename="sample.log", level=logging.INFO)


@click.group()
@click.pass_context
def main(ctx):
    setup_logger()
    ctx.obj = load_data()
    if ctx.obj is None:
        ctx.obj = dict()
    logging.info('Data loaded.')


def load_data() -> dict:
    with open(DEFAULT_DATABASE_FILE_NAME, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    return data


@main.resultcallback()
@click.pass_obj
def save_data(data: dict, result):
    with open(DEFAULT_DATABASE_FILE_NAME, 'w', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
    logging.info('Data saved.')


# Commands.
@main.command(help="Добавить результаты в базу")
def add_results():
    raise NotImplementedError


@main.command(help="Добавить игрока в базу")
@click.pass_obj
def add_player(data):
    print(data)
    new_player_name = ""
    while not len(new_player_name):
        new_player_name = click.prompt("Введите имя и фамилию")
    print(type(data))
    if new_player_name in data.keys():
        print("Игрок уже есть в базе")
        return
    data[new_player_name] = new_player_name


@main.command(help="Добавить игроков в базу")
def add_players():
    raise NotImplementedError


@main.command(help="Сгенерировать сетку")
def generate_grid():
    raise NotImplementedError


@main.command(help="Распечатать результаты")
def write_results():
    raise NotImplementedError


@main.command(help="Распечатать сетку")
def write_grid():
    raise NotImplementedError


if __name__ == "__main__":
    global data
    data = dict()
    main()
