"""1st Place LGB Model(public:0.470, private:0.502).

[1st Place LGB Model(public:0.470, private:0.502)](https://www.kaggle.com/pureheart/1st-place-lgb-model-public-0-470-private-0-502)

下記コードは一部抜粋，順序を入れ替えたもの．

Summary

予測対象は 2017-04-23 - 2017-05-31 の 39 日．
下記コードでは 2 種類の train データを用いて学習している．

1. 39 日前までのデータを集約したもの．(1)の部分．57 行．
2. x 週間前から学習データ最終日までのデータを集約したもの．(2)の部分．5 行．

"""

## Codes
train_feat = pd.DataFrame()
# @note: 出どころが不明．
start_date = '2017-03-12'
for i in range(58):
    # (1)
    # @note: range(58) の 58 の出どころが不明．
    # 直近のデータのうち，年末年始を除いたものか？
    # i = 1 のとき make_feats(2017-03-05, 39)
    # i = 57 のとき make_feats(2017-01-14, 39)
    train_feat_sub = make_feats(
        date_add_days(start_date, i*(-7)),
        39
    )
    train_feat = pd.concat([train_feat,train_feat_sub])
for i in range(1,6):
    # (2)
    # @note:
    # i = 1 のとき make_feats('2017-03-19', 35)
    # 2017-03-19 の 35 日後は 2017-04-23
    # i = 2 のとき make_feats('2017-03-26', 28)
    # 2017-03-26 の 28 日後は 2017-04-23
    train_feat_sub = make_feats(date_add_days(start_date,i*(7)),42-(i*7))
    train_feat = pd.concat([train_feat,train_feat_sub])
# 2017-03-12 + 42 days = 2017-04-23.
# make_feats(2017-04-23, 39) を実行している．
# i.e. 2017-04-23 - 2017-05-31.
test_feat = make_feats(date_add_days(start_date, 42),39)
# ...
lgb_train = lgb.Dataset(train_feat[predictors], train_feat['visitors'])
lgb_test = lgb.Dataset(test_feat[predictors], test_feat['visitors'])
# ...
gbm = lgb.train(params,lgb_train,2300)
pred = gbm.predict(test_feat[predictors])

def date_add_days(start_date, days):
    end_date = parse(start_date[:10]) + timedelta(days=days)
    end_date = end_date.strftime('%Y-%m-%d')
    return end_date

def make_feats(end_date,n_day):
    # ...
    label = get_label(end_date,n_day)
    # ...
    result = [label]
    result.append(get_store_visitor_feat(label, key, 1000))        # store features
    result.append(get_store_visitor_feat(label, key, 56))          # store features
    result.append(get_store_visitor_feat(label, key, 28))          # store features
    result.append(get_store_visitor_feat(label, key, 14))          # store features
    result.append(get_store_exp_visitor_feat(label, key, 1000))    # store exp features
    result.append(get_store_week_feat(label, key, 1000))           # store dow features
    result.append(get_store_week_feat(label, key, 56))             # store dow features
    result.append(get_store_week_feat(label, key, 28))             # store dow features
    result.append(get_store_week_feat(label, key, 14))             # store dow features
    result.append(get_store_week_diff_feat(label, key, 58))       # store dow diff features
    result.append(get_store_week_diff_feat(label, key, 1000))      # store dow diff features
    result.append(get_store_all_week_feat(label, key, 1000))       # store all week feat
    result.append(get_store_week_exp_feat(label, key, 1000))       # store dow exp feat
    result.append(get_store_holiday_feat(label, key, 1000))        # store holiday feat

    result.append(get_genre_visitor_feat(label, key, 1000))         # genre feature
    result.append(get_genre_visitor_feat(label, key, 56))           # genre feature
    result.append(get_genre_visitor_feat(label, key, 28))           # genre feature
    result.append(get_genre_exp_visitor_feat(label, key, 1000))     # genre feature
    result.append(get_genre_week_feat(label, key, 1000))            # genre dow feature
    result.append(get_genre_week_feat(label, key, 56))              # genre dow feature
    result.append(get_genre_week_feat(label, key, 28))              # genre dow feature
    result.append(get_genre_week_exp_feat(label, key, 1000))        # genre dow exp feature

    result.append(get_reserve_feat(label,key))                      # air_reserve
    result.append(get_first_last_time(label,key,1000))             # first time and last time
    # ...
    return result


def get_label(end_date,n_day):
    label_end_date = date_add_days(end_date, n_day)
    label = data[
        (data['visit_date'] < label_end_date) & (data['visit_date'] >= end_date)
    ].copy()
    label['end_date'] = end_date
    label['diff_of_day'] = label['visit_date'].apply(
        lambda x: diff_of_days(x,end_date)
    )
    label['month'] = label['visit_date'].str[5:7].astype(int)
    label['year'] = label['visit_date'].str[:4].astype(int)
    for i in [3,2,1,-1]:
        date_info_temp = date_info.copy()
        date_info_temp['visit_date'] = date_info_temp['visit_date']\
            .apply(lambda x: date_add_days(x,i))
        date_info_temp.rename(columns={'holiday_flg':'ahead_holiday_{}'.format(i),'holiday_flg2':'ahead_holiday2_{}'.format(i)},inplace=True)
        label = label.merge(date_info_temp, on=['visit_date'],how='left')
    label = label.reset_index(drop=True)
    return label

def get_store_visitor_feat(label, key, n_day):
    start_date = date_add_days(key[0],-n_day)
    data_temp = data[(data.visit_date < key[0]) & (data.visit_date > start_date)].copy()
    result = data_temp.groupby(['store_id'], as_index=False)['visitors']\
        .agg({
            'store_min{}'.format(n_day): 'min',
            'store_mean{}'.format(n_day): 'mean',
            'store_median{}'.format(n_day): 'median',
            'store_max{}'.format(n_day): 'max',
            'store_count{}'.format(n_day): 'count',
            'store_std{}'.format(n_day): 'std',
            'store_skew{}'.format(n_day): 'skew'
        })
    result = left_merge(label, result, on=['store_id']).fillna(0)
    return result

def diff_of_days(day1, day2):
    days = (parse(day1[:10]) - parse(day2[:10])).days
    return days
