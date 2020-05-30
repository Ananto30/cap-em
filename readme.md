## Tests

Tests are better to be run with SQLite database. Because there will be entries in DB and those should be cleared after each test is run. So **if you use any other than sqlite, make sure to delete the entries to pass tests**. To use SQLite you need to set the enviroment variable `DB_URL` -
```bash
DB_URL=sqlite:///capem-ut.db python -m pytest 
```

To run tests with coverage - 
```bash
DB_URL=sqlite:///capem-ut.db python -m pytest --cov=./app
```