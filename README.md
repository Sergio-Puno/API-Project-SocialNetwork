#### Status: In Process

# API-Project-SocialNetwork
Mock API for a social network application

## Main goals for this project
- Build out an API from scratch
- Build out local PostgreSQL database
- Setup data masking and encrypting process
- User auth management

## Tools
Using Python for this project, packages in use:
- [`FastAPI`](https://fastapi.tiangolo.com/)
- [`psycopg2`](https://www.psycopg.org/docs/)
- [`configparser`](https://docs.python.org/3/library/configparser.html)
- [`pydantic`](https://pydantic-docs.helpmanual.io/)
- [`passlib`](https://passlib.readthedocs.io/en/stable/) & [`bcrypt`](https://pypi.org/project/bcrypt/)
- [`email-validator`](https://pypi.org/project/email-validator/)
- [`python-jose`](https://pypi.org/project/python-jose/)

## Topics Covered
During the building of this project, several larger concepts or topics came up that encapsulate the API process:

- Data Validation
- Response handling
- Raw SQL vs. ORM
- Storing sensitive information
- User Authentication

I'll discuss each of these briefly to explain the concept, why it is important, and how I dealt with or implemented them within this mock API.

### Data Validation

A lot of data validation within this API is handled automatically by FastAPI. We can set expected data types of user inputs and create schemas or models within our app to ensure we validate user inputs before running any database operations.

### Response Handling

Within any program you want to make sure you are capturing errors and providing the user with as much useful information about issues as possible. Giving an end user a generic error or not providing additional context will make working with an API difficult.


### Raw SQL vs. ORM

There are two options when it comes to integrating with your database, you can either use a lightweight direct connection making use of raw SQL strings to perform CRUD operations, or you can make use of something called an ORM (Object Relational Mapping).

An example ORM would be the Python package `SQLAlchemy`

### Storing Sensitive Data

An example of sensitive information that would flow through an API is the user's password they would create when setting up their account.

### User Authentication

Made use of the token design pattern through JWT. 