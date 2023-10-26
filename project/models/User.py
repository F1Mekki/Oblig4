from neo4j import GraphDatabase

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
        car_exists = session.run("MATCH (a:Car{reg:$reg}) RETURN a;", reg=reg).single()

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


# Customer
# Create Customer
def save_customer(personnummer, name, age, address, carBooked):
    customers = _get_connection().execute_query(
        "MERGE (c:Customer{personnummer: $personnummer, name: $name, age: $age, address: $address, carBooked: $carBooked}) RETURN c;",
        personnummer=personnummer, name=name, age=age, address=address, carBooked=carBooked)
    print(customers)
    node_json = [node_to_json(record["c"]) for record in customers.records]
    print(node_json)
    return node_json


# Read Customer

def findAllCustomers():
    with _get_connection().session() as session:
        customers = session.run("MATCH (c:Customer) RETURN c;")
        node_json = [node_to_json(record["c"]) for record in customers]
        print(node_json)
        return node_json


# Update Customer

def update_customer(personnummer, name, age, address, carBooked):
    with _get_connection().session() as session:
        # Check if the customer with the given personnummer exists
        customer_exists = session.run("MATCH (c:Customer {personnummer:$personnummer}) RETURN c",
                                      personnummer=personnummer).single()
        if not customer_exists:
            raise ValueError(f"No customer found with personnummer: {personnummer}")

        # customer exists; update
        customers = session.run(
            """      
                MATCH (c:Customer {personnummer:$personnummer})
                SET c.personnummer=$personnummer,
                    c.name=$name,
                    c.age=$age,
                    c.address=$address,
                    c.carBooked=$carBooked,
                RETURN c
                """,
            personnummer=personnummer, name=name, age=age, address=address, carBooked=carBooked
        )
        nodes_json = [node_to_json(record["c"]) for record in customers]
        return nodes_json


def delete_customer(personnummer):
    _get_connection().execute_query("MATCH (c:Customer {personnummer:$personnummer}) DELETE c",
                                    personnummer=personnummer)


# employee
# Create Employee
def save_employee(personnummer, name, age, address, branch):
    employees = _get_connection().execute_query(
        "MERGE (c:Employee {personnummer: $personnummer, name: $name, age: $age, address: $address, branch: $branch "
        "}) RETURN c;",
        personnummer=personnummer, name=name, age=age, address=address, branch=branch)
    print(employees)
    node_json = [node_to_json(record["c"]) for record in employees.records]
    print(node_json)
    return node_json


# Read Employees
def findAllEmployees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (a:Employee) RETURN a")
        node_json = [node_to_json(record["a"]) for record in employees]
        print(node_json)
        return node_json


# Update Employee

def update_employee(personnummer, name, age, address, branch):
    with _get_connection().session() as session:
        # Check if the employee with the given personnummer exists
        employee_exists = session.run("MATCH (c:Employee {personnummer:$personnummer}) RETURN c",
                                      personnummer=personnummer).single()
        if not employee_exists:
            raise ValueError(f"No Employee found with personnummer: {personnummer}")

        # Employee exists; update
        employee = session.run(
            """                                                                                                          
                MATCH (c:Employee {personnummer:$personnummer})                                                          
                SET c.personnummer=$personnummer,                                                                        
                    c.name=$name,                                                                                        
                    c.age=$age,                                                                                          
                    c.address=$address, 
                    c.branch=$branch                                                                                 
                RETURN c                                                                                                 
                """,
            personnummer=personnummer, name=name, age=age, address=address, branch=branch
        )
        nodes_json = [node_to_json(record["c"]) for record in employee]
        return nodes_json


def delete_employee(personnummer):
    _get_connection().execute_query("MATCH (c:Employee {personnummer:$personnummer}) DELETE c",
                                    personnummer=personnummer)


# ################# Second half

# Implement an endpoint ‘order-car’ where:
# a customer-id, car-id is passed as parameters.
# The system must check that the customer with customer-id has not booked other cars.
# The system changes the status of the car with car-id from ‘available’ to ‘booked’.

# Order car
def customer_order_car(customer_id, car_id):
    with _get_connection().session() as session:
        # Retrieve Customer's carBooked property using personnummer
        customer_result = session.run(
            "MATCH (c:Customer {personnummer:$personnummer}) RETURN c.carBooked As carBooked;",
            personnummer=customer_id)
        customer_record = customer_result.single()

        carBooked = customer_record["carBooked"]
        # If the customer has already booked a car, return an error
        if carBooked:
            return False, "Customer has already booked a car."

        # Check if the car is available
        car_result = session.run(
            "MATCH (a:Car {reg: $reg}) RETURN a.status As status;",
            reg=car_id)
        car_record = car_result.single()  # retrieve single record if it exists
        #  print("Here car_record: ", car_record["status"])
        status = car_record["status"]

        # If the car is available, book it for the customer
        if status == "available":
            session.run(
                "MATCH (a:Car {reg: $reg}) SET a.status = 'booked' RETURN a;",
                reg=car_id
            )
            session.run(
                "MATCH (c:Customer {personnummer: $personnummer}) SET c.carBooked = $reg RETURN c;",
                personnummer=customer_id, reg=car_id
            )
            return True, f"Car {car_id} is now booked by customer {customer_id}."

        else:
            return False, f"Car {car_id} is not available."


