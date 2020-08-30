# Capstone API Project

## Introduction
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Getting Started

### Pre-requisites and Local Development
Developers using this project should already have Python3, pip and node installed on their local machines.

## Backend
From the starter folder run the following command to install All required packages:
```bash
pip install -r requirements.txt
```
To run the application run the following commands:
```bash
python3 app.py
```
These commands put the application in development and use the `app.py` file in our starter folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.
The application is run on http://0.0.0.0:8080/ and production url is https://casting-agency-05.herokuapp.com/.

## Tests
In order to run tests navigate to the starter folder and run the following commands:
```
dropdb Casting_Agency_test
createdb Casting_Agency_test
python test_app.py
```
The first time you run the tests, omit the dropdb command.

## API Reference
GET /movies
* General:
    * Returns a list of movies objects and success value.
* Sample: curl https://casting-agency-05.herokuapp.com/movies
```
  {
    "movies": [
    {
        "id": 1,
        "title": "joy",
        "release_date": "25-6-2020"
        },
        {
        "id": 2,
        "title": "hush",
        "release_date": "25-6-2020"
        }
    ],
    "success": true
}
```
GET /actors
* General:
    * Returns a list of actor objects and success value.
* Sample: curl https://casting-agency-05.herokuapp.com/actors
```
{
    "actors": [
        {
        "age": 24,
        "gender": "Female",
        "name": "Hala",
        "id": 1,
        "movie_id": 2
        },
        {
        "age": 23,
        "gender": "Female",
        "name": "Fatima",
        "id": 2,
        "movie_id": 2
        }
    ],
    "success": true

}
```
POST /movies
 * General:
    * Creates a new movie using the submitted title and release date. Returns the success value and the created movie.
 * curl https://casting-agency-05.herokuapp.com/movies -X POST -H "Content-Type: application/json" -d '{"title":"seven", "release_date":"2020-06-11"}'
 ```
 {
    "movies": {
        "id": 3,
        "release_date": "Thu, 11 Jun 2020 00:00:00 GMT",
        "title": "seven"
    },
    "success": true
 }
 ```
POST /actors
 * General:
    * Creates a new actor using the submitted name, age, gender, and movie_id. Returns the success value and the created actor.
 * curl https://casting-agency-05.herokuapp.com/actors -X POST -H "Content-Type: application/json" -d '{"name":"hala", "age":24, "gender":"Female", "movie_id": 1}'
 ```
 {
    "actors": {
        "age": 24,
        "gender": "Female",
        "id": 5,
        "movie_id": 1,
        "name": "hala"
    },
    "success": true
 }
 ```
  DELETE /movies/{movie_id} 
 * General:
    * Deletes the movie of the given ID if it exists. Returns the success value and movie ID.
* curl -X DELETE https://casting-agency-05.herokuapp.com/movies/1
```
 {
    "delete": 1,
    "success": true,
 }
  ```
  DELETE /actors/{actor_id} 
 * General:
    * Deletes the actor of the given ID if it exists. Returns the success value and actor ID.
* curl -X DELETE https://casting-agency-05.herokuapp.com/actors/1
```
 {
    "delete": 1,
    "success": true,
 }
 ```
  PATCH /movies/1
* General:
    * Update the movie of the given ID using the submitted title or release date. Returns object of the updated movie and success value.
* curl https://casting-agency-05.herokuapp.com/movies/1 -X POST -H "Content-Type: application/json" -d '{"title":"kidnap"}' 
 ```
{
    "movies": {
        "id": 1,
        "release_date": "Thu, 11 Jun 2020 00:00:00 GMT",
        "title": "kidnap"
    },
    "success": true
 }
  ```
  PATCH /actors/1
* General:
    * Update the actor of the given ID using the submitted name, age, gender or movie_id. Returns object of the updated actor and success value.
* curl https://casting-agency-05.herokuapp.com/actors/1 -X POST -H "Content-Type: application/json" -d '{"name":"Noura"}' 
 ```
 {
    "actors": {
        "age": 24,
        "gender": "Female",
        "id": 5,
        "movie_id": 1,
        "name": "Noura"
    },
    "success": true
 }
```
## Users Roles:
* Casting Assistant
    * Can view actors and movies
* Casting Director
    * All permissions a Casting Assistant has and…
    * Add or delete an actor from the database
    * Modify actors or movies
* Executive Producer
    * All permissions a Casting Director has and…
    * Add or delete a movie from the database


## Authors
* Hala Almaimoni

## Acknowledgements
Many thanks to Udacity team, my session lead Ms. Elham Jaffar and my colleagues for all the assistance and support