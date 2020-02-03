There are several scripts for developing Bridger:

pipen run `scriptname`

* local
    * runs the dev-server on `0.0.0.0:5000`
* start_db
    * start the postgresql server through docker compose
* psql
    * enters psql
* docks
    * start the documentation server on `0.0.0.0:8000`
* test
    * runs all the tests in the current environment
* sort_import
    * sorts all the imports in all files through isort