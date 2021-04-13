# Run PostgreSQL Using Docker

For this part, Docker is required. The stack is a Docker compose file and macOS.

#### Break down of the individual ingredients of the docker-compose.yml file:
* The first line defines the version of the Compose file, which is 3.8. There are other file formats — 1, 2, 2.x, and 3.x.
* the services hash contains the services for an application.
  * This application has two services called `db` and `pgadmin` (optional).
    * Inside the db service, we have the following tags:
      - `container_name`: changes the default container name to `pg_container`.
      - `image`: defines the Docker image for the db service (pre-built official image of PostgreSQL)
      - `restart`: always - it always automatically restarts the container by saving time. It restarts the container when either the Docker daemon restarts or the container itself is manually restarted.
      - `environment`: defines a set of environment variables related to DB connection.
      - `ports`: defines both `host` and container `ports`. It maps port 5432 on the host to port 5432 on the container.
      - `volumes`: is used to mount a folder from the host machine to the container. It is used to store the database data,
      the first part is the name of the volume, and the second part is the path in the container where the database data is stored.
    * Inside the pgadmin service, we have the following tags:
        - `ports` 5050:80: This parameter tells docker to map the port `80` in the container to port `5050` in your computer (Docker host)
        - `environment`:
          - `PGADMIN_DEFAULT_EMAIL`: Environment variable for default user’s email, you will use this to log in the portal afterwards
          - `PGADMIN_DEFAULT_PASSWORD`: Environment variable for default user’s password

#### Accessing the PostgreSQL from the pgAdmin tool
These containers are running on the default one, and if you try to access the database or the web portal
through their ports, connecting via `localhost` or `127.0.0.1` would work just fine; but in order to connect to pgadming
the IP address of the PostgreSQL container on the host, should be defined by the following command:

```bash
$ docker inspect pg_container -f "{{json .NetworkSettings.Networks }}"
```

`docker inspect` return low-level information of Docker objects, in this case, the `pg_container`
instance’s IP Address. The -f parameter is to format the output as a JSON given a Go template. You can use IP Address to
create a server in pgadmin.

#### Useful Docker Commands

* `docker ps`: check if the container is running or not
* `docker image`: check if the image is running or not
* `docker rm pg_container`: delete the container
* `docker-compose up`: create the container
* `docker exec -it pg_container bash`: use psql
* `docker volume rm postgresql-snippets_pg_data`: delete the backup volume
* `docker-compose down --volumes`: delete the backup volume

