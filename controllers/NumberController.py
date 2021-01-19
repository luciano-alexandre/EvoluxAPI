from flask import Blueprint, request, abort, session, Response, jsonify
from json import dumps
from models.NumberModel import db, Contacts
from sqlalchemy import exc

app = Blueprint("number", __name__)


@app.route('/getAllNumbers', methods=["GET"])
def getAllNumbers():
    """Checks whether the applicant is authenticated,
        if so, consult the database to search for all registered numbers.
        If the query is not empty, send the returned data to the
        get_paginated_list function that executes the page logic.

    Returns:
        All registered numbers, due to the large number of records,
        the return uses a page strategy, where by default a limit of 20 records per page will be returned,
        starting from the first record, but the return can be changed,
        for that it must be informed in the request the limit arguments,
        which will inform the maximum number of records printed per page and the start argument,
        which should inform which record should start the return.

    Raises:
        Abort: If the user is not authenticated.
    """

    if 'authenticated' in session:
        result = Contacts.query.all()

        if len(result) == 0:
            return Response(response=dumps("No records found"), status=200, content_type="application/json")

        return jsonify(get_paginated_list(
            result,
            '/number/getAllNumbers',
            start=request.args.get('start', 1),
            limit=request.args.get('limit', 20)
        ))
    else:
        abort(401)

@app.route('/getNumberById/<int:numberID>', methods=["GET"])
def getNumberById(numberID):
    """Checks whether the requester is authenticated, if so,
        consult the database to search for the requested number.

    Args:
       numberID: number identifier to be searched

    Returns:
        A requested number.

    Raises:
        Abort: If the user is not authenticated.
    """

    if 'authenticated' in session:
        if numberID >= 0:
            contact = Contacts.query.get(numberID)
            if contact != None:
                return Response(response=dumps(contact.to_dict()), status='200', content_type="application/json")

        return Response(response=dumps({'status':'No records found', 'message':'Please enter a valid identifier for the number you would like to search for.'}),
                        status='200', content_type="application/json")
    else:
        abort(401)


@app.route('/addNumber', methods=["POST"])
def addNumber():
    """Check if the requester is authenticated, if so, read the parameters
        sent as arguments in the request and create a
        new Contact object that will be saved in the database.

        Returns:
            Details of the number added.

        Raises:
            Abort: If the user is not authenticated.
            ValueError: If the value sent in the numeric fields does not correspond to a valid decimal number.
            SQLAlchemyError: It was not possible to add the number to the database.
        """

    if 'authenticated' in session:

        try:
            monthyPrice = float(request.args['monthyPrice'])
            setupPrice = float(request.args['setupPrice'])
        except ValueError:
            return Response(response=dumps({'status': 'error', 'message': 'The monthyPrice and setupPrice fields must be valid decimal numbers.'}), status='200',
                            content_type="application/json")

        if monthyPrice < 0 or setupPrice < 0:
            return Response(response=dumps(
                {'status': 'error', 'message': 'The monthyPrice and setupPrice fields must be decimal numbers greater than 0.'}),
                            status='200',
                            content_type="application/json")

        contact = Contacts(request.args['value'], monthyPrice, setupPrice, request.args['currency'])
        db.session.add(contact)

        try:
            db.session.commit()
        except exc.SQLAlchemyError:
            return Response(response=dumps(
                {'status': 'error', 'message': 'It was not possible to save the information in our database. Please check the data sent and try again.'}),
                            status='200',
                            content_type="application/json")

        return Response(response=dumps({'status':'success', 'data':contact.to_dict()}), status='201', content_type="application/json")

    else:
        abort(401)

@app.route('/deleteNumber/<int:numberID>', methods=["GET", "DELETE"])
def deleteNumber(numberID):
    """Checks whether the applicant is authenticated, if so,
        delete the number corresponding to the received identifier.

       Args:
          numberID: number identifier to be delete.

       Returns:
           Confirmation of success.

       Raises:
           Abort: If the user is not authenticated.
           SQLAlchemyError: It was not possible to delete the number to the database.
    """

    if 'authenticated' in session:
        if numberID >= 0:

            contact = Contacts.query.get(numberID)

            if contact != None:
                db.session.delete(contact)
                try:
                    db.session.commit()
                except exc.SQLAlchemyError:
                    return Response(response=dumps( {'status': 'error',
                        'message': 'It was not possible to delete the information in our database. ' 
                                   'Please check the data sent and try again.'}),  status='200', content_type="application/json")


                return Response(response=dumps({'status': 'success'}), status='200',
                            content_type="application/json")

        return Response(response=dumps(
            {'status': 'No records found', 'message': 'Please enter the identifier of the number you would like to delete.'}),
                        status='200', content_type="application/json")
    else:
        abort(401)

@app.route('/editNumber/<int:numberID>', methods=["POST", "PUT"])
def editNumber(numberID):
    """Checks whether the applicant is authenticated, if so,
            edit the number corresponding to the received identifier.

           Args:
              numberID: number identifier to be edit.

           Returns:
              Details of the edited number.

           Raises:
               Abort: If the user is not authenticated.
               ValueError: If the value sent in the numeric fields does not correspond to a valid decimal number.
               SQLAlchemyError: It was not possible to edit the number to the database.
        """
    if 'authenticated' in session:
        contact = Contacts.query.get(numberID)

        if contact != None:
            try:
                monthyPrice = float(request.args['monthyPrice'])
                setupPrice = float(request.args['setupPrice'])
            except ValueError:
                return Response(response=dumps({'status': 'error',
                                                'message': 'The monthyPrice and setupPrice fields must be valid decimal numbers.'}),
                                                status='200',  content_type="application/json")

            if monthyPrice < 0 or setupPrice < 0:
                return Response(response=dumps( {'status': 'error',
                        'message': 'The monthyPrice and setupPrice fields must be decimal numbers greater than 0.'}),
                        status='200', content_type="application/json")

            contact.value = request.args['value']
            contact.monthyPrice = monthyPrice
            contact.setupPrice = setupPrice
            contact.currency = request.args['currency']

            try:
                db.session.commit
            except exc.SQLAlchemyError:
                return Response(response=dumps({'status': 'error',
                        'message': 'It was not possible to edit the information in our database. ' 
                                   'Please check the data sent and try again.'}), status='200', content_type="application/json")

            return Response(response=dumps({'status': 'success', 'data': contact.to_dict()}), status='200',
                        content_type="application/json")

        else:
            return Response(response=dumps(
                {'status': 'No records found', 'message': 'Please enter the identifier of the number you would like to edit.'}),
                status='200', content_type="application/json")
    else:
        abort(401)


def get_paginated_list(result, url, start, limit):
    """Identifies how many records were returned in the database query.
        Converts the result to a dictionary structure.
        Verified the start of the page and the limit of records per page.
        Identifies which records are on the current page, the next page and the next page and returns an object with this information.

      Args:
        result: records that will be pageed.
        url: address for consultation.
        start: record index that should start the page.
        limit: total records per page.

      Returns:
         object with the following information:
            index of the beginning of the page.
            total number of records per page.
            total records found.
            url to previous page.
            url to next page.
            records from the current page.
      Raises:
            Abort: Index for the beginning of the page greater than the
                    total number of elements returned in the query.
    """

    count = len(result)

    results = [c.to_dict() for c in result]

    start = int(start)
    limit = int(limit)

    if (count < start):
        abort(404)
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count

    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d&limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)

    obj['results'] = results[(start - 1):(start - 1 + limit)]

    return obj