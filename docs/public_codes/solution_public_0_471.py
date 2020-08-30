"""solution(public:0.471,private:0.505 ).

[solution(public:0.471,private:0.505 ) | Kaggle](https://www.kaggle.com/plantsgo/solution-public-0-471-private-0-505)

下記コードは一部抜粋，順序を入れ替えたもの．

Summary

予測対象は 2017-04-23 - 2017-05-31 の 39 日．
"""

## Codes

def date_gap(x,y):
    a,b,c=x.split("-")
    return (date(int(a),int(b),int(c))-y).days

def feat_sum(df, df_feature, fe,value,name=""):
    df_count = pd.DataFrame(df_feature.groupby(fe)[value].sum()).reset_index()
    if not name:
        df_count.columns = fe + [value+"_%s_sum" % ("_".join(fe))]
    else:
        df_count.columns = fe + [name]
    df = df.merge(df_count, on=fe, how="left").fillna(0)
    return df

def create_features(df_label,df_train,df_air_reserve,df_hpg_reserve):
    df_train=date_handle(df_train)
    df_label=date_handle(df_label)


    #预定信息
    # Feiyang: 4. 把这两段的 mean 改成了 kernelMedian
    df_label=feat_sum(
        df_label,
        df_air_reserve,
        ["air_store_id","visit_date"],
        "reserve_datetime_diff",
        "air_reserve_datetime_diff_sum"
    )
    df_label=feat_kernelMedian(df_label,df_air_reserve,["air_store_id","visit_date"],"reserve_datetime_diff",PrEp,"air_reserve_datetime_diff_mean")
    df_label=feat_sum(df_label,df_air_reserve,["air_store_id","visit_date"],"reserve_visitors","air_reserve_visitors_sum")
    df_label=feat_kernelMedian(df_label,df_air_reserve,["air_store_id","visit_date"],"reserve_visitors",PrEp,"air_reserve_visitors_mean")
    df_label=feat_sum(df_label,df_air_reserve,["visit_date"],"reserve_visitors","air_date_reserve_visitors_sum")
    df_label=feat_kernelMedian(df_label,df_air_reserve,["visit_date"],"reserve_visitors",PrEp,"air_date_reserve_visitors_mean")

    df_label=feat_sum(df_label,df_hpg_reserve,["air_store_id","visit_date"],"reserve_datetime_diff","hpg_reserve_datetime_diff_sum")
    df_label=feat_kernelMedian(df_label,df_hpg_reserve,["air_store_id","visit_date"],"reserve_datetime_diff",PrEp,"hpg_reserve_datetime_diff_mean")
    df_label=feat_sum(df_label,df_hpg_reserve,["air_store_id","visit_date"],"reserve_visitors","hpg_reserve_visitors_sum")
    df_label=feat_kernelMedian(df_label,df_hpg_reserve,["air_store_id","visit_date"],"reserve_visitors",PrEp,"hpg_reserve_visitors_mean")
    df_label=feat_sum(df_label,df_hpg_reserve,["visit_date"],"reserve_visitors","hpg_date_reserve_visitors_sum")
    df_label=feat_kernelMedian(df_label,df_hpg_reserve,["visit_date"],"reserve_visitors",PrEp,"hpg_date_reserve_visitors_mean")

    # 出どころが不明．
    for i in [35,63,140]:
        df_air_reserve_select=df_air_reserve[df_air_reserve.day_gap>=-i].copy()
        df_hpg_reserve_select=df_hpg_reserve[df_hpg_reserve.day_gap>=-i].copy()

        # Feiyang: 5. 把这两段的 mean 改成了 kernelMedian
        date_air_reserve=pd.DataFrame(df_air_reserve_select.groupby(["air_store_id","visit_date"]).reserve_visitors.sum()).reset_index()
        date_air_reserve.columns=["air_store_id","visit_date","reserve_visitors_sum"]
        date_air_reserve=feat_count(date_air_reserve,df_air_reserve_select,["air_store_id","visit_date"],"reserve_visitors","reserve_visitors_count")
        date_air_reserve=feat_kernelMedian(date_air_reserve,df_air_reserve_select,["air_store_id","visit_date"],"reserve_visitors",PrEp,"reserve_visitors_mean")

        date_hpg_reserve=pd.DataFrame(df_hpg_reserve_select.groupby(["air_store_id","visit_date"]).reserve_visitors.sum()).reset_index()
        date_hpg_reserve.columns=["air_store_id","visit_date","reserve_visitors_sum"]
        date_hpg_reserve=feat_count(date_hpg_reserve,df_hpg_reserve_select,["air_store_id","visit_date"],"reserve_visitors","reserve_visitors_count")
        date_hpg_reserve=feat_kernelMedian(date_hpg_reserve,df_hpg_reserve_select,["air_store_id","visit_date"],"reserve_visitors",PrEp,"reserve_visitors_mean")

        date_air_reserve=date_handle(date_air_reserve)
        date_hpg_reserve=date_handle(date_hpg_reserve)
        date_air_reserve["holiday"] = ((date_air_reserve["weekday"]>=5) | (date_air_reserve["holiday_flg"]==1)).astype(int)
        date_hpg_reserve["holiday"] = ((date_hpg_reserve["weekday"]>=5) | (date_hpg_reserve["holiday_flg"]==1)).astype(int)
        #date_air_reserve["holiday"] = map(lambda a, b: 1 if a in [5, 6] or b == 1 else 0, date_air_reserve["weekday"], date_air_reserve["holiday_flg"])
        #date_hpg_reserve["holiday"] = map(lambda a, b: 1 if a in [5, 6] or b == 1 else 0, date_hpg_reserve["weekday"], date_hpg_reserve["holiday_flg"])

        df_label=feat_mean(df_label,date_air_reserve,["air_store_id","weekday"],"reserve_visitors_sum", "air_reserve_visitors_sum_weekday_mean_%s"%i)
        df_label=feat_mean(df_label,date_hpg_reserve,["air_store_id","weekday"],"reserve_visitors_sum", "hpg_reserve_visitors_sum_weekday_mean_%s"%i)
        df_label=feat_mean(df_label,date_air_reserve,["air_store_id","weekday"],"reserve_visitors_mean", "air_reserve_visitors_mean_weekday_mean_%s"%i)
        df_label=feat_mean(df_label,date_hpg_reserve,["air_store_id","weekday"],"reserve_visitors_mean", "hpg_reserve_visitors_mean_weekday_mean_%s"%i)
        df_label=feat_mean(df_label,date_air_reserve,["air_store_id","weekday"],"reserve_visitors_count", "air_reserve_visitors_count_weekday_mean_%s"%i)
        df_label=feat_mean(df_label,date_hpg_reserve,["air_store_id","weekday"],"reserve_visitors_count", "hpg_reserve_visitors_count_weekday_mean_%s"%i)

        df_label=feat_mean(df_label,date_air_reserve,["air_store_id","holiday"],"reserve_visitors_sum", "air_reserve_visitors_sum_holiday_mean_%s"%i)
        df_label=feat_mean(df_label,date_hpg_reserve,["air_store_id","holiday"],"reserve_visitors_sum", "hpg_reserve_visitors_sum_holiday_mean_%s"%i)
        df_label=feat_mean(df_label,date_air_reserve,["air_store_id","holiday"],"reserve_visitors_mean", "air_reserve_visitors_mean_holiday_mean_%s"%i)
        df_label=feat_mean(df_label,date_hpg_reserve,["air_store_id","holiday"],"reserve_visitors_mean", "hpg_reserve_visitors_mean_holiday_mean_%s"%i)
        df_label=feat_mean(df_label,date_air_reserve,["air_store_id","holiday"],"reserve_visitors_count", "air_reserve_visitors_count_holiday_mean_%s"%i)
        df_label=feat_mean(df_label,date_hpg_reserve,["air_store_id","holiday"],"reserve_visitors_count", "hpg_reserve_visitors_count_holiday_mean_%s"%i)


    #月初月中月末
    # Feiyang: 6. 把这两段的 mean 改成了 kernelMedian
    df_label = feat_kernelMedian(df_label, df_train, ["air_store_id","day","weekday"], "visitors",PrEp, "air_day_mean")
    df_label = feat_kernelMedian(df_label, df_train, ["air_store_id","day","holiday"], "visitors",PrEp, "air_holiday_mean")
    for i in [21,35,63,140,280,350,420]:
        df_select=df_train[df_train.day_gap>=-i].copy()

        # Feiyang: 7. 给最重要的 visitors 这一列加上了新的特征: kernelMedian, median
        df_label=feat_median(df_label, df_select, ["air_store_id"], "visitors", "air_median_%s"%i)
        df_label=feat_mean(df_label,df_select,["air_store_id"],"visitors", "air_mean_%s"%i)
        df_label=feat_kernelMedian(df_label,df_select,["air_store_id"],"visitors",PrEp,"air_kermed_%s"%i)
        df_label=feat_max(df_label,df_select,["air_store_id"],"visitors","air_max_%s"%i)
        df_label=feat_min(df_label,df_select,["air_store_id"],"visitors","air_min_%s"%i)
        df_label=feat_std(df_label,df_select,["air_store_id"],"visitors","air_std_%s"%i)
        df_label=feat_count(df_label,df_select,["air_store_id"],"visitors","air_count_%s"%i)

        # Feiyang: 8. 把这几段的 mean 改成了 kernelMedian
        #df_label=feat_mean(df_label,df_select,["air_store_id","weekday"],"visitors", "air_week_mean_%s"%i)
        df_label=feat_kernelMedian(df_label,df_select,["air_store_id","weekday"],"visitors",PrEp,"air_week_kermed_%s"%i)
        df_label=feat_max(df_label,df_select,["air_store_id","weekday"],"visitors","air_week_max_%s"%i)
        df_label=feat_min(df_label,df_select,["air_store_id","weekday"],"visitors","air_week_min_%s"%i)
        df_label=feat_std(df_label,df_select,["air_store_id","weekday"],"visitors","air_week_std_%s"%i)
        df_label=feat_count(df_label,df_select,["air_store_id","weekday"],"visitors","air_week_count_%s"%i)

        # df_label=feat_mean(df_label,df_select,["air_store_id","holiday"],"visitors", "air_holiday_mean_%s"%i)
        df_label=feat_kernelMedian(df_label,df_select,["air_store_id","holiday"],"visitors",PrEp,"air_holiday_kermed_%s"%i)
        df_label=feat_max(df_label,df_select,["air_store_id","holiday"],"visitors","air_holiday_max_%s"%i)
        df_label=feat_min(df_label,df_select,["air_store_id","holiday"],"visitors","air_holiday_min_%s"%i)
        df_label=feat_count(df_label,df_select,["air_store_id","holiday"],"visitors","air_holiday_count_%s"%i)

        #df_label=feat_mean(df_label,df_select,["air_genre_name","holiday"],"visitors", "air_genre_name_holiday_mean_%s"%i)
        df_label=feat_kernelMedian(df_label,df_select,["air_genre_name","holiday"],"visitors",PrEp,"air_genre_name_holiday_kermed_%s"%i)
        df_label=feat_max(df_label,df_select,["air_genre_name","holiday"],"visitors","air_genre_name_holiday_max_%s"%i)
        df_label=feat_min(df_label,df_select,["air_genre_name","holiday"],"visitors","air_genre_name_holiday_min_%s"%i)
        df_label=feat_count(df_label,df_select,["air_genre_name","holiday"],"visitors","air_genre_name_holiday_count_%s"%i)

        #df_label=feat_mean(df_label,df_select,["air_genre_name","weekday"],"visitors", "air_genre_name_weekday_mean_%s"%i)
        df_label=feat_kernelMedian(df_label,df_select,["air_genre_name","weekday"],"visitors",PrEp,"air_genre_name_weekday_kermed_%s"%i)
        df_label=feat_max(df_label,df_select,["air_genre_name","weekday"],"visitors","air_genre_name_weekday_max_%s"%i)
        df_label=feat_min(df_label,df_select,["air_genre_name","weekday"],"visitors","air_genre_name_weekday_min_%s"%i)
        df_label=feat_count(df_label,df_select,["air_genre_name","weekday"],"visitors","air_genre_name_weekday_count_%s"%i)

        #df_label=feat_mean(df_label,df_select,["air_area_name","holiday"],"visitors", "air_area_name_holiday_mean_%s"%i)
        df_label=feat_kernelMedian(df_label,df_select,["air_area_name","holiday"],"visitors",PrEp,"air_area_name_holiday_kermed_%s"%i)
        df_label=feat_max(df_label,df_select,["air_area_name","holiday"],"visitors","air_area_name_holiday_max_%s"%i)
        df_label=feat_min(df_label,df_select,["air_area_name","holiday"],"visitors","air_area_name_holiday_min_%s"%i)
        df_label=feat_count(df_label,df_select,["air_area_name","holiday"],"visitors","air_area_name_holiday_count_%s"%i)

        #df_label=feat_mean(df_label,df_select,["air_area_name","air_genre_name","holiday"],"visitors", "air_area_genre_name_holiday_mean_%s"%i)
        df_label=feat_kernelMedian(df_label,df_select,["air_area_name","air_genre_name","holiday"],"visitors",PrEp,"air_area_genre_name_holiday_kermed_%s"%i)
        df_label=feat_max(df_label,df_select,["air_area_name","air_genre_name","holiday"],"visitors","air_area_genre_name_holiday_max_%s"%i)
        df_label=feat_min(df_label,df_select,["air_area_name","air_genre_name","holiday"],"visitors","air_area_genre_name_holiday_min_%s"%i)
        df_label=feat_count(df_label,df_select,["air_area_name","air_genre_name","holiday"],"visitors","air_area_genre_name_holiday_count_%s"%i)

    return df_label

