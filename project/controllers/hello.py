from project import app
from flask import render_template, request, redirect, url_for, jsonify
from project.models.User import findUserByUsername


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
            print(f"Error: {err}")
    else:
        data = {
            "username": "Not specified",
            "email": "Not specified"
        }
    return render_template('index.html.j2', data=data)


# Define CRUD Endpoints for 'Cars,' 'Customer,' and 'Employee'

# Create, Read, Update and Delete ‘Cars' with basic information
# e.g., make, model, year, location, status (i.e., available, booked, rented, damaged):
@app.route("/api/cars", methods=["POST"])
def create_car():
    # Implement the logic to create a new car and save it to the database.
    # Use request.json to get data from the request.
    return jsonify({"message": "Car created successfully."})


# Read information about a car:
@app.route('/api/cars/<car_id>', methods=['GET'])
def get_car(car_id):
    # Implement the logic to retrieve information about the specified car.
    return jsonify({"message": f"Information about car {car_id}."})


# Update information about a car:
@app.route('/api/cars/<car_id>', methods=['PUT'])
def update_car(car_id):
    # Implement the logic to update information about the specified car.
    return jsonify({"message": f"Car {car_id} updated successfully."})


# Delete a car:
@app.route('/api/cars/<car_id>', methods=['DELETE'])
def delete_car(car_id):
    # Implement the logic to delete the specified car from the database.
    return jsonify({"message": f"Car {car_id} deleted successfully."})


# next
# Create, Read, Update and Delete ‘Customer’ with basic information e.g., name, age, address.
# Create a new customer:
@app.route("/api/customers", methods=["POST"])
def create_customer():
    # Implement the logic to create a new customer and save it to the database.
    # Use request.json to get data from the request.
    return jsonify({"message": "Customer created successfully."})


# Read information about a customer:
@app.route('/api/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    # Implement the logic to retrieve information about the specified customer.
    return jsonify({"message": f"Information about customer {customer_id}."})


# Update information about a customer:
@app.route('/api/customers/<customer_id>', methods=['PUT'])
def update_customer(customer_id):
    # Implement the logic to update information about the specified customer.
    return jsonify({"message": f"Customer {customer_id} updated successfully."})


# Delete a customer:
@app.route('/api/customers/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    # Implement the logic to delete the specified customer from the database.
    return jsonify({"message": f"Customer {customer_id} deleted successfully."})


# next Employee
# Create, Read, Update and Delete ‘Employee’ with basic information e.g., name, address, branch
# Create a new Employee:
@app.route("/api/employees", methods=["POST"])
def create_employee():
    # Implement the logic to create a new employee and save it to the database.
    # Use request.json to get data from the request.
    return jsonify({"message": "Employee created successfully."})


# Read information about an employee:
@app.route('/api/employees/<employee_id>', methods=['GET'])
def get_employee(employee_id):
    # Implement the logic to retrieve information about the specified employee.
    return jsonify({"message": f"Information about employee {employee_id}."})


# Update information about an employee:
@app.route('/api/employees/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    # Implement the logic to update information about the specified employee.
    return jsonify({"message": f"Employee {employee_id} updated successfully."})


# Delete an employee:
@app.route('/api/employees/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    # Implement the logic to delete the specified employee from the database.
    return jsonify({"message": f"Employee {employee_id} deleted successfully."})


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
@app.route('/api/cancel-order-car', methods=['POST'])
def cancel_order_car():
    data = request.json
    customer_id = data.get('customer-id')
    car_id = data.get('car-id')

    # Implement the logic to check if the customer has booked the specified car.
    # If the customer has booked the car, change the car's status from 'booked' to 'available.'

    return jsonify({"message": f"Booking for car {car_id} is canceled by customer {customer_id}."})


# Implement 'rent-car' Endpoint
@app.route('/api/rent-car', methods=['POST'])
def rent_car():
    data = request.json
    customer_id = data.get('customer-id')
    car_id = data.get('car-id')

    # Implement the logic to check if the customer has a booking for the specified car.
    # If the customer has a booking, change the car's status from 'booked' to 'rented.'

    return jsonify({"message": f"Car {car_id} is now rented by customer {customer_id}."})


# Implement 'return-car' Endpoint
@app.route('/api/return-car', methods=['POST'])
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
