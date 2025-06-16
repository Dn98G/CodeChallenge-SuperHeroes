# Superheroes-codechallenge
# Superheroes API

## Project Description
The Superheroes API is a RESTful web service that allows users to manage superheroes and their powers, enabling users to retrieve, create, and update information about superheroes and their associated powers.Built using Flask and SQLAlchemy.

### Technologies Used
- **Flask**: A lightweight WSGI web application framework for Python
- **SQLAlchemy**: An ORM for database management
- **Flask-Migrate**: To handle database migrations
- **Flask-RESTful**: For building REST APIs

### Challenges Faced
 with database relationships and validation

## Table of Contents
1. How to Install and Run the Project
2. How to Use the Project
3. Credits
4. License

## How to Install and Run the Project
1. Clone the repository:git clone https://github.com/rxhma-sys/Superheroes-codechallenge.git
2. Navigate to the project directory:cd Superheroes-codechallenge
3. Create a virtual environment and activate it:python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
4. Set up the database:
- flask db init
- flask db migrate -m "Initial Migration"
- flask db upgrade
5. Seed the database:
python seed.py
6. Run the application:
## Once the server is running, use Postman. Here are some endpoints:

Get all heroes: GET http://127.0.0.1:5555/heroes
Get a hero by ID: GET http://127.0.0.1:5555/heroes/<id>
Get all powers: GET http://127.0.0.1:5555/powers
Update a power: PATCH http://127.0.0.1:5555/powers/<id>
Create a hero-power relationship: POST http://127.0.0.1:5555/hero_powers

## Credits
Rahma Mohammed
# Special thanks to the canvas documentation , recording and online resources that guided me through the development process.
