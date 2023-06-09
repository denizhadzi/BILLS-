# CS50 Final Project - BILLS
#### Video Demo: <https://www.youtube.com/watch?v=gduvhIyx5ws>
#### Description:

My name is Deniz, and I'm a civil engineer from Maribor, Slovenia who set a goal for myself to learn programming.

To help me collect and send all the invoices costs for my apartment to my tenants with ease, I created a locally hosted web application for personal use.

The web application automatically collects all the invoices for my apartment, including electricity, gas, TV, building supervisor, and internet provider invoices from my Gmail labels and displays them on my webpage.

Technologies used:

- JS
- HTML
- Python
- Google API
- sqlite3
- flask
- css
- bootstrap
- other small libraries or packages

## How the web application works?

The web application allows me to log in to the webpage, and there is no register option since it is only meant for personal use. There are seven different HTML pages, one for each of the five providers, displaying all the bills collected from each specific provider. Every provider page includes an option to collect any new invoices automatically, if there are any. There is also one login/logout page and one home/index page, showing the invoices for all the providers combined and sorted by month. For every month on the index page, there is an option to automatically send all invoice expenses to my tenant's email.

During login I need to enter these fields:

-Username
-Password: which is hashed and checked if it exists in my database

## Backend

### Files (credential are not shown for security reasons)

In the backend of the application there are 8 .py files:

- **app.py** (main file that runs the main function and controls the page behavior)

- **helpers.py** ( in  which the apology function and login decorator are defined which are then used in the main file)

- **calculatin_bill.py** ( in which all the  functions that collect, modify, create, and send email data with help of the google API are defined )

- **elektro.py**, **plin.py**, **rtv.py**, **staninvest.py**, **telemach.py**: These files contain functions that go through every message in the Gmail label for the specific provider. The functions temporarily open the .xml attachment with the invoice information and search through the data in that attachment for the date and costs of the invoice for that month. All of the functions return a dictionary, for example: {'2022-12': 30.9, '2022-11': 29.0, '2022-10': 18.99, '2022-9': 41.84, '2022-8': 59.27}, with date/month as a key and the costs of the invoice for that date as a value. When all is done, all the checked messages are moved to another label.

### Tables

In finance.db database there are  7 tables:

- users table (collects my username and password data that is required for login)

- elektro table ( table of all the data collected from the elektro.py function, with the date/month as the primary key and costs for that date as  value)

- plin table ( table of all the data collected from the plin.py function, with the date/month as the primary key and costs for that date as  value)

- rtv table( table of all the data collected from the rtv.py function, with the date/month as the primary key and costs for that date as  value)

- staninvest table ( table of all the data collected from the staninvest.py function, with the date/month as the primary key and costs for that date as value)

- telemach table ( table of all the data collected from the telemach.py function, with the date/month as the primary key and costs for that date
as value)

- together table (the table that combines the data for the invoices from all the providers sorted by date with the help of the app.py)


## Frontend

- layout.html (the base for all the other pages)

- apology.html ( page to redirect to when an error occurs)

- login.html (login form)

- elektro.html (the page that shows the data from the Elektro table which is collected with the elektro.py function. At the bottom of the page there is a button that gives me the option  to add information from newly arrived invoices which returns an apology if there are no new invoices)

- plin.html (the page that shows the data from the plin table which is collected with the plin.py function. At the bottom of the page there is a button that gives us the option to add information from newly arrived invoices which returns an apology if there are no new invoices)

- rtv.html (the page that shows the data from the rtv table which is collected with the rtv.py function. At the bottom of the page there is a button that gives us the option to add information from newly arrived invoices which returns an apology if there are no new invoices)

- staninvest.html (the page that shows the data from the staninvest table which is collected with the staninvest.py function. At the bottom of the page there is a button that gives us the option to add information from newly arrived invoices which returns an apology if there are no new invoices)

- telemach.html (the page that shows the data from the telemach table which is collected with the telemach.py function. At the bottom of the page there is a button that gives us the option to add information from newly arrived invoices which returns an apology if there are no new invoices)

- index.html (homepage that shows all the data collected in the other tables combined and sorted by month. For every month there is also an option to automatically send an email to my tenants with the costs for all the invoices for that month.)

















