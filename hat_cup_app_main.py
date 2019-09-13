#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
ilya pogodaev, 2019
'''

import click
import json
import logging

TABLE_DEFAULT_SIZE = 7
TABLE_MIN_SIZE = 6
TABLE_MAX_SIZE = 8
CURRENT_CUP_ID = 3
NOT_DEFINED = -1000

STOPPER_NAME = 'stop'

MAX_CUP_ID = 3
MAX_TABLE_ID = 6

FIRST_QUALIFICATION_STAGE_ID = 'qual_1'
SECOND_QUALIFICATION_STAGE_ID = 'qual_2'
FINAL_STAGE_ID = 'final_1'

DEFAULT_DATABASE_FILE_NAME = 'data.json'
LOG_FILE_NAME = 'sample.log'


def setup_logger():
    logger = logging.getLogger('hat_cup_app')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('sample.log', mode='w')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logging.basicConfig(filename='sample.log', level=logging.INFO)


@click.group()
@click.pass_context
def main(ctx):
    assert CURRENT_CUP_ID <= MAX_CUP_ID, "Кубок {} ещё не существует!".format(CURRENT_CUP_ID)
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


def is_positive_int(x: int) -> bool:
    if x == NOT_DEFINED:
        return False
    if x <= 0:
        print('Введите число больше 0')
        return False
    if type(x) is not int:
        print('Введите число')
        return False
    return True


def is_valid_cup(cup: int) -> bool:
    if not is_positive_int(cup):
        return False
    if cup > MAX_CUP_ID:
        print('Такого кубка ещё нет')
        return False
    return True


def is_valid_table(table: int) -> bool:
    if not is_positive_int(table):
        return False
    if table > MAX_TABLE_ID:
        print('Стола с таким номером нет')
        return False
    return True


def is_valid_size(size: int) -> bool:
    if not is_positive_int(size):
        return False
    if size < TABLE_MIN_SIZE:
        print('Слишком маленький стол')
        return False
    if size > TABLE_MAX_SIZE:
        print('Слишком большой стол')
        return False
    return True


def is_valid_stage_id(stage_id: int) -> bool:
    if not is_positive_int(stage_id):
        return False
    if stage_id > 2:
        return False
    return True


is_valid_score = is_positive_int


# Commands.
@main.command(help='Добавить результаты в базу')
@click.option('--cup', 'cup_', default=CURRENT_CUP_ID, show_default=True, help='Номер кубка', type=int)
@click.option('--table', 'table_', default=NOT_DEFINED, help='Номер стола', type=int)
@click.option('--size', 'size_', default=NOT_DEFINED, help='Число игроков за столом', type=int)
@click.option('--stage-id', 'stage_id_', default=NOT_DEFINED, help='Номер отборочной игры', type=int)
@click.pass_obj
def add_results(data, cup_, table_, size_, stage_id_):
    while not is_valid_cup(cup_):
        cup_ = int(click.prompt('Введите номер кубка'))
    while not is_valid_stage_id(stage_id_):
        stage_id_ = int(click.prompt('Введите номер отборочной игры (1 или 2)'))
    if stage_id_ == 1:
        stage_id_ = FIRST_QUALIFICATION_STAGE_ID
    elif stage_id_ == 2:
        stage_id_ = SECOND_QUALIFICATION_STAGE_ID
    else:
        raise IndexError('В игре только 2 отбора')
    while not is_valid_table(table_):
        table_ = int(click.prompt('Введите номер стола'))
    while not is_valid_size(size_):
        size_ = int(click.prompt('Введите количество игроков за столом'))
    logging.info('cup == {}'.format(cup_))
    logging.info('table == {}'.format(table_))
    logging.info('size == {}'.format(size_))
    for player_id in range(size_):
        player_name = ''
        while True:
            player_name = click.prompt('Введите имя игрока')
            if (player_name == STOPPER_NAME):
                return
            found_player_name = is_found_in_db(data, player_name)
            if len(found_player_name) != 0:
                break
        player_score = NOT_DEFINED
        while not is_valid_score(player_score):
            player_score = int(click.prompt('Введите число очков'))
        player_score = player_score / (size_ - 1) * (TABLE_DEFAULT_SIZE - 1)
        data[found_player_name]["scores"][stage_id_] = player_score
        data[found_player_name]["tables"][stage_id_] = table_


def is_found_in_db(db, player_name: str) -> str:
    player_name = player_name.lower()
    found_players = []
    for candidate_name in db.keys():
        if candidate_name.lower().find(player_name) != -1:
            found_players.append(candidate_name)
    if len(found_players) == 0:
        print('Игрок в базе не найден')
        return ''
    if len(found_players) > 1:
        print('Найдено слишком много игроков:')
        for player in found_players:
            print(db[player]['name'])
        return ''
    print('Найден игрок {}'.format(found_players[0]))
    return found_players[0]


@main.command(help='Добавить игрока в базу')
@click.pass_obj
def add_player(data):
    new_player_name = ''
    while not len(new_player_name):
        new_player_name = click.prompt('Введите имя и фамилию')
    try:
        _add_player_to_db(data, new_player_name)
    except FileExistsError as e:
        logging.warning(e)


@main.command(help='Добавить игроков в базу из файла')
@click.argument('file_name', required=True)
@click.pass_obj
def import_players(data, file_name):
    with open(file_name, 'r', encoding='utf-8') as player_names_file:
        for new_player_name in player_names_file:
            new_player_name = new_player_name.strip()
            try:
                _add_player_to_db(data, new_player_name)
            except FileExistsError as e:
                logging.warning(e)


def _add_player_to_db(data, new_player_name):
    if new_player_name in data.keys():
        raise FileExistsError('Игрок уже есть в базе')
    data[new_player_name] = {
        "name" : new_player_name,
        "scores": {
            FIRST_QUALIFICATION_STAGE_ID : 0,
            SECOND_QUALIFICATION_STAGE_ID : 0,
            FINAL_STAGE_ID : 0,
        },
        "tables": {
            FIRST_QUALIFICATION_STAGE_ID : 0,
            SECOND_QUALIFICATION_STAGE_ID : 0,
            FINAL_STAGE_ID : 0,
        },
    }


import random
@main.command()
@click.pass_obj
def filler(db):
    for player_name in db.keys():
        db[player_name]['scores'][FIRST_QUALIFICATION_STAGE_ID] = random.randint(10, 90)



@main.command(help='Сгенерировать сетку')
def generate_grid():
    raise NotImplementedError


def filter_by_1(candidate_name, db) -> bool:
    return db[candidate_name]['scores'][FIRST_QUALIFICATION_STAGE_ID] > 0

def filter_by_2(candidate_name, db) -> bool:
    return db[candidate_name]['scores'][SECOND_QUALIFICATION_STAGE_ID] > 0

def filter_by_sum(candidate_name, db) -> bool:
    return (
        db[candidate_name]['scores'][FIRST_QUALIFICATION_STAGE_ID] > 0
        or
        db[candidate_name]['scores'][SECOND_QUALIFICATION_STAGE_ID] > 0
        )


def score_by_1(candidate_name, db) -> float:
    return db[candidate_name]['scores'][FIRST_QUALIFICATION_STAGE_ID]

def score_by_2(candidate_name, db) -> float:
    return db[candidate_name]['scores'][SECOND_QUALIFICATION_STAGE_ID]

def score_by_sum(candidate_name, db) -> float:
    return score_by_1(candidate_name, db) + score_by_2(candidate_name, db) * 1.001


def print_1(candidate_names, db) -> None:
    print('Результаты первой игры')
    for i, candidate_name in enumerate(candidate_names):
        print('{:>2} | {:>30} | {:6.2f}'.format(i + 1, candidate_name, db[candidate_name]['scores'][FIRST_QUALIFICATION_STAGE_ID]))

def print_2(candidate_names, db) -> None:
    print('Результаты второй игры')
    for i, candidate_name in enumerate(candidate_names):
        print('{:>2} | {:>30} | {:6.2f}'.format(i + 1, candidate_name, db[candidate_name]['scores'][SECOND_QUALIFICATION_STAGE_ID]))


def print_sum(candidate_names, db) -> None:
    print('Результаты отбора')
    for i, candidate_name in enumerate(candidate_names):
        print('{:>2} | {:>30} | {:6.2f} {:6.2f} | {:6.2f}'.format(
            i + 1,
            candidate_name,
            db[candidate_name]['scores'][FIRST_QUALIFICATION_STAGE_ID],
            db[candidate_name]['scores'][SECOND_QUALIFICATION_STAGE_ID],
            db[candidate_name]['scores'][FIRST_QUALIFICATION_STAGE_ID] + db[candidate_name]['scores'][SECOND_QUALIFICATION_STAGE_ID],
        ))


from functools import partial

@main.command(help='Распечатать результаты')
@click.option('--stage', 'stage_id_', default=NOT_DEFINED, type=int)
@click.pass_obj
def write_results(db, stage_id_):
    ordered_players = [key for key in db.keys()]
    if stage_id_ == 1:
        stage_id_ = FIRST_QUALIFICATION_STAGE_ID
        non_playing_filter = partial(filter_by_1, db=db)
    elif stage_id_ == 2:
        stage_id_ = SECOND_QUALIFICATION_STAGE_ID
        non_playing_filter = partial(filter_by_2, db=db)
    else:
        non_playing_filter = filter_by_sum
        non_playing_filter = partial(filter_by_sum, db=db)
    ordered_players = list(filter(non_playing_filter, ordered_players))
    if stage_id_ == FIRST_QUALIFICATION_STAGE_ID:
        get_score = partial(score_by_1, db=db)
    elif stage_id_ == SECOND_QUALIFICATION_STAGE_ID:
        get_score = partial(score_by_2, db=db)
    else:
        get_score = partial(score_by_sum, db=db)
    ordered_players.sort(key=get_score, reverse=True)
    if stage_id_ == FIRST_QUALIFICATION_STAGE_ID:
        print_results = partial(print_1, db=db)
    elif stage_id_ == SECOND_QUALIFICATION_STAGE_ID:
        print_results = partial(print_2, db=db)
    else:
        print_results = partial(print_sum, db=db)
    print_results(ordered_players)


@main.command(help='Распечатать сетку')
def write_grid():
    raise NotImplementedError


if __name__ == '__main__':
    global data
    data = dict()
    main()
