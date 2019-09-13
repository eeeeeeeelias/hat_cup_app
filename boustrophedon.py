# def get_boustrophedon(db : dict, num_tables: int, normal_table_size, num_pools: int = 1):
def get_boustrophedon(num_tables: int, num_pools: int, num_players: int):
    # 39, 6 -> 6
    # 42, 6 -> 7
    normal_table_size = num_players // num_tables
    table_sizes = [normal_table_size for table_id in range(num_tables)]
    tables = [['' for player_id in range(table_sizes[table_id] + 1)] for table_id in range(num_tables)]
    # scoreboard = get_scoreboard()
    scoreboard = [i for i in range(num_players)]
    for i in range(len(scoreboard)):
        scoreboard[i] = {
            "name" : str("name{0} surname{0}".format(i)),
            "score" : 100 - i,
        }
    print(scoreboard)
    player_id = 0
    from_left_to_right = True
    max_top_pot_id = normal_table_size // 2
    for pot_id in range(max_top_pot_id):
        for table_id in range(num_tables):
            if normal_table_size % 2 == 0:
                # start from first table and first table
                if from_left_to_right:
                    tables[table_id][pot_id] = scoreboard[player_id]["name"]
                    tables[table_id][normal_table_size - pot_id] = scoreboard[len(scoreboard) - player_id - 1]["name"]
                else:
                    tables[num_tables - table_id - 1][pot_id] = scoreboard[player_id]["name"]
                    tables[num_tables - table_id - 1][normal_table_size - pot_id] = scoreboard[len(scoreboard) - player_id - 1]["name"]
            else:
                # start from first table and last table
                if from_left_to_right:
                    tables[table_id][pot_id] = scoreboard[player_id]["name"]
                    tables[num_tables - table_id - 1][normal_table_size - pot_id] = scoreboard[len(scoreboard) - player_id - 1]["name"]
                else:
                    tables[num_tables - table_id - 1][pot_id] = scoreboard[player_id]["name"]
                    tables[table_id][normal_table_size - pot_id] = scoreboard[len(scoreboard) - player_id - 1]["name"]
            player_id += 1
        from_left_to_right = not from_left_to_right
    added_table_id = 0
    if normal_table_size % 2 != 0:
        for table_id in range()
    '''
    for added_player_id in range(player_id, len(scoreboard) - player_id - 1):
        if normal_table_size % 2 == 0:
            tables[added_table_id][normal_table_size // 2] = scoreboard[added_player_id]["name"]
        else:
    '''     
    return tables

if __name__ == '__main__':
    grid = get_boustrophedon(5, 1, 39)
    table_id = 1
    for table in grid:
        formatted_table = ['{:>20}'.format(item) for item in table]
        print('=' * 140)
        print('Table {} : '.format(table_id), end='')
        print(' '.join(formatted_table))
        table_id += 1
