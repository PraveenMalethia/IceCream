clone this repo

install virtualenv using 
- `pip install virtualenv`

create new env using

- `virtualenv env` or `python -m virtualenv env`

activate virtualenv

- (linux) `source env/bin/activate`
- (windows) `env\bin\activate`

install dependecies in env

- `pip install -r requirements.txt`

Run migrations

- `python manage.py migrate`

Create a superuser using 

- `python manage.py createsuperuser`

Go to admin panel - 

- http://127.0.0.1:8000/admin


Create dummy products to test the API

Hit API endpoint to buy ice cream from truck
with payload
{
  'product':'product-slug',
  'truck':'truck-slug'
}
- http://127.0.0.1:8000/api/v1/buy


Hit API endpoint to check total sales of truck

- http://127.0.0.1:8000/api/v1/truck-slug/total-sales