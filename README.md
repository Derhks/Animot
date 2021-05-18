# Animot


## Table of Content

* [Development Environment Configuration](#development-environment-configuration)
* [Run development version with docker](#run-development-version-with-docker)  
* [Test the Application](#test-the-application)
* [Built With](#built-with)
* [Authors](#authors)


## Development Environment Configuration

- Download the files from this repository.

  ```bash
  git clone git@github.com:Derhks/Animot.git
  ```

- Create a virtual environment with Anaconda

  ```bash
  conda create -n animot python=3.8 -y
  ```

- Now, let's activate the created virtual environment

  ```bash
  conda activate animot
  ```

- With the virtual environment activated we are going to install 
  the requirements used in the project

  ```bash
  pip3 install -r requirements.txt
  ```

- We must export the following environment variable

  ```bash
  export $(cat .env | grep -v ^# | xargs)
  ```
  
### Setup PostgreSQL

Verify that you have PostgreSQL installed on your computer, run the 
following command to find out which version you have installed:

```bash
  postgres -V
  ```

If you do not see the PostgreSQL version, you must install it.

Run the setup_postgres.sql script to create the database, user and password 
to be used in the project

```bash
  cat setup_postgres.sql | sudo -u postgres psql
  ```

With the above command we enter the PostgreSQL Shell and the commands inside 
the file are executed. To verify that the database, and the user were created 
execute the following commands:

1. Database
```bash
  echo "SELECT datname FROM pg_database;" | sudo -u postgres psql | grep animot_db
  ```

2. User
```bash
  echo "SELECT * FROM pg_catalog.pg_user;" | sudo -u postgres psql | grep derhks
  ```

Let's create the table we will use in the project within our database

```bash
  python create_table.py
  ```

### Run server

- You can verify that the environment variables were added 
  correctly with the following command:

  ```bash
  env | grep "FLASK"
  ```

- The application has its unit tests, run the following command:

  ```bash
  python -m unittest
  ```

- We can view the report with the command:
  
    ```bash
  coverage report -m
  ```

- Finally, run the application server

  ```bash
  python -m flask run
  ```


## Run development version with docker

Run the following command to initialize the project using docker:

```bash
  docker-compose up --remove-orphans
  ```

You can stop the containers and also delete everything that was 
created at initialization by executing the following command, to 
do this you must open a new console:

```bash
  docker-compose down --rmi all && sudo rm -rf data/
  ```


## Test the Application

### Develop

You can test the endpoint locally with the following curl:
  ```bash
  curl --location --request GET 'http://127.0.0.1:5000/naruto'
  ```

## Built With

- [Python](https://www.python.org/) - Programming language
- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web framework
- [PostgreSQL](https://www.postgresql.org) - Database


## Authors
- **Julián Sandoval [derhks]** https://github.com/Derhks