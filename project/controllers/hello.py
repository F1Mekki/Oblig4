from project import app
from flask import render_template, request, jsonify, json
from project.models.User import findUserByUsername, save_car, findAllCars, update_car, delete_car
from project.models.User import save_customer, findAllCustomers, update_customer, delete_customer
from project.models.User import save_employee, findAllEmployees, update_employee, delete_employee
from project.models.User import customer_order_car, customer_cancel_car, customer_rent_car, car_condition


# route index
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        try:
            user = findUserByUsername(username)
            data = {
                "username": user.username,
                "email": user.email
            }
        except Exception as err:
            print("Error2: ", err)

    else:
        data = {
            "username": "Not specified",
            "email": "Not specified"
        }
    return render_template('index.html.j2', data=data)


# Define CRUD Endpoints for 'Cars,' 'Customer,' and 'Employee'


# Create, Read, Update and Delete ‘Cars' with basic information
# e.g., make, model, year, location, status (i.e., available, booked, rented, damaged):

# Route to display the car registration form
# Create Cars
@app.route('/register_car', methods=['GET'])
def display_car_registration_form():
    return render_template('register_cars.html')


@app.route("/save_car", methods=["POST"])
def create_car():
    reg = request.form['reg']
    make = request.form['make']
    model = request.form['model']
    year = request.form['year']
    location = request.form['location']
    status = request.form['status']

    return save_car(reg, make, model, year, location, status)


# Read Cars information (listing all cars)
@app.route('/get_cars', methods=['GET'])
def query_records():
    cars = findAllCars()
    return cars


# Update Cars information
# Test data format in json in postman body JSON
"""
{
  "reg": "1",
  "make": "Tesla",
  "model": "Model S",
  "year": "2024",
  "location": "Oslo",
  "status": "booked"
}
"""


@app.route('/update_car', methods=['PUT'])
def update_car_info():
    data = request.json
    required_fields = ["reg", "make", "model", "year", "location", "status"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        updated_car = update_car(
            data["reg"],
            data['make'],
            data['model'],
            data['year'],
            data['location'],
            data['status']
        )
        return jsonify(updated_car), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404  # Not Found error for missing car
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete a car:
@app.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    record = json.loads(request.data)  # convert json to python
    print(record)
    delete_car(record['reg'])
    return findAllCars()


#  ############ Customers ######

# Next: Create, Read, Update and Delete ‘Customer’ with basic information
# personnummer, name, age, address.

# Create a new customer:
@app.route("/register_customer", methods=["POST"])
def register_customer():
    record = json.loads(request.data)
    print("Customer to be Registered: ", record)
    return save_customer(record["personnummer"], record["name"], record["age"], record["address"], record["carBooked"])


# Read Customer information:
@app.route('/get_customers', methods=['GET'])
def get_customers():
    customers = findAllCustomers()
    return customers


# Update information about a customer:
@app.route('/update_customer', methods=['PUT'])
def update_customer_info():
    data = request.json
    required_fields = ["personnummer", "name", "age", "address", "carBooked"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        updated_customer = update_customer(
            data["personnummer"],
            data['name'],
            data['age'],
            data['address'],
            data['carBooked'])

        return jsonify(updated_customer), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404  # Not Found error for missing car
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete a customer:
@app.route('/delete_customer', methods=['DELETE'])
def delete_customer_info():
    record = json.loads(request.data)  # convert json data format to python format
    print("Customer To Be Deleted: ", record)
    delete_customer(record["personnummer"])
    return findAllCustomers()


# Employee
# Create, Read, Update and Delete ‘Employee’ with basic information
# (personnummer, name, address, branch ("Bergen, Oslo, Stavanger") )

# Create a new Employee:
@app.route("/register_employee", methods=["POST"])
def register_employee():
    record = json.loads(request.data)
    print("Employee to be Registered: ", record)
    return save_employee(record["personnummer"], record["name"], record["age"], record["address"], record["branch"])


# Read Employee information:
@app.route('/get_employee', methods=['GET'])
def get_employees():
    employees = findAllEmployees()
    return employees


# Update information about an Employee:
@app.route('/update_employee', methods=['PUT'])
def update_employee_info():
    data = request.json
    required_fields = ["personnummer", "name", "age", "address", "branch"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        updated_employee = update_employee(
            data["personnummer"],
            data['name'],
            data['age'],
            data['address'],
            data["branch"])

        return jsonify(updated_employee), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404  # Not Found error for missing car
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Delete an Employee:
@app.route('/delete_employee', methods=['DELETE'])
def delete_employee_info():
    record = json.loads(request.data)  # convert json data format to python format
    print("Employee To Be Deleted: ", record)
    delete_employee(record["personnummer"])
    return findAllCustomers()


# ################# Second half

# Implement an endpoint ‘order-car’ where:
# a customer-id, car-id is passed as parameters.
# The system must check that the customer with customer-id has not booked other cars.
# The system changes the status of the car with car-id from ‘available’ to ‘booked’.

@app.route('/order_car', methods=['PUT'])
def order_car():
    record = json.loads(request.data)
    car_id = record["reg"]  # car_id of the node Car is "reg" in neo4j DB
    customer_id = record["personnummer"]  # customer id of the node Customer is personnummer in neo4j DB

    success, message = customer_order_car(customer_id, car_id)

    if success:
        return jsonify({"message": message})
    else:
        return jsonify(message, status=400)  # 400 Bad Request


# Implement 'cancel-order-car' Endpoint where:
# where a customer-id, car-id is passed as parameters.
# The system must check that the customer with customer-id has booked for the car.
# If the customer has booked the car, the car becomes available.
@app.route('/cancel_order_car', methods=['PUT'])
def cancel_order_car():
    data = json.loads(request.data)
    customer_id = data.get('personnummer')  # or data["personnummer"]
    car_id = data.get('reg')  # or data["reg"]
    success, message = customer_cancel_car(customer_id, car_id)

    if success:
        return jsonify({"message": message})
    else:
        return jsonify(message, status=400)  # 400 Bad Request


# Implement 'rent-car' Endpoint where:
# where a customer-id, car-id is passed as parameters.
# The system must check that the customer with customer-id has a booking for the car.
# The car’s status is changed from ‘booked’ to ‘rented’.

@app.route('/rent_car', methods=['PUT'])
def rent_car():
    data = request.json  # or data = json.loads(request.data)
    customer_id = data.get('personnummer')
    car_id = data.get('reg')

    success, message = customer_rent_car(customer_id, car_id)
    if success:
        return jsonify({"message": message})
    else:
        return jsonify(message, status=400)  # 400 Bad Request


# Implement 'return-car' Endpoint where:
# where a customer-id, car-id is passed as parameters.
# Car’s status (e.g., ok or damaged) during the return will also be sent as a parameter.
# The system must check that the customer with customer-id has rented the car.
# The car’s status is changed from ‘booked’ to ‘available’ or ‘damaged’
@app.route('/return_car', methods=['PUT'])
def return_car():
    data = request.json  # or data = json.loads(request.data)
    customer_id = data.get('personnummer')
    car_id = data.get('reg')

    success, message = car_condition(customer_id, car_id)

    if success:
        return jsonify({"message": message})
    else:
        return jsonify(message, status=400)  # 400 Bad Request

# End
