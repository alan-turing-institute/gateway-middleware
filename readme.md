# Science Gateway Middleware

The science gateway middleware stores the current status 
of all cases and jobs. It does minimal processing, and serves
primarily as a persistent store of state (but not of data).

## Running The System

1. Ensure that you have installed [Docker](https://docs.docker.com/docker-for-mac/install/).

1. Start the Docker daemon if it is not already running.

1. If this is the first time you are running the system, 
    run the Postgres server individually in order for it
    to set itself up. You should give it a minute just to be 
    safe.
    ```shell
    docker-compose run -d postgres
    ```

1. Shutdown the Postgres server.
    ```shell
    docker-compose down
    ```

1. Bring up the full system.
    ```shell
    docker-compose up
    ```

1. If you need to add demo data to the system send a `POST`
    request to `http://localhost:5000/test`. This will return
    `null`.

1. Connect to the running server at (http://localhost:5000).

1. To bring the system down (saving the database state)
    ```shell
    docker-compose down
    ```

1. If you ever need to work with the database run:
    ```shell
    docker-compose run -d postgres
    docker ps
    ```
    This will show a `CONTAINER ID` for the container that you just 
    created. 
    Connect to this container with:
    ```shell
    docker exec -it 5a73ca796372 /bin/bash
    ```
    Once inside the shell you can connect to the database with:
    ```shell
    psql -U sg -W sg 
    ```
    with the password `sg`
    When you are finished. Quit from `psql` and the shell and run:
    ```shell
    docker-compose down
    ```

1. If you have Postgres installed on your local machine, you can 
    connect to the docker `Postgres` instance by running:
    ```shell
    docker-compose run -d -p "8082:5432" postgres
    psql -U sg -W -h localhost sg
    ```
    When you are finished run:
    ```shell
    docker-compose down
    ```

### Helpful SQL Commands

Just as a reminder here are some helpful PostgreSQL commands
that may be helpful:

* List all tables:
    ```sql
    \dt
    ```

* Get all cases. Note that because the `case` table name clashes
    with an SQL keyword, you must wrap the table name in `"`
    ```sql
    SELECT * FROM "Case";

* Delete all tables:
    ```sql
    DROP TABLE IF EXISTS "Case", Case_Field, ParameterSpec, Job, JobParameter, JobParameterTemplate, JobParameterTemplateValue CASCADE;
    ```


## Using The Middleware

The Flask app creates a server at `localhost:5000`.

It supports the following endpoints:
* `/case[?page=N&per_page=N]`: Get a listing of all the cases in the system.
    * `page` gives the page of output that you are requesting. The first page is 1 (also the default)
    * `per_page` gives the number of results per page to return
    Rather than returning and error, the pagination will return an empty list when you ask for a page
    that does not exist (i.e off the end). I am not returning any information about whether the
    next page may or may not exist. This is because I am expecting this to be used as part of an
    infinite scrolling system, where there is no explicit display to the user to ask for more 
    (or if there a button to support error situations, returning no extra data is a valid respose).
* `/cases/<id>`: Gets the full details for a single case. This retreives the entire case and
    serialises it for the user. 
* `/job/`: 
    * `GET`: See all existing jobs. Takes query arguments.
        * `page` gives the page of output that you are requesting. The first page is 1 (also the default).
        * `per_page` gives the number of results per page to return.
    * `POST`: Create a new job. Takes header arguments.
        * `case_id`: The case id for the case this job is based off.
* `/job/<id>`:
    * `GET`: Get the details of the current job
    * `PATCH`: Update details of the current job. Takes a JSON object of what to replace.
        Only replace fields that are provided. The required structure is:
        ```json
        {
            "name": "New name of the job",
            "values": [
                {
                    "name": "parameter name",
                    "value": "parameter value"
                },
                ...
            ]
        }
        ```

* Not yet implemented:
   * having the minted case know what mintstore names and versions its values came from.
   * marshmallow serialization/deserialization of the "Minted" half of the data model.
   * Job endpoints
   * Storage of script data
