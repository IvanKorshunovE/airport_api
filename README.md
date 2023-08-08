# SkyLink: Elevating Flight and Airport Management

SkyLink is a comprehensive RESTful API designed to manage flight-related information and operations. It facilitates interaction with various resources, including flights, crews, airplanes, airplane types, orders, and tickets. The API empowers airlines, travel agencies, and other aviation-related services to efficiently handle flight data, bookings, and logistics.
## Requirements
- Python 3.x
- Django
- Django REST framework

### How to Run

1. Clone the repository: `git clone https://github.com/IvanKorshunovE/sky_link`
2. Change to the project directory: `cd airport_api`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment: `source venv/bin/activate`
5. Install the required packages: `pip install -r requirements.txt`
6. Create a `.env` file by copying the `.env.sample` file and populate it with the required values.
7. Run migrations: `python manage.py migrate`
8. Run the app: `python manage.py runserver`

### API Documentation

The API is well-documented with detailed explanations of each endpoint and their functionalities. The documentation provides sample requests and responses to help you understand how to interact with the API. You can access the API documentation by visiting the following URL in your browser:
- [API Documentation](http://localhost:8000/api/schema/swagger-ui/)
