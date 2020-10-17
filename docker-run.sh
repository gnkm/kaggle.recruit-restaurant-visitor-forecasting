#! /usr/bin/env bash

# print the usage and exit
print_usage_and_exit () {
	cat <<____USAGE 1>&2
Usage   : ${0##*/} <var1> <var2> ...
____USAGE
	exit 1
}

# main script starts here

if [ $1 = 'py' ]; then
    docker run \
        -v $PWD:/tmp/working \
        -w=/tmp/working \
        --rm \
        -it \
        --name kaggle-python \
        gnkm/kaggle:001 \
        python ${@:2}
elif [ $1 = 'jp' ]; then
    docker run \
        -v $PWD:/tmp/working \
        -w=/tmp/working \
        -p 8080:8080 \
        --rm \
        -it \
        --name kaggle-jupyter \
        gnkm/kaggle:001 \
        jupyter lab \
            --no-browser \
            --ip=0.0.0.0 \
            --allow-root \
            --notebook-dir=/tmp/working
elif [ $1 = 'ui' ]; then
    docker run \
        -v $PWD:/tmp/working \
        -w=/tmp/working \
        -p 5000:5000 \
        --rm \
        -it \
        --name kaggle-mlflow-ui \
        gnkm/kaggle:001 \
        mlflow ui \
            --backend-store-uri /tmp/working/mlflow/mlruns \
            --host 0.0.0.0
elif [ $1 = 'flake' ]; then
    docker run \
        -v $PWD:/tmp/working \
        -w=/tmp/working \
        --rm \
        -it \
        --name kaggle-python \
        gnkm/kaggle:001 \
        flake8 ${@:2}
else
    docker run \
        -v $PWD:/tmp/working \
        -w=/tmp/working \
        --rm \
        -it \
        --name kaggle-python \
        gnkm/kaggle:001 \
        ${@:2}
fi
