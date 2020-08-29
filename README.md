# Recruit Restaurant Visitor Forecasting

## Problem Page

[Recruit Restaurant Visitor Forecasting | Kaggle](https://www.kaggle.com/c/recruit-restaurant-visitor-forecasting)

## Usage

### Pull docker image

```
docker pull gcr.io/kaggle-images/python
```

### Run Jupyter

```
./docker-run.sh jp
```

### Run Python

#### Convert CSV to Feather

```
./docker-run.sh py scripts/convet_to_feather.py
```

#### Main Script

```
./docker-run.sh py run.py
```

## For Development with VSCode

- Install `Remote - Container` package
- Start jupyter container
- Input "Remote-Containers: Attach to running container" to command palette
- Select jupyter container
- Select python interpreter: Python 3.7.6 64-bit ('base': conda)
