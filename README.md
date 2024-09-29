# Marketplace Web App with REST API

This is a project done for CS50x, an online introduction to CS course hosted by Harvard University. The Swift Marketplace app lets vendors create, update and delete items from their store, view details on items and other vendors, update stock via the API. The application uses session based authentication for normal users and JWT authorization for API users.

## Project Demo Video: Coming soon

## Technologies Used 
* Python 3.12.6
* Flask (To handle routes and rendering templates etc)
* Flask-Session (To keep users logged in and keep track of the shopping cart)
* Flask_JWT_Extended (To authorize API users)
* SQLite3 (To store the data in an SQL database)
* Postman (To make API calls)
* Werkzeug (To hash passwords)
* (pytz planned to be implmented alongside the reviews feature for tracking time)

## To run the program
First clone the repository,
Create a virtual environment, as seen <a href="https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/">here</a>.
Run the following command in the project path to download the dependencies: 
```bash
pip install -r requirements.txt
````
Create a file called "sensitive.env" in the root of the repository. Do not share this!. In the .env file, type JWT_SECRET={your key}, the key will be used for encrypting the JWT tokens.
To initialize the database, run the program once to create the db file, then type:
```bash
sqlite3 swift_market.db
````
* To create the tables
```bash
.read create.sql
````
* To populate the DB with dummy data for testing
```bash
.read populateDB.sql
````
If you followed all the steps, the program should run correctly. If not please contact me for help!

## API endpoints (Using Postman or similar for ease of access is recommended)

* For vendor related actions
* POST /api/vendors Registers a new vendor. Sample input:
>{
    "username": "New Vendor",
    "password": "123",
    "display_name": "Cool Vendor",
    "description": "A nice vendor that sells many things",
    "contact_info": "+1111111"
}
>
Sample Output:
>{
    "status": "success"
}

* POST /api/token To login and get an access token. Sample input:
>{
    "username": "New Vendor",
    "password": "123",
}

>
Sample Output:
>{
    "access_token": "eıxc9sSB9S9Nsamoasqbe8a9s9199bas..."
}

* GET /api/vendors/{id} Gets information about a specific vendor. Sample output:
>{
    "contact_info": "techhaven@example.com",
    "description": "Your one-stop shop for the latest gadgets.",
    "store_name": "Tech Haven Electronics"
}

* PUT /api/vendors/{id}/update Updates the vendors information. JWT required. Sample input:
> {
>   "display_name: "Store name",
>   "description": "Cool store description",
>   "contact_info": "something@example.com"
> }

Sample outputs:
> {'error': 'not authorized to edit other vendors'}
> {'error': f'missing field: {field}'}
> {'status': 'success'}

GET /api/vendors/{id}/items To view all the items of a vendor. JWT required. Sample output:
> {
    "items": [
        {
            "item_id": 1,
            "item_name": "Laptop Pro",
            "price": 1200,
            "stock": 10,
            "vendor_id": 1
        },
>       {
            "item_id": 2,
            "item_name": "Wireless Mouse",
            "price": 25,
            "stock": 25,
            "vendor_id": 1
        },
>       {
            "item_id": 3,
            "item_name": "Bluetooth Headphones",
            "price": 75,
            "stock": 15,
            "vendor_id": 1
        },
>       {
            "item_id": 4,
            "item_name": "4K Monitor",
            "price": 300,
            "stock": 8,
            "vendor_id": 1
        },
>       {
            "item_id": 7,
            "item_name": "Smartwatch",
            "price": 150,
            "stock": 18,
            "vendor_id": 1
        },
>       {
            "item_id": 10,
            "item_name": "VR Headset",
            "price": 400,
            "stock": 5,
            "vendor_id": 1
        }
    ],
    "vendor_id": 1
}

* For item related actions
* POST /api/items Create a new item under vendor. JWT Required. Sample input:
> {
    "item_name": "New item",
    "stock": 50,
    "price": 10
}

Sample Output: 
> {
    "status": "success"
}

* GET /api/items/{id} To see an items details. JWT Required. Sample output:
> {
    "item_id": 1,
    "item_name": "Laptop Pro",
    "price": 1200,
    "stock": 10,
    "vendor_id": 1
}

* DELETE /api/items/{id}/delete To delete an item. Sample outputs:
> {"status": "success"}
> 
> {'error': 'item not found, it may not belong to you'}
