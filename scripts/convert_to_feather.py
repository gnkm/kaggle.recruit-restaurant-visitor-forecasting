import pandas as pd

target = [
    'air_reserve',
    'air_visit_data',
    'hpg_reserve',
    'sample_submission',
    'air_store_info',
    'date_info',
    'hpg_store_info',
    'store_id_relation',
]

extension = 'csv'
# extension = 'tsv'
# extension = 'zip'

for t in target:
    pd.read_csv('./data/input/' + t + '.' + extension, encoding="utf-8")\
        .to_feather('./data/input/' + t + '.feather')
