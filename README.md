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

```powershell
PS> ./init.ps1  # Starts virtual environment and sets config variables
PS> npm install # installs any new NPM dependencies
PS> flask run   # Starts configured development server
```

### Deployment

There are 2 git remotes, and 2 corresponding heroku apps. Push to `stage` for staging and `pro` for production.
The app is hosted on a [gunicorn](https://gunicorn.org/) server.

```powershell
PS> heroku run python fs.py --app fs-mir-stage
PS> heroku run python fs.py --app fs-mir-pro
```

## Code Structure

### Logic

The mathematical logic is contained in `elo.py`.

### Api Request Handling

`FBApi.py` serves as the dedicated api request handler.

### Construction of Data Objects

The data objects are stored as JSON files in the `json` directory. They are written by `run_calcs.py`.

### Excel Integration

All of the file i/o and logic for creating the Excel sheets is stored in the `xl_py` folder.

## Testing

### Running Tests

Testing is implemented by [pytest](https://github.com/pytest-dev/pytest) ([Docs](https://docs.pytest.org)).
Each test module corresponds with a module in the repo. Pytest will discover the tests and is configured to run
them simply by calling `pytest`. Code coverage statistics are output as HTML in th `docs/coverage` directory.

## Documentation

Placeholder text.

## API Requests

Complete [API documentation](https://www.football-data.org/documentation/api). API requires signing up for an account
to recieve an API key.

## League Coverage

| id   | code | name                  | area        |
|------|------|-----------------------|-------------|
| 2024 | ASL  | Superliga Argentina   | Argentina   |
| 2013 | BSA  | Série A               | Brazil      |
| 2002 | BL   | Bundesliga            | Germany     |
| 2015 | FL1  | Ligue 1               | France      |
| 2021 | PL   | Premier League        | England     |
| 2016 | ELC  | Championship          | England     |
| 2014 | PD   | La Liga               | Spain       |
| 2019 | SA   | Serie A               | Italy       |
| 2017 | PPL  | Primeira Liga         | Portugal    |
| 2003 | DED  | Eredivisie            | Netherlands |
| 2145 | MLS  | MLS                   | USA         |
| 2001 | CL   | UEFA Champions League | Europe      |
| 2146 | EL   | UEFA Europa League    | Europe      |


## TODO

- [ ] Refactor xl_py.main() without so many loops. Just write the lists all at once.
- [ ] Expand the data constructions towards pandas and away from JSON.