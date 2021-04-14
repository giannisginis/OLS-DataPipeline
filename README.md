# <img src="documents/icons/python_postgres.png" width="350" height="150"/>&nbsp;&nbsp;&nbsp;
# OLS-DataPipeline

A Data Pipeline which loads data fetched from a remote source into a database.


## Table of Contents

* [Overview](#overview)
* [DB-Design](#db-design)
* [Python-Installation](#python-installation)
* [Execution](#execution)

Overview
---------
`ETL` is the process of fetching data from one or many systems and loading it into a target data warehouse after doing some intermediate transformations.
`ETL` stands for `Extract`, `Transform`, and `Load`. In this project, the goal is to retrieve specific data provided by a remote source and inject them into a DB.

More specifically, `OLS-DataPipeline` is a Data Pipeline which retrieves specific data provided by the [Ontology Lookup Service repository](https://www.ebi.ac.uk/ols/index)
and imports them into a Database. It supports two modes, `create` and `update`:

1. `create`: Given the short name of an ontology, this mode creates the corresponding tables in database and injects the retrieved data in DB.
2. `update`: Given the short name of an ontology, this mode injects the data in the corresponding tables from mode `create`.
This mode expects the tables to be already created and is the only incremental update that this project supports right now.

### Technology stack

* [Python 3.8.x](https://www.python.org/)
* [PostgresSQL](https://www.postgresql.org/)
* [psycopg2](https://www.psycopg.org/)
* [Docker](https://www.docker.com/)

## DB-Design

The approach followed in this project was to identify the relationship between the entities. For each entity, create a table that includes all of it’s simple attributes. Then, choose the primary key, if it’s composite, then a set of simple attributes will form together the primary key.
For each weak entity, create a table that includes all of it’s simple attributes and include a foreign key points to the primary key of the owner entity based on their relation.
With this approach in mind the final schema is the following:

* `terms`: This table includes the ontology (i.e. EFO) terms with primary key the column `id`
* `synonyms`: This table includes the synonyms per term with primary key the column `id`
* `ontology`: This table includes the most metadata for parents per term based on the response of OLS API in the parent link.
* `xref`: This table includes the MeSH term references (xref with MSH database) with foreign key reference to terms.id
  * The conclusion here was that xref references has a `one to many` relation with terms entity which can be represented by a foreign key constrain.
* `terms_synonyms`: This table represents the many to many relationship between terms and synonyms. The conclusion here was that can have common synonyms across many terms.
* `terms_ontology`: This table represents the one to many relationship between ontology(parent links) and terms. The conclusion here was that we can have the same parent across many terms.
The idea behind the extra table in this case was to have unique entries in ontology table as well.
## Python-Installation

Installation guidelines can be found in [the installation document](documents/installation.md).

## Execution

### First steps
Activate python virtual environment
```bash
$ source path2venv/bin/activate
```
Clone the project:
```bash
$ git clone https://github.com/giannisginis/OLS-DataPipeline.git
```
CD to project:
```bash
$ cd OLS-DataPipeline
```
### DataBase
Considering the postgreSQL there are two ways to use it:
* Run with Docker (recommended). In case you want to change the DB configurations check `utils/config.py`.
The full description of `docker-compose`, `pg-admin` access and `configuration` file can be found in [here](documents/docker-postgresql.md)

```Bash
$ docker-compose up -d (detach mode)
```
* The alternative is to install postgreSQL from scratch on your system (not properly tested). For this case define the correct database parameters in `utils/config.py`.
### Run Pipeline
* Run the Pipeline with `create` mode activated:
```bash
$ python main.py --Mode create --ontology EFO
```
* Run the Pipeline with `update` mode activated:
```bash
$ python main.py --Mode update --ontology AGRO
```

## Future Improvements
* For now this package handles the duplicate insertion by just skipping the duplicate entries. A possible
improvement here could be to inform the client about which of how many were the duplicate entries detected.
* Expose more database functionalities to the end user, like delete or update a specific entry of a table or
drop a whole table.
* A more clever refactoring of the Flow class. It seems a little bit repetitive right now.
* Add proper tests.
