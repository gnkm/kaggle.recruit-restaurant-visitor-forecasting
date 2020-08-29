# File Descriptions

## 特徴量

学習時に使えて予測時に使えない特徴量

- air_reserve
  - visit_datetime - the time of the reservation
  - reserve_datetime - the time the reservation was made
  - reserve_visitors - the number of visitors for that reservation
- hpg_reserve
  - visit_datetime - the time of the reservation
  - reserve_datetime - the time the reservation was made
  - reserve_visitors - the number of visitors for that reservation

予測時に使える特徴量

- visit_date
- air_store_info
  - air_genre_name
  - air_area_name
  - latitude
  - longitude
- hpg_store_info
  - hpg_store_id
  - hpg_genre_name
  - hpg_area_name
  - latitude
  - longitude
- date_info
  - calendar_date
  - day_of_week
  - holiday_flg

学習時に使える特徴量

- air_reserve
  - visit_datetime - the time of the reservation
  - reserve_datetime - the time the reservation was made
  - reserve_visitors - the number of visitors for that reservation
- hpg_reserve
  - visit_datetime - the time of the reservation
  - reserve_datetime - the time the reservation was made
  - reserve_visitors - the number of visitors for that reservation
- air_store_info
  - air_genre_name
  - air_area_name
  - latitude
  - longitude
- hpg_store_info
  - hpg_genre_name
  - hpg_area_name
  - latitude
  - longitude
- air_visit_data
  - visit_date
  - visitors
- date_info
  - calendar_date
  - day_of_week
  - holiday_flg

## Referance

[kaggle page](https://www.kaggle.com/c/recruit-restaurant-visitor-forecasting/data)

## Descriptions

In this competition, you are provided a time-series forecasting problem centered around restaurant visitors. The data comes from two separate sites:

- Hot Pepper Gourmet (hpg): similar to Yelp, here users can search restaurants and also make a reservation online
- AirREGI / Restaurant Board (air): similar to Square, a reservation control and cash register system

You must use the reservations, visits, and other information from these sites to forecast future restaurant visitor totals on a given date. The training data covers the dates from 2016 until April 2017. The test set covers the last week of April and May of 2017. The test set is split based on time (the public fold coming first, the private fold following the public) and covers a chosen subset of the air restaurants. Note that the test set intentionally spans a holiday week in Japan called the "Golden Week."

There are days in the test set where the restaurant were closed and had no visitors. These are ignored in scoring. The training set omits days where the restaurants were closed.

This is a relational dataset from two systems. Each file is prefaced with the source (either air_ or hpg_) to indicate its origin. Each restaurant has a unique air_store_id and hpg_store_id. Note that not all restaurants are covered by both systems, and that you have been provided data beyond the restaurants for which you must forecast. Latitudes and Longitudes are not exact to discourage de-identification of restaurants.

### air_reserve.csv

This file contains reservations made in the air system. Note that the reserve_datetime indicates the time when the reservation was created, whereas the visit_datetime is the time in the future where the visit will occur.

- air_store_id - the restaurant's id in the air system
- visit_datetime - the time of the reservation
- reserve_datetime - the time the reservation was made
- reserve_visitors - the number of visitors for that reservation

###  hpg_reserve.csv

This file contains reservations made in the hpg system.

- hpg_store_id - the restaurant's id in the hpg system
- visit_datetime - the time of the reservation
- reserve_datetime - the time the reservation was made
- reserve_visitors - the number of visitors for that reservation

### air_store_info.csv

This file contains information about select air restaurants. Column names and contents are self-explanatory.

- air_store_id
- air_genre_name
- air_area_name
- latitude
- longitude

Note: latitude and longitude are the latitude and longitude of the area to which the store belongs

### hpg_store_info.csv

This file contains information about select hpg restaurants. Column names and contents are self-explanatory.

- hpg_store_id
- hpg_genre_name
- hpg_area_name
- latitude
- longitude

Note: latitude and longitude are the latitude and longitude of the area to which the store belongs

### store_id_relation.csv

This file allows you to join select restaurants that have both the air and hpg system.

- hpg_store_id
- air_store_id

### air_visit_data.csv

This file contains historical visit data for the air restaurants.

- air_store_id
- visit_date - the date
- visitors - the number of visitors to the restaurant on the date

```
air_store_id,visit_date,visitors
air_ba937bf13d40fb24,2016-01-13,25
air_ba937bf13d40fb24,2016-01-14,32
air_ba937bf13d40fb24,2016-01-15,29
air_ba937bf13d40fb24,2016-01-16,22
```

### sample_submission.csv

This file shows a submission in the correct format, including the days for which you must forecast.

- id - the id is formed by concatenating the air_store_id and visit_date with an underscore
- visitors- the number of visitors forecasted for the store and date combination

```
cat data/input/sample_submission.csv | head -5

id,visitors
air_00a91d42b08b08d9_2017-04-23,0
air_00a91d42b08b08d9_2017-04-24,0
air_00a91d42b08b08d9_2017-04-25,0
air_00a91d42b08b08d9_2017-04-26,0
```

```
cat data/input/sample_submission.csv | tail -5

air_fff68b929994bfbd_2017-05-27,0
air_fff68b929994bfbd_2017-05-28,0
air_fff68b929994bfbd_2017-05-29,0
air_fff68b929994bfbd_2017-05-30,0
air_fff68b929994bfbd_2017-05-31,0
```

### date_info.csv

This file gives basic information about the calendar dates in the dataset.

- calendar_date
- day_of_week
- holiday_flg - is the day a holiday in Japan

```
cat data/input/date_info.csv | head -5

calendar_date,day_of_week,holiday_flg
2016-01-01,Friday,1
2016-01-02,Saturday,1
2016-01-03,Sunday,1
2016-01-04,Monday,0
```

```
cat data/input/date_info.csv | tail -5

2017-05-27,Saturday,0
2017-05-28,Sunday,0
2017-05-29,Monday,0
2017-05-30,Tuesday,0
2017-05-31,Wednesday,0
```
