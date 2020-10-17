import pandas as pd
import sys


input_data_path = 'data/input'
files = [
    f'{input_data_path}/air_reserve.csv',
    f'{input_data_path}/air_visit_data.csv',
    f'{input_data_path}/hpg_reserve.csv',
    f'{input_data_path}/air_store_info.csv',
    f'{input_data_path}/date_info.csv',
    f'{input_data_path}/hpg_store_info.csv',
    f'{input_data_path}/store_id_relation.csv',
]


def main():
    for arg in sys.argv:
        if arg in files:
            func_name = arg.split('/')[-1].split('.')[0]
            globals()[func_name]()

    if len(sys.argv) == 1:
        air_reserve()
        air_visit_data()
        hpg_reserve()
        air_store_info()
        date_info()
        hpg_store_info()
        store_id_relation()


def air_reserve():
    file_name = 'air_reserve'
    pd.read_csv(
        f'{input_data_path}/{file_name}.csv',
        encoding='utf-8',
        parse_dates=['visit_datetime', 'reserve_datetime']
    ).to_feather(f'{input_data_path}/{file_name}.feather')


def air_visit_data():
    file_name = 'air_visit_data'
    pd.read_csv(
        f'{input_data_path}/{file_name}.csv',
        encoding='utf-8',
        parse_dates=['visit_date']
    ).to_feather(f'{input_data_path}/{file_name}.feather')


def hpg_reserve():
    file_name = 'hpg_reserve'
    pd.read_csv(
        f'{input_data_path}/{file_name}.csv',
        encoding='utf-8',
        parse_dates=['visit_datetime', 'reserve_datetime']
    ).to_feather(f'{input_data_path}/{file_name}.feather')


def air_store_info():
    file_name = 'air_store_info'
    pd.read_csv(
        f'{input_data_path}/{file_name}.csv',
        encoding='utf-8',
    ).to_feather(f'{input_data_path}/{file_name}.feather')


def date_info():
    file_name = 'date_info'
    pd.read_csv(
        f'{input_data_path}/{file_name}.csv',
        encoding='utf-8',
        parse_dates=['calendar_date']
    ).to_feather(f'{input_data_path}/{file_name}.feather')


def hpg_store_info():
    file_name = 'hpg_store_info'
    pd.read_csv(
        f'{input_data_path}/{file_name}.csv',
        encoding='utf-8',
    ).to_feather(f'{input_data_path}/{file_name}.feather')


def store_id_relation():
    file_name = 'store_id_relation'
    pd.read_csv(
        f'{input_data_path}/{file_name}.csv',
        encoding='utf-8',
    ).to_feather(f'{input_data_path}/{file_name}.feather')


if __name__ == '__main__':
    main()
