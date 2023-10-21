from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re

# Read the environment variables from the .env file
NEO4J_URI = 'neo4j+s://356e2ccc.databases.neo4j.io'
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = 'SiadROB3iako5VQe1766_8FmrZPV0djDdUXTLI9fV20'

AUTH = (NEO4J_USERNAME, NEO4J_PASSWORD)


def _get_connection():
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
        driver.verify_connectivity()
        return driver
    except Exception as e:
        print(f"Error1: {e}")  # Error1: Unable to retrieve routing information
        return None  # None is returned to "def findUserByUsername(username)" and causes the second error:
        # Error2:  'NoneType' object has no attribute 'execute_query'


def findUserByUsername(username):
    data = _get_connection().execute_query("MATCH (a:User) where a.username = $username RETURN a;", username=username)
    if len(data[0]) > 0:
        user = User(username, data[0][0][0]['email'])
        return user
    else:
        return User(username, "Not found in DB")


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_Username(self):
        return self.username

    def set_Username(self, value):
        self.username = value

    def get_Email(self):
        return self.email

    def set_Email(self, value):
        self.email = value


def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties


# create a car
def save_car(reg, make, model, year, location, status):
    cars = _get_connection().execute_query(
        "MERGE (a:Car{reg: $reg, make: $make, model: $model, year: $year, location:$location, "
        "status: $status}) RETURN a;", reg=reg, make=make, model=model, year=year,
        location=location, status=status)
    print(cars)
    node_json = [node_to_json(record["a"]) for record in cars.records]
    print(node_json)

    return node_json


# Read cars
def findAllCars():
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json


# update car by reg


def update_car(reg, make, model, year, location, status):
    with _get_connection().session() as session:
        # Check if the car with the given reg exists
        car_exists = session.run("MATCH (a:Car{reg:$reg}) RETURN a", reg=reg).single()

        if not car_exists:
            raise ValueError(f"No car found with reg: {reg}")

        # Update the car details
        cars = session.run(
            """
            MATCH (a:Car{reg:$reg}) 
            SET a.make=$make, 
                a.model=$model, 
                a.year=$year, 
                a.location=$location, 
                a.status=$status 
            RETURN a;
            """,
            reg=reg, make=make, model=model, year=year, location=location, status=status
        )

        nodes_json = [node_to_json(record["a"]) for record in cars]
    return nodes_json


# delete a car by register number
def delete_car(reg):
    _get_connection().execute_query("MATCH (a:Car {reg:$reg}) DELETE a;", reg=reg)

######################
