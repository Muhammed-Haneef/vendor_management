# vendor_management

This is a Django-based Vendor Management System with a RESTful API for managing vendors, purchase orders, and vendor performance metrics.

## Features
- CRUD operations for vendors, purchase orders, and vendor performance metrics.
- JWT authentication for secure API access.
- Simple frontend to interact with the API.


### Prerequisites
- Python 3.x
- Django
- Django REST Framework

Install dependencies:
pip install -r requirements.txt

Apply migrations:
python manage.py migrate

Run the development server:
python manage.py runserver



API Endpoints
Vendors:

List and Create: /api/vendors/ (GET, POST)
Retrieve, Update, Delete: /api/vendors/{id}/ (GET, PUT, DELETE)
Purchase Orders:

List and Create: /api/purchase_orders/ (GET, POST)
Retrieve, Update, Delete: /api/purchase_orders/{id}/ (GET, PUT, DELETE)
Vendor Performance Metrics:

List and Create: /api/vendor_performance/ (GET, POST)
Retrieve, Update, Delete: /api/vendor_performance/{id}/ (GET, PUT, DELETE)





