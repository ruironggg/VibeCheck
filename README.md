# VibeCheck

## Updating local conda environment.yml

1. `conda env export --no-build -f environment.yml`, this way environment.yml works for any Operating System

## Updating requirements.txt
1. `pip list --format=freeze > requirements.txt`

## Create venv using pip
````
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
````


## Create conda enviroment
`conda env create -f environment.yml`


## How to run
run using `flask run`, it runs on port 5000

