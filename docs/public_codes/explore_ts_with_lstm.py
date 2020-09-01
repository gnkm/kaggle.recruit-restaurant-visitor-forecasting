"""Explore TS with LSTM

[Explore TS with LSTM | Kaggle](https://www.kaggle.com/yekenot/explore-ts-with-lstm)

下記コードは一部抜粋．

Summary

`df.shift(positive_num)` で対象日より前のデータ，
`df.shift(negative_num)` で対象日より後のデータを学習データに含める．
=> @note: 予測の時に使えないのでは？
ここでは `n_in`, `n_out` で指定している．

```
reframed = series_to_supervised(scaled, 1, 1)
```

であるから，`n_in`, `n_out` 両方とも 1.
@note: もっと大きな値にしなくてよいのか？
"""

## Codes
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    """
    Frame a time series as a supervised learning dataset.
    Arguments:
        data: Sequence of observations as a list or NumPy array.
        n_in: Number of lag observations as input (X).
        n_out: Number of observations as output (y).
        dropnan: Boolean whether or not to drop rows with NaN values.
    Returns:
        Pandas DataFrame of series framed for supervised learning.
    """
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # Input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # Forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # Put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # Drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


# Normalize features
train['visitors'] = target_train
values = train.values
values = values.astype('float32')

scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(values)

# Frame as supervised learning
reframed = series_to_supervised(scaled, 1, 1)
