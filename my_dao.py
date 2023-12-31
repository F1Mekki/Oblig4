from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json
URI = "neo4j+s://1a80dac1.databases.neo4j.io"
AUTH = ("neo4j", "hc/rH7QXs6fa")
#/&¤¤%
# 1234 how many
def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    return driver

def node_to_json(node):
    node_properties = dict(node.items())
    return node_properties

def findAllCars():
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) RETURN a;")
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

def findCarByReg(reg):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car) where a.reg=$reg RETURN a;", reg=reg)
        print(cars)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        session.close()
        return nodes_json

def save_car(make, model, reg, year, capacity):
    cars = _get_connection().execute_query("MERGE (a:Car{make: $make, model: $model, reg: $reg, year: $year, capacity:$capacity}) RETURN a;", make = make, model =
    model, reg = reg, year = year, capacity = capacity)
    nodes_json = [node_to_json(record["a"]) for record in cars]
    print(nodes_json)
    return nodes_json


def update_car(make, model, reg, year, capacity):
    with _get_connection().session() as session:
        cars = session.run("MATCH (a:Car{reg:$reg}) set a.make=$make, a.model=$model, a.year = $year, a.capacity = $capacity RETURN a;", reg=reg, make=make,
        model=model, year=year, capacity=capacity)
        print(cars)
        nodes_json = [node_to_json(record["a"]) for record in cars]
        print(nodes_json)
        return nodes_json

def delete_car(reg):
    _get_connection().execute_query("MATCH (a:Car{reg: $reg}) delete a;", reg = reg)


<<<<<<< HEAD
=======
# mir lova lova
## zaggi wer r u

>>>>>>> cdc043aad30c2155c12fcaf5ac690a4dc9896138
findAllCars()
