import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

TOKEN = os.environ['TOKEN']

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "Casting_Agency_test"
        self.database_path = "postgres://hala@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    test for successful operation and for expected errors.
    """
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)
        movies = Movie.query.all()
        formatted_movies = [movie.format() for movie in movies]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'], formatted_movies)

    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)
        actors = Actor.query.all()
        formatted_actors = [actor.format() for actor in actors]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'], formatted_actors)

    def test_401_if_token_does_not_exist(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['code'], 'authorization_header_missing')

    def test_401_if_token_is_invalid(self):
        res = self.client().get('/actors', headers={'Authorization': TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['code'], 'invalid_header')

    def test_404_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000', headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_404_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000', headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
    
    def test_create_new_movie(self):
        res = self.client().post('/movies', json={'title': 'amazing', 'release_date': '25-8-2020'}, headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)
        pass
    
    def test_create_new_actor(self):
        res = self.client().post('/actors', json={'name': 'Hala', 'age': 24, 'gender': 'Female', 'movie_id': 1}, headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)
        pass
    
    def test_400_if_movie_creation_fails(self):
        res = self.client().post('/movies', json={'title': 1234, 'release_date': '25-8-2020'}, headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)
        pass
    
    def test_400_if_actor_creation_fails(self):
        res = self.client().post('/actors', json={'name': 'Hala', 'age': 'hh', 'gender': 'Female', 'movie_id': 1}, headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)
        pass
    
    def test_edit_movie(self):
        res = self.client().patch('/movies/9', json={'title': 'joy'}, headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)
        pass
    
    def test_edit_actor(self):
        res = self.client().patch('/actors/9', json={'name': 'Noura'}, headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)
        pass
    
    def test_404_if_movie_does_not_exist(self):
        res = self.client().patch('/movies/1000', json={'title': 'joy'}, headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)
        pass
    
    def test_404_if_actor_does_not_exist(self):
        res = self.client().patch('/actors/1000', json={'name': 'Noura'}, headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)
        pass
    
    def test_delete_movie(self):
        res = self.client().delete('/movies/9', headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_delete_actor(self):
        res = self.client().delete('/actors/9', headers={'Authorization': 'Bearer ' + TOKEN})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
