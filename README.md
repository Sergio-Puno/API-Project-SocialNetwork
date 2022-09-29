#### Status: In Process

# API-Project-SocialNetwork
Mock API for a social network application
Video reference for this project: [Sanjeev Thiyagarajan - Python API Development](https://www.youtube.com/watch?v=0sOvCWFmrtA)

## Main goals for this project
- Build out an API from scratch
- Build out local PostgreSQL database
- Setup data masking and encrypting process
- User auth management

While working with data there are often times that I've had to work with APIs to extract or query a database in order to get information. I have not had the opportunity to try to build an API myself and I believe going through the process of creating one from scratch would greatly improve my ability to work with APIs in the future as well as give me the confidence to build one in the future for work.

As this project is meant for learning, I want to get to the root of APIs, as with learning any topic the key take away is not about the specific technologies, but rather about the first principles that drive the design decisions and implementation.

## Tools
Using Python for this project, packages in use:
- [`FastAPI`](https://fastapi.tiangolo.com/)
- [`psycopg2`](https://www.psycopg.org/docs/)
- [`configparser`](https://docs.python.org/3/library/configparser.html)
- [`pydantic`](https://pydantic-docs.helpmanual.io/)
- [`sqlalchemy`](https://www.sqlalchemy.org/)
- [`passlib`](https://passlib.readthedocs.io/en/stable/) & [`bcrypt`](https://pypi.org/project/bcrypt/)
- [`email-validator`](https://pypi.org/project/email-validator/)
- [`python-jose`](https://pypi.org/project/python-jose/)

Might missed a few but hopefully this list at least contains the main packages (there may be additional dependencies), check the `requirements.txt` file for a full lsit of packages and vesions for this project.

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

An example ORM would be the Python package `SQLAlchemy` which offers us the ability to model out our database tables within Python and use built in functions to perform our queries.

### Storing Sensitive Data

An example of sensitive information that would flow through an API is the user's password they would create when setting up their account.

### User Authentication

Made use of the token design pattern through JWT. 

# Challenges

Wanted to keep note of any issues I had or concepts that were more difficult to implement as well as any decisions I made during the creation of this project. While I did follow along with Sanjeev at various parts of the development process, I did make my own decisons and experimented where able in order to gain additional understanding as to why certain choices could be made.

## ORM or Not?

One of the bigger issues I had dealt with the choice between raw SQL queries or using an ORM (`SQLAlchemy`). Initially I wanted to work through this project using raw SQL instead of switching to using SQLAlchemy as I am very confortable with SQL and would be able to code out the operations quickly.

At first, while the operations were simple, I was able to implement the rudimentary `POST` / `GET` / `DELETE` quite easily and using `psycopg2` for my query execution was not adding much overhead to the code size. **However**, I did start to feel the pain a bit when I had to being coding out solution for something like adding a search parameter to pulling posts. Creating a parameterized SQL query started adding a lot of code, making it more difficult to track information flow and maintain understanding of the query state.

I believe ORMs have developed quite a bit over the years, and while it may at first be scary to turn over the SQL query creation over to this engine, there are now typically tools within the ORM to build out and execute raw SQL (see below for reference article).

https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/

The main takeaway here is that ORMs can handle most of the standard operations you would need, and in the end save you quite a bit of both coding time and code length. This depends on the application, the operation, and the extent to which you have to optimize your queries.

## Pydantic Data Classes

I have seen `pydantic` before and am familiar with the idea of data validation through other tools such as `Great Expectations` which is another validation tool for data warehouses. Since pydantic works in conjuctions with FastAPI you will see the two together and while working on this project, I often would get confused as to which tool was performing the validation.

You will be using pydantic in order to setup how certain data should look, and if you read the documentation you'll see that pydantic themselves make sure to point out the distinction of what is is they are guranteeing:

> pydantic guarantees the types and constraints of the output model, not the input data.

Due to this distinction - along with the inherent data conversion - there can be some confusion as to what is actually being validated. The sample provided in the documentation would be the value `4.32` being supplied to a model expecting an int, despite the value originally being a float the model will convert this into just `4` to match the int requirement.

## Alembic for Database Revision Tracking

Within this project there was the opportunity to use `Alembic` which is a python package that essentially allows us to track database changes similarly to how we use Git for tracking code revisions. The main benefits that this would provide are:

- Log data showing revisions to database
- Functions for changing the current revision that is active
- Autogenerate revision through SQLAlchemy model file

While there are clear benefits to using a revision tracking framework like alembic, for this project I decided not to implement it for a few reasons:

- Overhead of maintaining upgrade and downgrade logic (unless you autogenerate)
- Requirement to have all DDL and DML within this architecture
- Revisions are arbitrary alpha-numeric codes + name provided by the user, so files within the revisions folder are not structured
- Working through CLI (command line interface), not integrated with the tooling (autocomplete revision names would be nice)
- Upgrading and downgrading isn't really like Git where you "rollback" to a prior state, for the database there are still commands ran which means you are actaully moving forward in terms of revisions (despite thinking you are downgrading to a prior state)

If I want to make changes the database I simply use Datagrip (by Jetbrains), and while I do lose the tracking I feel that it is better to reason about my changes and ensure that I am aware that the database (unless you delete and recreate it) is a persistent object. The concept of "rollback" within alembic just means you delete a table, drop a column, alter data types, and all this means that you are not rolling back but rather you are submitting additional commands to get back to a prior state. 