from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re

URI = "neo4j+s://1a80dac1.databases.neo4j.io"
AUTH = ("neo4j", "56EKaLKqJ0yU6In0TC_u1gUkmi237dgthBG9XCCbXtA")


# test
def _get_connection() -> Driver | None:
    try:
        driver = GraphDatabase.driver(URI, auth=AUTH)
        driver.verify_connectivity()
        return driver
    except Exception as e:
        print(f"Error: {e}")
        return None


# test
driver = _get_connection()
if driver:
    print("It worked")
else:
    print("Failed to connect to the database.")


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
