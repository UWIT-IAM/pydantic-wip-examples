from unittest import mock

from pydantic import ValidationError
from flask import Flask, request as flask_request
from sqlalchemy.orm import Session

from examples.flask_with_sql_orm.models import CreateUserInput, CreateUserOutput, UserSettingsBase
from werkzeug import exceptions

from examples.flask_with_sql_orm.relationships import UserORM, UserSettingsORM

app = Flask('pydantic-example')


@app.route('/')
def welcome() -> str:
    return f"""
    <html>
    <body>
        <form method="POST" action="/new">
            <input name="username" placeholder="enter username"/><br/>
            <input name="email_address" placeholder="enter email address"/><br/>
            <input type="submit"/></form>
        </form>
        <h3>By the way, pydantic can generate a JSON schema too . . .</h3>
        <p>
            Here is the JSON schema for the input model. You can use this to 
            allow front-ends to mirror back-end validations.
            You can fiddle with it 
            <a href="https://www.jsonschemavalidator.net/s/t2VS1l9Y" target="_blank">here</a>.
        </p>        
        <pre>{CreateUserInput.schema_json(by_alias=True, indent=4)}</pre>
    </body>
    </html>
    """


@app.route('/new', methods=['POST'])
def create_user() -> str:
    """
    This is the API method that creates a user. It accepts the request, and returns the
    user object. Notice that the request method does very little work itself. The model handles its
    own input validation. The `create_user_orm` function acts as our DBA layer. So, our API does only what it
    should: Accepts a request, and returns a response.

    Input: {"username": "foo"}
    Output: '{"username": "foo",
              "userId": 1234,
              "settings": {
                "emailSubscription": False,
                "privateProfile": True,
                "emailAddress": "foo@bar.com"
              }
            }'
    """
    # First, we parse and validate the user data.
    try:
        form_data = dict(flask_request.form)
        request_input = CreateUserInput.parse_obj(form_data)
    except ValidationError as e:
        print(e)
        raise exceptions.BadRequest(e.json())

    user = create_user_orm(request_input)
    return user.json(by_alias=True)


def get_sql_session() -> Session:
    """This is just here to demonstrate that somehow a SQLAlchemy session gets created.
    We don't need that overhead in this example."""
    session = mock.MagicMock(Session)  # Obviously pseudocode

    def mock_add(orm: UserORM):
        print("Pretending to creating a DB record.")
        orm.user_id = 1234

    session.add.side_effect = mock_add
    return session


def create_user_orm(request_input: CreateUserInput) -> CreateUserOutput:
    """
    This function would likely be found in a Database Access layer (DBA/DAL) somewhere.
    By using strictly declared inputs and outputs, instead of long strings of function parameters,
    we don't have to keep re-documenting the fields and arguments. Additionally,
    refactors are easier when all you need to do is add a field to your model and call it a day.

    Ideally, only the DBA interacts with the database. Your application's services pass around the pydantic model,
    and leave it to your DBA to update the database to be in sync with the desired user state.
    """
    # First, we create the dependent model that will eventually have the user foreign key assigned to it.
    # We create the ORM from a "splat" of the settings object's dict() output, which passes all fields
    # including default fields, as if we had set them explicitly in the function call.
    settings = UserSettingsORM(
        **UserSettingsBase(email_address=request_input.email_address).dict(exclude_none=True)
    )
    # Next, we create a UserORM in the same way, also providing the dependent model.
    user_orm = UserORM(username=request_input.username, settings=settings)
    session = get_sql_session()
    with session.begin_nested():
        session.add(user_orm)
        # When we commit, the user_id is generated, and automagically exported to the UserSettings table
        session.commit()
    session.refresh(user_orm)  # This might not be necessary, I can't ever remember the sqlalchemy rules.
    # And finally, we we use the ORM mode to create an output object directly from the relational model; this
    # will ensure that manipulations of the object do not result in database queries.
    return CreateUserOutput.from_orm(user_orm)


if __name__ == "__main__":
    app.run(debug=True)
