# How to setup the project on your local server?

1. Clone the repository:

```CMD
git clone https://github.com/anshumannandan/MikeLegal
```
To run the server, you need to have Python installed on your machine. If you don't have it installed, you can follow the instructions [here](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/) to install it.

2. Navigate to the project directory: 

```CMD
cd MikeLegal
```

3. Install & Create a virtual environment:

```CMD
pip install virtualenv
virtualenv venv
```

4. Activate the virtual environment:
```CMD
venv/scripts/activate
```

5. Install the dependencies: 

```CMD
pip install -r requirements.txt
```

6. Setup .env file in MikeLegal/project/ and navigate back to base directory MikeLegal/:
```
SECRET_KEY =
DEBUG = 
```

7. Run the migrate command:
```CMD
python manage.py migrate
```

8. You can create a superuser executing the following commands:
```CMD
python manage.py createsuperuer
```
A prompt will appear asking for username, email followed by password. 

9. Run the backend server on localhost:

```CMD
python manage.py runserver
```

You can access the endpoints from your web browser following this url:
```url
http://127.0.0.1:8000
```

To access the django admin panel follow this link and login through superuser credentials:
```url
http://127.0.0.1:8000/admin/
```