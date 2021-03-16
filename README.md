# pydantic-wip-examples
A repository of pydantic use case examples. 

Ok, right now, there is only one example. You can run it like so:

```
./run-example.sh -e flask_with_sql_orm
```

For more information, see the [orm proxy readme](examples/flask_with_sql_orm/README.md).

## Requirements

- A linux/mac terminal (I may be "extra", but I'm not "windows-compatibility extra.")
- A running docker daemon

### Alternate configuration

You can run these examples directly with [poetry], instead of via docker. See 
[below](#runtime).


## Adding New Examples

- Add a subdirectory under "examples"
- Include an `.example.sh` file that exports (required) 
  `DOCKER_RUN_COMMAND` and (optionally) `DOCKER_RUN_ARGS`. 
  See [an existing example](examples/flask_with_sql_orm/.example.sh)
  
If you want users to be able to live-mount and edit example code while it's running,
include `${LIVE_MOUNT}` somewhere in your `DOCKER_RUN_ARGS`.

### Poetry

#### Dependency Management

This package uses [poetry] to manage dependencies. If you want to add new 
dependencies, you must install [poetry] and use `poetry add`, e.g., `poetry add 
pydantic`. 

If you want to install these dependencies on _your_ machine, you can use `poetry 
install`.

#### Runtime

You don't have to use docker to run these examples. If you are willing to install 
[poetry], you can run anything in this package using `poetry run /path/to/python/file.py`.


#### Docker base image

The docker container is built on the shared [uwitiam/poetry] container, which comes 
ready to run poetry-backed applications. It is hosted publicly on dockerhub. Feel 
free to use it yourself! The [Dockerfile](Dockerfile) used here is mostly 
responsible for copying the repository files into the docker image, then issuing the 
`poetry install` command.

[poetry]: https://python-poetry.org
[uwitiam/poetry]: https://uwiam.page.link/poetry-docker-base