# Cancel order car
def customer_cancel_car(customer_id, car_id):
    with _get_connection().session() as session:
        # Retrieve Customer's carBooked property using personnummer
        customer_result = session.run(
            "MATCH (c:Customer {personnummer:$personnummer}) RETURN c.carBooked As carBooked;",
            personnummer=customer_id)
        customer_record = customer_result.single()  # returns False if customer have not booked any cars.
        carBooked = customer_record["carBooked"]

        car_result = session.run(
            "MATCH (a:Car {reg: $reg}) RETURN a.reg As reg;",
            reg=car_id)
        car_record = car_result.single()  # retrieve single record if it exists
        car_reg = car_record["reg"]

        if not carBooked:
            return True, f"Customer: Customer ID {customer_id} has no car booked."
        elif carBooked == car_reg:
            session.run(
                "MATCH (a:Car {reg: $reg}) SET a.status = 'available' RETURN a;",
                reg=car_id
            )
            session.run(
                "MATCH (c:Customer {personnummer: $personnummer}) SET c.carBooked = $false RETURN c;",
                personnummer=customer_id, false=False
            )
            return True, (f"The customer: Customer ID: {customer_id} canceled his order and The Car: Car ID: {car_id} "
                          f"is now available.")

        else:
            return False, f"Customer: {customer_id} has another booked car: Register number {car_reg}."


#  Rent car
def customer_rent_car(customer_id, car_id):
    with _get_connection().session() as session:
        # Retrieve Customer's carBooked property using personnummer
        customer_result = session.run(
            "MATCH (c:Customer {personnummer:$personnummer}) RETURN c.carBooked As carBooked;",
            personnummer=customer_id)
        customer_record = customer_result.single()  # returns False if customer have not booked any cars.
        carBooked = customer_record["carBooked"]

        # Retrieve Car's reg property using car_id
        car_result = session.run(
            "MATCH (a:Car {reg: $reg}) RETURN a.reg As reg;",
            reg=car_id)
        car_record = car_result.single()  # retrieve single record if it exists
        car_reg = car_record["reg"]

        if not carBooked:  # if the customer have not booked any car at all
            return True, f"Customer: Customer ID {customer_id} has no car booked."
        elif carBooked == car_reg:
            session.run(
                "MATCH (a:Car {reg: $reg}) SET a.status = 'rented' RETURN a;",
                reg=car_id
            )
            return True, f"The customer: Customer ID: {customer_id} rented his car order: Car ID: {car_id} "

        else:
            return False, f"Customer: {customer_id} has another booked car: Register number {car_reg}."


# Return car
# the customer was a troublemaker and damaged the rented car ;)

def car_condition(customer_id, car_id):
    with _get_connection().session() as session:
        # Retrieve Customer's carBooked property using personnummer
        customer_result = session.run(
            "MATCH (c:Customer {personnummer:$personnummer}) RETURN c.carBooked As carBooked;",
            personnummer=customer_id)
        customer_record = customer_result.single()  # returns False if customer have not booked any cars.
        carBooked = customer_record["carBooked"]

        # Retrieve Car's reg property using car_id
        car_result = session.run(
            "MATCH (a:Car {reg: $reg}) RETURN a.reg As reg;",
            reg=car_id)
        car_record = car_result.single()  # retrieve single record if it exists
        car_reg = car_record["reg"]

        if not carBooked:  # if the customer have not booked/rented any car at all # false
            return True, f"Customer: Customer ID {customer_id} has no car rent."

        elif carBooked == car_reg:
            session.run(
                "MATCH (a:Car {reg: $reg}) SET a.status = 'damaged' RETURN a;",
                reg=car_id
            )
            session.run(     # removing the booked/rented car from customer carBooked property to false
                "MATCH (c:Customer {personnummer: $personnummer}) SET c.carBooked = $false RETURN c;",
                personnummer=customer_id, false=False
            )

            return True, f"The customer ID: {customer_id} returned car ID: {car_id}. Status: Damaged. "

        else:
            return False, f"Customer: {customer_id} has another booked car: Register number {car_reg}."

# End
