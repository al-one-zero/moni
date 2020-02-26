# moni

Helps humans keep track of their spendings.

## install|run
1. clone the repo
2. make a virtualenv to run the webapp
```bash
virtualenv -p python3 moni-env
```
3. install the dependencies
```bash
pip install -r requirements.txt
```
4. declare app name
```bash
export FLASK_APP=moni
```
5. init the database
```bash
flask init-db
```
6. run the app
```bash
flask run
```
