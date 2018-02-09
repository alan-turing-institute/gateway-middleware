# Science Gateway Middleware

The science gateway middleware stores the current status 
of all cases and jobs. It does minimal processing, and serves
primarily as a persistent store of state (but not of data).

## Running The System

1. Ensure that you have installed [Docker](https://docs.docker.com/docker-for-mac/install/).

1. Start the Docker daemon if it is not already running.

1. If this is the first time you are running the system, 
    run the Postgres server individually in order for it
    to set itself up.
    ```shell
    docker-compose run postgres
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

1. If you ever need to work with the database run (assuming you have already
    brought the system down):
    ```shell
    docker-compose run -d postgres
    docker ps
    ```
    This will show a `CONTAINER ID` for the container that you just 
    created. 
    Connect to this container with:
    ```shell
    docker exec -it <container id> /bin/bash
    ```
    Once inside the shell you can connect to the database with:
    ```shell
    psql -U sg -W sg 
    ```
    with the password `sg`
    When you are finished. Quit from both `psql` and the shell and run:
    ```shell
    docker-compose down
    ```

1. If you have Postgres installed on your local machine, you can 
    connect to the docker `Postgres` instance directly by running:
    ```shell
    docker-compose run -d -p "8082:5432" postgres
    psql -U sg -W -p 8082 -h localhost sg
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

The following is a list of endpoints and their functionality.

### `/case`

This endpoint is responsible for managing the list of cases.

#### GET 

A `GET` on this end point allows for paginated listing of all the cases in the system.

##### Arguments
It supports the following query args:

* `page` (optional, default=1) gives the page of output that you are requesting.
    The first page is 1.
    If you ask for a page that does not exist (i.e off the end) you will get an empty list.
* `per_page` (optional, default=10) gives the number of results per page to return.
    
No information about whether the next page exists is returned. 
This is because I am expecting this to be used as part of an
infinite scrolling system, where there is no explicit display to the user to ask for more 
(or if there a button to support error situations, returning no extra data is a valid response).

##### Return

Returns a list of case metadata for the selected cases. (May be empty).
The format is:

```json
[
    {
        "name": "Case name",
        "id": "Case id",
        "links": {
            "self": "Link to more details about this case"
        }
    },
    ...
]
```

### `/cases/<id>`

This endpoint is responsible for managing the details of a specific case. 

#### GET 
 Gets the full details for a single case. This retrieves the entire case and serialises it for the user. 

##### Arguments

No arguments are accepted.

##### Return

Returns the full details of a specific case with the following structure:

```json
{
    "name": "Case Name",
    "id": "Case Id",
    "fields": [
        {
            "name": "Case Field Name",
            "specs": [],
            "child_fields": [
                {
                    "name": "Case Field Name",
                    "specs": [
                        {
                            "name": "Parameter name",
                            "value": "Parameter Value",
                            "id": "Parameter id"
                        },
                        ...
                    ],
                    "child_fields": []
                },
                ...
            ]
        }
    ]
}
```

### `/job/`

This endpoint manages the list of all jobs. 

#### `GET`

Paginate through a list of all existing jobs.

##### Arguments
It supports the following query args:

* `page` (optional, default=1) gives the page of output that you are requesting.
    The first page is 1.
    If you ask for a page that does not exist (i.e off the end) you will get an empty list.
* `per_page` (optional, default=10) gives the number of results per page to return.
    
No information about whether the next page exists is returned. 
This is because I am expecting this to be used as part of an
infinite scrolling system, where there is no explicit display to the user to ask for more 
(or if there a button to support error situations, returning no extra data is a valid response).

##### Return

Returns a list of jobs with the following format:

```json
[
    {
        "name": "Job name",
        "user": "Job creation user",
        "id": "Job id",
        "links": {
            "self": "Link to full job details",
            "case": "Link to full details of generating case"
        },
    },
    ...
]
```

#### `POST`

Create a new job 

##### Arguments 

Takes the following JSON structure in the body:

```json
{
    "user": "Creating user",
    "name": "Job name",
    "case_id": "Parent case"
}
```

##### Return 

If not enough fields are provided the following structure will be returned:

```json
{ 
    "messages": { 
        "author": [ "Missing data for required field." ],
        "name": [ "Missing data for required field." ],
        "case_id": [ "Missing data for required field." ]
    }
}
```

If the job name and details are not accepted
(i.e. the pair of job name and author already exists) 
the following will be returned:

```json
{ 
    "message": "Sorry, these parameters have already been used. You have requested this URI [/job] but did you mean /job or /job/ ?"
}
```

If the job is successfully created, the following will be returned:

```json
{ 
    "job_id": new_job_id 
}
```

### `/job/<id>`

This endpoint is responsible for dealing with the details of a specific
job. 

#### `GET`

Get the details of the current job

##### Arguments

This end point accepts no arguments

##### Return

```json
{
    "user": "username",
    "id": job_id,
    "name": "Job_name",
    "values": [
        {
            "value": "parameter value",
            "parent_template": "source template or null",
            "id": value_id,
            "name": "parameter name",
        },
        ...
    ],
    "parent_case": { case object as from /case/id }
}
```

####`PATCH`

Update details of the current job. Note that the author and source case of a job
can not be changed after creation.

##### Arguments

Takes a JSON object of what to replace. 
Fields that are not included will not be changed.

The largest possible structure is to replace is:
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

Note that the `values` list is replaced wholesale. So if the
client sends back a shorter list, the removed values will be
deleted. 

##### Return 

If the value is successfully changed the following structure is returned. 

```json
{ 
    "status": "success", 
    "changed": [ "name", "values" ]
}
```

Note that the `changed` field is a list of which fields where successfully changed. 

### `/test`

This endpoint is used purely for testing the system

#### `POST`

This populates the database with some fake data.

##### Arguments

No arguments are supported

##### Return

Returns `null`.
