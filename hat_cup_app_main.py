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


# Commands.
@main.command(help='Добавить результаты в базу')
@click.option('--cup', 'cup_', default=CURRENT_CUP_ID, show_default=True, help='Номер кубка', type=int)
@click.option('--table', 'table_', default=NOT_DEFINED, help='Номер стола', type=int)
@click.option('--size', 'size_', default=NOT_DEFINED, help='Число игроков за столом', type=int)
@click.pass_obj
def add_results(data, cup_, table_, size_):
    while not is_valid_cup(cup_):
        cup_ = int(click.prompt('Введите номер кубка'))
    while not is_valid_table(table_):
        table_ = int(click.prompt('Введите номер стола'))
    while not is_valid_size(size_):
        size_ = int(click.prompt('Введите количество игроков за столом'))
    logging.info('cup == {}'.format(cup_))
    logging.info('table == {}'.format(table_))
    logging.info('size == {}'.format(size_))
    for player_id in range(size_):
        player_name = ''
        while not is_found_in_db(data, dataplayer_name):
            player_name = click.prompt('Введите имя игрока')
        player_score = NOT_DEFINED
        while is_valid_score(player_score):
            player_score = int(click.prompt('Введите число очков'))
        raise NotImplementedError


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
    data[new_player_name] = new_player_name


@main.command(help='Сгенерировать сетку')
def generate_grid():
    raise NotImplementedError


@main.command(help='Распечатать результаты')
def write_results():
    raise NotImplementedError


@main.command(help='Распечатать сетку')
def write_grid():
    raise NotImplementedError


if __name__ == '__main__':
    global data
    data = dict()
    main()
