Inventory & Sales Management System

A command-line Inventory & Sales Management System built with **Python** and **SQLite**. The project allows a small business to manage products, monitor stock levels, record sales, track inventory value, and review sales history from a simple terminal-based interface.

This project was built as a practical Python and SQL project to demonstrate how a real-world application can connect Python programming logic with a relational database.



Project Overview

Managing products manually can become difficult as the number of products and sales increases.

This system provides a simple way to:

* Add new products
* View available products
* Search for products
* Update product prices
* Delete products
* Restock products
* Record customer purchases
* Automatically reduce stock after a sale
* View sales history
* Generate an inventory report
* Identify products with low stock

The application uses SQLite to permanently store product and sales information.



 Features


1. Add Product

Users can add a new product by providing:

* Product name
* Product category
* Unit price
* Quantity in stock

The system validates the information before saving it to the database.



2. View Products

Displays all products currently stored in the inventory.

The information includes:

* Product ID
* Product name
* Category
* Unit price
* Quantity in stock

The output is formatted into a readable table in the terminal.


3. Search Product

Users can search for products by entering part or all of a product name.

The search uses SQL's `LIKE` operator to find matching products.

Example:
Search Word: laptop

The system can find products such as:

Laptop
Gaming Laptop
Laptop Stand
Laptop Bag




4. Update Product

The system allows users to update the price of an existing product.

The product is first identified from the database and its price can then be changed.


5. Delete Product

Users can remove an existing product from the inventory by providing its product name.

The system checks whether the product exists before attempting to delete it.


6. Restock Product

When inventory levels become low, users can add additional quantities to an existing product.

For example:

Current stock: 10
Restocked: 20
New stock: 30


The system updates the quantity directly in the database.



 7. Sell Product

The sales feature records customer purchases.

When a sale is made, the system:

1. Identifies the product.
2. Checks the available stock.
3. Checks that the requested quantity is valid.
4. Calculates the total selling price.
5. Records the sale.
6. Automatically decreases the product's stock.

For example:

Product price: $50
Quantity sold: 3

Total price = $50 × 3
            = $150

The inventory is then reduced by 3 units.



8. Sales History

The system keeps a record of previous sales.

The sales history contains:

* Sales ID
* Customer name
* Product sold
* Product ID
* Quantity sold
* Total price

This provides a basic transaction history for the business.



9. Inventory Report

The inventory report provides a quick summary of the current inventory.

It calculates:

* Total number of products
* Total units in stock
* Total inventory value

The inventory value is calculated using:

Unit Price × Quantity in Stock



10. Low Stock Report

The system identifies products whose inventory has reached or fallen below the low-stock threshold.

The current threshold is:
5 units

This makes it easier to identify products that may need to be restocked.







Technologies Used

* Python
* SQLite
* SQL





Python Concepts Used

This project demonstrates several important Python concepts:

* Functions
* while loops
* if / elif / else
* try / except
* User input
* String formatting
* Variables
* Tuples
* Lists
* Database connections
* Exception handling
* SQL queries
* Functions communicating through shared data
* Input validation




SQL Concepts Used

The project also demonstrates practical SQL concepts including:

* CREATE TABLE
* INSERT
* SELECT
* UPDATE
* DELETE
* WHERE
* LIKE
* COUNT()
* SUM()
* PRIMARY KEY
* FOREIGN KEY
* Parameterized queries
* Basic table relationships





Database Structure

The application uses an SQLite database called:
Products.db


The database contains two main tables;

Product Table

| Column            | Description                |
| ----------------- | -------------------------- |
| id                | Unique product ID          |
| product_name      | Name of the product        |
| category          | Product category           |
| unit_price        | Price of one unit          |
| quantity_in_stock | Current inventory quantity |



Sales Table


| Column        | Description                 |
| ------------- | --------------------------- |
| id            | Unique sales transaction ID |
| customer_name | Name of the customer        |
| sold_product  | Name of the product sold    |
| product_id    | ID of the product           |
| quantity_sold | Number of units sold        |
| price         | Total price of the sale     |

The product_id column connects the sales table to the product table through a foreign key relationship.

Conceptually:


product_table
      |
      | product_id
      |
      ↓
sales_table


This allows sales transactions to be associated with the products being sold.



How the System Works

The application starts with a main menu that allows the user to select an operation.


================== CHOOSE AN OPTION ==================

1. Add Product
2. View Products
3. Search Product
4. Update Product
5. Delete Product
6. Restock Product
7. Sell Product
8. Sales History
9. Inventory Report
10. Low Stock Report
11. Exit


The user selects an option, and the corresponding Python function is executed.

For example:


User
  ↓
Main Menu
  ↓
Choose "Sell Product"
  ↓
sell_product()
  ↓
Check Product
  ↓
Check Stock
  ↓
Calculate Price
  ↓
Save Sale
  ↓
Reduce Inventory



Input Validation

The application includes validation to prevent invalid information from being entered.

For example, the system prevents:

* Empty product names
* Empty categories
* Negative prices
* Zero or negative selling quantities
* Negative inventory quantities
* Invalid numeric input
* Selling more products than are currently available

Example:
Enter product quantity in stock: -5

Product quantity cannot be negative

The user is then asked to enter a valid value.





Example Workflow

A typical workflow might look like this:

Step 1 — Add a Product

Product name: Laptop
Category: Electronics
Price: 750
Quantity: 20


The product is saved to the database.


Step 2 — Sell the Product

Customer name: John
Product: Laptop
Quantity: 2


The system calculates:
750 × 2 = 1500

The sale is recorded and inventory becomes:

20 - 2 = 18


Step 3 — Check Inventory

The inventory report can then show the updated number of units and inventory value.



Error Handling

The project uses Python's `try / except` structure to handle invalid user input.

For example, if a user is asked to enter a number but enters text:

Enter product price: abc


The program catches the `ValueError` instead of crashing.

The user receives an appropriate message and can try again.



Security and Data Handling

The project uses parameterized SQL querie when inserting user-provided values into the database.

For example:

cursor.execute(
    "SELECT id FROM product_table WHERE product_name = ?",
    (product_name,)
)

Using placeholders helps prevent user input from being directly inserted into SQL statements.




What I Learned From This Project

Building this project helped me understand how different parts of software development work together.

PYTHON
I practiced:

* Writing functions
* Creating program menus
* Using loops
* Handling exceptions
* Validating user input
* Working with variables and data structures

SQL
I practiced:

* Creating relational tables
* Inserting records
* Retrieving data
* Updating records
* Deleting records
* Filtering data
* Using aggregate functions
* Connecting related tables

SQLite
I learned how Python can communicate with a database using the built-in `sqlite3` module.



Future Improvements
This project can be expanded with additional features in the future, such as:

* User authentication
* Admin and employee accounts
* Multiple product categories
* Sales dates and timestamps
* Product suppliers
* Purchase orders
* Customer database
* Profit and revenue reports
* Daily, weekly, and monthly sales reports
* Better database normalization
* A graphical user interface
* A web-based version
* REST API integration
* Automated reporting
* Data visualization
* Unit tests
* Logging


Project Goal

The main goal of this project was to build a practical application rather than simply practice isolated Python or SQL commands.

It combines Python programming, SQL, SQLite, database relationships, input validation, error handling, and Git/GitHub into one small but functional business application.

This project represents a foundation that can be expanded into a larger inventory and sales management application.



Author
**Owolabi Adewale**

Built as a practical Python and SQL learning project.
