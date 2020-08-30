import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from flask_migrate import Migrate
from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)

    #   @app.after_request
    # def after_request(response):
    #     response.headers.add(
    #         'Access-Control-Allow-Headers',
    #         'Content-Type,Authorization,true')
    #     response.headers.add(
    #         'Access-Control-Allow-Methods',
    #         'GET,PATCH,POST,DELETE,OPTIONS')
    #     return response

    # ROUTES
    '''
        GET /movies
            require the 'get:movies' permission
            it returns status code 200 and movies list
    '''

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        movies = Movie.query.all()
        if not movies:
            abort(404)
        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            "success": True,
            "movies": formatted_movies,
        }), 200

    '''
        GET /actors
            require the 'get:actors' permission
            it returns status code 200 and actors list
    '''

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.all()
        if not actors:
            abort(404)
        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            "success": True,
            "actors": formatted_actors,
        }), 200

    '''
        POST /movies
            create a new row in the movies table
            require the 'post:movies' permission
        returns status code 200 and the new movie
    '''

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movies(jwt):
        body = request.get_json()
        try:
            new_movie = Movie(title=body.get('title'),
                              release_date=body.get('release_date'))
            new_movie.insert()
            formatted_movie = new_movie.format()
        except Exception:
            abort(400)
        return jsonify({
                "success": True,
                "movies": formatted_movie,
            }), 200

    '''
        POST /actors
            create a new row in the actors table
            require the 'post:actors' permission
        returns status code 200 and the new actor
    '''

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actors(jwt):
        body = request.get_json()
        try:
            new_actor = Actor(name=body.get('name'), age=body.get('age'),
                              gender=body.get('gender'),
                              movie_id=body.get('movie_id'))
            new_actor.insert()
            formatted_actor = new_actor.format()
        except Exception:
            abort(400)
        return jsonify({
                "success": True,
                "actors": formatted_actor,
            }), 200

    '''
        PATCH /movies/<id>
            where <id> is the existing model id
            respond with a 404 error if <id> is not found
            update the corresponding row for <id>
            require the 'patch:movies' permission
            returns status code 200 and updated movie
    '''

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(jwt, id):
        body = request.get_json()
        movie = Movie.query.get(id)
        if not movie:
            abort(404)
        try:
            if 'title' in body:
                movie.title = body['title']
            if 'release_date' in body:
                release_date = body.get('release_date')
                movie.release_date = release_date
            movie.update()
        except Exception:
            abort(400)
        return jsonify({
            "success": True,
            "movies": movie.format(),
        }), 200

    '''
        PATCH /actors/<id>
            where <id> is the existing model id
            respond with a 404 error if <id> is not found
            update the corresponding row for <id>
            require the 'patch:actors' permission
            returns status code 200 and updated actor
    '''

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(jwt, id):
        body = request.get_json()
        actor = Actor.query.get(id)
        if not actor:
            abort(404)
        try:
            if 'name' in body:
                print(actor.name)
                actor.name = body.get('name')
            if 'age' in body:
                age = body.get('age')
                actor.age = age
            if 'gender' in body:
                gender = body.get('gender')
                actor.gender = gender
            if 'movie_id' in body:
                movie_id = body.get('movie_id')
                actor.movie_id = movie_id
            actor.update()
        except Exception:
            abort(400)
        return jsonify({
            "success": True,
            "actors": actor.format(),
        }), 200

    '''
        DELETE /movies/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:movies' permission
        returns status code 200 and id of deleted movie
    '''

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):
        movie = Movie.query.get(id)
        if not movie:
            abort(404)
        movie.delete()
        return jsonify({
            "success": True,
            "delete": movie.id,
        }), 200

    '''
        DELETE /actors/<id>
            where <id> is the existing model id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:actors' permission
        returns status code 200 and id of deleted actor
    '''

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        actor = Actor.query.get(id)
        if not actor:
            abort(404)
        actor.delete()
        return jsonify({
            "success": True,
            "delete": actor.id,
        }), 200

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

    @app.errorhandler(404)
    def not_found(error):
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
                        "message": "bad request"
                    }), 400

    '''
    error handler for AuthError
    '''

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app

app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
