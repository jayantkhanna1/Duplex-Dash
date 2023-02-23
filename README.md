This is a web application for listing houses that are available for rent or sale. The application is built using the Django web framework.

<h2>Features</h2>

<li>Users can sign up, log in, and log out of the application.
<li>Users can add a house listing, edit and delete their own house listings.
<li>Users can view all available house listings.
<li>Users can filter house listings by various criteria such as location, price, and house type.
<li>Admin users can manage all house listings and user accounts.<br/>


<h2>Installation</h2>
Clone the repository to your local machine using the command:

bash
Copy code
git clone   
Install the required Python dependencies using the command:

Copy code
pip install -r requirements.txt
Set up the database by running the following commands:

Copy code
python manage.py makemigrations
python manage.py migrate
Create a superuser account to access the admin panel:

Copy code
python manage.py createsuperuser
Run the development server using the command:

Copy code
python manage.py runserver
Access the web application in your browser at http://localhost:8000

<h2>Usage</h2>
<li>Create an account or log in to an existing account.
<li>Add a house listing by clicking on the "Add Listing" button and filling in the required details.
<li>View all available house listings by clicking on the "View Listings" button.
<li>Filter house listings by various criteria using the filters on the listings page.
<li>Edit or delete your own house listings by clicking on the corresponding buttons on the listings page.
<li>Admin users can manage all house listings and user accounts from the admin panel at http://localhost:8000/admin.

<h2>Contributing</h2>
Contributions are welcome! Please open an issue or submit a pull request with any features, bug fixes, or improvements.
