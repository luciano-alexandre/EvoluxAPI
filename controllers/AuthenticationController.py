from flask import Blueprint, request, abort, session, Response
from json import dumps

app = Blueprint("authentication", __name__)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Checks if the credentials informed are valid, if so,
        it creates a session to allow the requester to have access to other features.

       Returns:
           Login confirmation.

       Raises:
           Abort: If the user is not authenticated.
       """

    if request.args['username'] == 'admin' and request.args['pass'] == 'admin':
        session['authenticated'] = 'yes'

        return Response(response=dumps('success'), status=200, content_type="application/json")

    else:
       abort(401)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    """Logs out the user.

        Returns:
            Logout confirmation.
    """

    session.pop('authenticated', None)
    return Response(response=dumps('success'), status=200, content_type="application/json")
