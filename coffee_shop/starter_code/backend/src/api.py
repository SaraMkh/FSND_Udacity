import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_ALLdrinks():
        try:
            All_drinks = Drink.query.all()
            drinks = [drinki.short() for drinki in All_drinks]
            return jsonify({
                'success': True,
                "drinks": drinks
            }), 200
        except Exception as error:
            raise error

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
        where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
        try:
            All_drinks = Drink.query.all()
            return jsonify({
                'success': True,
                "drinks": [drinki.short() for drinki in All_drinks]
            }), 200
        except Exception as error:
            raise error

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
        body = request.get_json()
        if body is None:
            abort(401)
        new_title = body.get('title', None)
        drink_recipe = body.get('recipe', None)
        new_recipe = json.dumps(drink_recipe)

        try:
            new_drink = Drink(title=new_title, recipe=json.dumps(new_recipe))
            new_drink.insert()
            return jsonify({
                'success': True,
                "drinks": [new_drink.long()]
            }), 200
        except Exception as error:
            raise error

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
        where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink_details(payload, id):

        try:
            find_drink = Drink.query.filter(Drink.id == id).first()
            if find_drink is None:
                abort(404)
            else:
                body = request.get_json()
                drink_title = body.get('title', None)
                recipe = body.get('recipe', None)
                drink_recipe = json.dumps(recipe)
                find_drink.title = drink_title
                find_drink.recipe = drink_recipe
                find_drink.update()
                return jsonify({
                    'success': True,
                    "drinks": [find_drink.long()]
                    }), 200
        except Exception as error:
            raise error


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
        try:
            find_drink = Drink.query.filter(Drink.id == id).first()
            if find_drink is None:
                abort(404)
            else:
                find_drink.delete()
                return jsonify({
                    'success': True,
                    "drinks": find_drink.id
                    }), 200
        except Exception as error:
            raise error
'''
raise appropriate status code reflecting the reason of failure
'''

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False,
                    "error": 400,
                    "message": "Bad Request"
                    }), 400


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
                    "success": False,
                    "error": 405,
                    "message": "Method Not Allowed"
                    }), 405


@app.errorhandler(500)
def Internal_Server_Error(error):
    return jsonify({
                    "success": False,
                    "error": 500,
                    "message": 'Internal Server Error'
                    }), 500


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def auth_error(err):
    response = jsonify(err.error)
    response.status_code = err.status_code
    return response
