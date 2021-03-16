export DOCKER_RUN_ENV_ARGS="-e FLASK_ENV=development -e FLASK_APP=examples/flask_with_sql_orm/app.py"
export DOCKER_RUN_ARGS="${DOCKER_RUN_ENV_ARGS} ${LIVE_MOUNT} -p 127.0.0.1:5000:5000"
export DOCKER_RUN_COMMAND="poetry run python -m flask run --host=0.0.0.0"
