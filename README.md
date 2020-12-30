---
page_type: meta
languages:
- python
description: "README"
urlFragment: readme
---
# Elo Football Data Calculator

## Workflow

### Local Development

```bash
    > source ./init.sh  # Starts virtual environment and sets config variables
    > npm install # installs any new NPM dependencies
    > npm run build # Builds static assets
    > npm run serve   # Starts configured development server
```

### Deployment

There are 2 git remotes, and 2 corresponding heroku apps. Push to `stage` for staging and `pro` for production.
The app is hosted on a [gunicorn](https://gunicorn.org/) server.

```bash
    > git push stage master vX.X.X
    > git push pro master vX.X.X
```

## Code Structure

### Logic

The mathematical logic is contained in `elo.py`.

### Api Request Handling

`FBApi.py` serves as the dedicated api request handler.

### Construction of Data Objects

The data objects are stored in a database as HD5 tables and read by pandas. They are written by `updater.py`.

## Documentation

**JSON Updates**: To update leagues, do the following:

1. Ensure `./app/data/updater.py` has the correct active leagues configured (under `__main__`)
2. Run the updater script from the project root (this is where the HD5 database is):

```bash
    > npm run update
```

## API Requests

Complete [API documentation](https://www.football-data.org/documentation/api). API requires signing up for an account
to recieve an API key.

## League Coverage

| id   | code | name                  | area        |
|------|------|-----------------------|-------------|
| 2002 | BL   | Bundesliga            | Germany     |
| 2015 | FL1  | Ligue 1               | France      |
| 2021 | PL   | Premier League        | England     |
| 2016 | ELC  | Championship          | England     |
| 2014 | PD   | La Liga               | Spain       |
| 2019 | SA   | Serie A               | Italy       |
| 2017 | PPL  | Primeira Liga         | Portugal    |
| 2003 | DED  | Eredivisie            | Netherlands |
