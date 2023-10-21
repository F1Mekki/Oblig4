from project import app
from flask import render_template, request, jsonify, json
from project.models.User import findUserByUsername, save_car, findAllCars, update_car, delete_car
from project.models.User import save_customer, findAllCustomers, update_customer, delete_customer
from project.models.User import save_employee, findAllEmployees, update_employee, delete_employee


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
    return save_customer(record["personnummer"], record["name"], record["age"], record["address"])


# Read Customer information:
@app.route('/get_customers', methods=['GET'])
def get_customers():
    customers = findAllCustomers()
    return customers


# Update information about a customer:
@app.route('/update_customer', methods=['PUT'])
def update_customer_info():
    data = request.json
    required_fields = ["personnummer", "name", "age", "address"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        updated_customer = update_customer(
            data["personnummer"],
            data['name'],
            data['age'],
            data['address'])

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

# Implement an endpoint ‘order-car’ where a customer-id, car-id is passed as parameters.
@app.route('/api/order-car', methods=['POST'])
def order_car():
    data = request.json
    customer_id = data.get('customer-id')
    car_id = data.get('car-id')

    # Implement the logic to check if the customer has not booked other cars.
    # Change the status of the car with car_id from 'available' to 'booked' if the customer is eligible.

    return jsonify({"message": f"Car {car_id} is now booked by customer {customer_id}."})


# Implement 'cancel-order-car' Endpoint
@app.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    data = request.json
    customer_id = data.get('customer-id')
    car_id = data.get('car-id')

    # Implement the logic to check if the customer has booked the specified car.
    # If the customer has booked the car, change the car's status from 'booked' to 'available.'

    return jsonify({"message": f"Booking for car {car_id} is canceled by customer {customer_id}."})


# Implement 'rent-car' Endpoint
@app.route('/rent-car', methods=['POST'])
def rent_car():
    data = request.json
    customer_id = data.get('customer-id')
    car_id = data.get('car-id')

    # Implement the logic to check if the customer has a booking for the specified car.
    # If the customer has a booking, change the car's status from 'booked' to 'rented.'

    return jsonify({"message": f"Car {car_id} is now rented by customer {customer_id}."})


# Implement 'return-car' Endpoint
@app.route('/return-car', methods=['POST'])
def return_car():
    data = request.json
    customer_id = data.get('customer-id')
    car_id = data.get('car-id')
    car_condition = data.get('car-condition')  # Expected values: 'ok' or 'damaged'

    # Implement the logic to check if the customer has rented the specified car.
    # If the customer has rented the car, change the car's status from 'rented' to 'available' or 'damaged'
    # based on the car's condition.

    return jsonify(
        {"message": f"Car {car_id} has been returned by customer {customer_id} in {car_condition} condition."})
