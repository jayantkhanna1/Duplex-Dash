# Introduction
This is a web application for listing houses that are available for rent or sale. The application is built using the Django web framework.

<br>
<h2>Features</h2>

<li>Users can sign up, log in, and log out of the application.
<li>Users can add a house listing, edit and delete their own house listings.
<li>Users can view all available house listings.
<li>Users can filter house listings by various criteria such as location, price, and house type.
<li>Admin users can manage all house listings and user accounts.<br/>
<li>Payments for Premium are handled using PesaPal. (More gateways will be included soon)<br/>
<li>All listings are approved by admin.<br/>
<li>Admin can add video of the listing property. (Option will be available to users in future)<br/>


<br>

<h2>Installation</h2>
1. Clone the repository to your local machine using the command:

```
git clone https://github.com/jayantkhanna1/Duplex-Dash.git
```
2. Install the required Python dependencies using the command:

```
pip install -r requirements.txt
```
3. Set up .env file

4. Set up the database by running the following commands:

```
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser account to access the admin panel:

```
python manage.py createsuperuser
```

6. Run the development server using the command:

```
python manage.py runserver
```

7. Access the web application in your browser at http://localhost:8000

<br>

## Usage
<li>Create an account or log in to an existing account.
<li>Add a house listing by clicking on the "Add Listing" button and filling in the required details.
<li>View all available house listings by clicking on the "View Listings" button.
<li>Filter house listings by various criteria using the filters on the listings page.
<li>Edit or delete your own house listings by clicking on the corresponding buttons on the listings page.
<li>Admin users can manage all house listings and user accounts from the admin panel at http://localhost:8000/admin.

<br>
<h2>Contributing</h2>
Contributions are welcome! Please open an issue or submit a pull request with any features, bug fixes, or improvements.

<br>