for slip in [14,28,42]:   #you can add 21 35...
    t2017 = date(2017, 4, 23)
    nday=slip
    # ...
    all_data=[]
    for i in range(nday*1,nday*(420//nday+1),nday):  #windowsize==step
        delta = timedelta(days=i)
        t_begin=t2017 - delta
        print(t_begin)
        df_train["day_gap"]=df_train["visit_date"].apply(lambda x:date_gap(x,t_begin))
        air_reserve["day_gap"]=air_reserve["reserve_date"].apply(lambda x:date_gap(x,t_begin))
        hpg_reserve["day_gap"]=hpg_reserve["reserve_date"].apply(lambda x:date_gap(x,t_begin))
        df_feature=df_train[df_train.day_gap<0].copy()
        df_air_reserve=air_reserve[air_reserve.day_gap<0].copy()
        df_hpg_reserve=hpg_reserve[hpg_reserve.day_gap<0].copy()
        df_label=df_train[(df_train.day_gap>=0)&(df_train.day_gap<nday)][["air_store_id","hpg_store_id","visit_date","day_gap","visitors"]].copy()
        # @note: create_features()
        train_data_tmp=create_features(df_label,df_feature,df_air_reserve,df_hpg_reserve)
        all_data.append(train_data_tmp)

    # @note: train() に使われるデータ
    train=pd.concat(all_data)

    t_begin=date(2017, 4, 23)
    # ...
    df_label=df_test.merge(store_id_relation,on="air_store_id",how="left")
    df_label["day_gap"]=df_label["visit_date"].apply(lambda x:date_gap(x,t_begin))
    df_train["day_gap"]=df_train["visit_date"].apply(lambda x:date_gap(x,t_begin))
    # ...
    df_label=df_label[["air_store_id","hpg_store_id","visit_date","day_gap"]].copy()
    # @note: predict() に使われるデータ
    # each args of create_features()
    # train_data_tmp = create_features(df_label,df_feature,df_air_reserve,df_hpg_reserve)
    # train,          test
    # ------------------------
    # df_label,       df_label
    # df_feature,     df_train
    # df_air_reserve, air_reserve
    # df_hpg_reserve, hpg_reserve
    test=create_features(df_label,df_train,air_reserve,hpg_reserve)
    # ...
    train_data = train.drop(["air_store_id","hpg_store_id","visit_date"], axis=1)
    test_data = test.drop(["air_store_id","hpg_store_id","visit_date"], axis=1)

    weight_df=train[["day_gap"]].copy()
    weight_df["weight"]=weight_df["day_gap"].apply(lambda x: 1 if x<=6 else 1)

    kf = KFold(train.shape[0], n_folds=folds, shuffle=True, random_state=seed)
    lgb_train, lgb_test,m=lgb(train_data,test_data)
    lgb_train, lgb_test,m=lgb(train_data,test_data)
    # ...
    def lgb(train, valid):
        xgb_train, xgb_test,cv_scores = stacking(lightgbm,train,valid,"lgb")
        return xgb_train, xgb_test,cv_scores

    def stacking(clf,train_data,test_data,clf_name,class_num=1):
        train=np.zeros((train_data.shape[0],class_num))
        test=np.zeros((test_data.shape[0],class_num))
        test_pre=np.empty((folds,test_data.shape[0],class_num))
        cv_scores=[]
        for i,(train_index,test_index) in enumerate(kf):
            tr=train_data.iloc[train_index]
            # @note 予測対象
            te=train_data.iloc[test_index]
            #分别测试分数
            te_1=te[te.day_gap<=6].copy()
            te_2=te[te.day_gap>6].copy()
            te_1_x=te_1.drop(["visitors"], axis=1)
            te_2_x=te_2.drop(["visitors"], axis=1)
            # ...
            if test_matrix:
                # ...
                model = clf.train(params, train_matrix,num_round,valid_sets=test_matrix,
                                  early_stopping_rounds=early_stopping_rounds
                                  )
                pre_1=model.predict(te_1_x,num_iteration=model.best_iteration).reshape((te_1_x.shape[0],1))
                pre_2=model.predict(te_2_x,num_iteration=model.best_iteration).reshape((te_2_x.shape[0],1))
                cv_scores.append((mean_squared_error(te_y, pre)**0.5,mean_squared_error(te_1_y, pre_1)**0.5,mean_squared_error(te_2_y, pre_2)**0.5))
        # ...
        return train.reshape(-1,class_num),test.reshape(-1,class_num),score_split


    # ...
    import lightgbm

    train_data = train.drop(["air_store_id","hpg_store_id","visit_date"], axis=1)
    test_data = test.drop(["air_store_id","hpg_store_id","visit_date"], axis=1)
    # @note: lgb() -> stacking() -> predict()
    lgb_train, lgb_test,m=lgb(train_data,test_data)
    # ...

