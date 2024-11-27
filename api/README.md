# simple fastapi app

## Install
python3 -m venv venv (first time only)
source venv/bin/activate
pip install -r ./requirements.txt

## Issues with pyscog2
If you cannot install the requirements because of pscog TEMPORARILY change
psycopg2==2.9.9
to
psycopg2-binary==2.9.9
Install the deps and revert the changes in requirements

## Develop locally
> source venv/bin/activate
> uvicorn kipeez.main:app --reload

## Run local postgres
docker-compose -f docker-compose-db.yml up postgres


