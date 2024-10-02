# Blog and Todo features with Flask
This repo is for practicing web development with Flask based on its [official tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/). It also includes additional features like tailwind css and some JavaScript. For the UI, I generated with ChatGPT free version and modify later.

# Features
- User login and registration
- Blog features:
    - Post creation
    - Post listing with pagination
- Todo list management:
    - Create new Todo items
    - Update and delete Todo items using JavaScript fetch
    - Edit Todo items by double-clicking on them

# Run the project
## Requirements
Make sure to install all the dependencies listed in the requirements.txt file. Some key packages include:

- **Flask**: A micro web framework for Python.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library.
- **Jinja2**: Template engine for Python, used with Flask for rendering templates.
- **WTForms**: Form handling library for validation.
- **Tailwind CSS**: Utility-first CSS framework for styling.
- **Pytest**: Testing framework for Python applications.

### Activate venv
```
$ . .venv/bin/activate
```
### Install dependencies
```
$ pip install -r requirements.txt
```
### Install local package for pytest
```
$ pip install -e .
```
# Testing with pytest
### Run all the test
```
$ pytest
```
# Create .env
- Copy the `.env.example` to `.env`

# Create the Database
### init the db
```
$ flask db init 
// You man need to add FLASK_APP=microblog in system environment.
```
### migrage the db
```
$ flask db migrate
```