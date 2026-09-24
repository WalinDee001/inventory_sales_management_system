import sqlite3


# Connect to the SQLite database.
# If products.db does not exist, SQLite will create it automatically.
connection = sqlite3.connect("products.db")

# Enable foreign key enforcement in SQLite.
# This ensures that product_id relationships are properly maintained.
connection.execute("PRAGMA foreign_keys = ON")

# Create a cursor object for executing SQL queries.
cursor = connection.cursor()


# Create the product table if it does not already exist.
# This table stores the information about products currently in inventory.
cursor.execute("""
CREATE TABLE IF NOT EXISTS product_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    unit_price DECIMAL(15,2) NOT NULL,
    quantity_in_stock INTEGER NOT NULL
)
""")


# Create the sales table.
# product_id connects each sale to the corresponding product in product_table.
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    sold_product TEXT NOT NULL,
    product_id INTEGER NOT NULL,
    quantity_sold INTEGER NOT NULL,
    price DECIMAL(15,2) NOT NULL,
    FOREIGN KEY(product_id) REFERENCES product_table(id)
)
""")


def add_product():
    """Add a new product to the inventory."""

    # Ask for the product name and make sure it is not empty.
    while True:
        product_name = input("Product name: ").strip()

        if not product_name:
            print("Product name cannot be empty")
            continue

        break

    # Ask for the product category.
    while True:
        product_category = input("Enter product category: ").strip()

        if not product_category:
            print("Product category cannot be empty")
            continue

        break

    # Get and validate the product price.
    while True:
        try:
            product_price = float(input("Enter product price: "))

            if product_price <= 0:
                print("Product price cannot be zero or negative")
                continue

            break

        except ValueError:
            print("Invalid input. Enter a numeric value")

    # Get and validate the initial quantity in stock.
    # Quantity is an integer because products are sold as whole units.
    while True:
        try:
            product_quantity = int(
                input("Enter product quantity in stock: ")
            )

            if product_quantity < 0:
                print("Product quantity cannot be negative")
                continue

            break

        except ValueError:
            print("Invalid input. Input a numeric value")

    try:
        # Parameterized SQL prevents user input from being directly
        # inserted into the SQL statement.
        cursor.execute(
            """
            INSERT INTO product_table
            (product_name, category, unit_price, quantity_in_stock)
            VALUES (?, ?, ?, ?)
            """,
            (
                product_name,
                product_category,
                product_price,
                product_quantity
            )
        )

        # Save the changes permanently to the database.
        connection.commit()

        print("Product details saved successfully.")

    except sqlite3.IntegrityError:
        # This can occur if the product name already exists because
        # product_name has a UNIQUE constraint.
        print("Product name already exists.")

    return


def view_products():
    """Display all products in a readable table format."""

    product_list = cursor.execute(
        """
        SELECT id, product_name, category, unit_price, quantity_in_stock
        FROM product_table
        """
    ).fetchall()

    if product_list:
        print("=" * 90)
        print("                    PRODUCT LIST")
        print("=" * 90)

        # The < symbol left-aligns each value within the specified width.
        print(
            f"{'ID':<5}"
            f"{'PRODUCT_NAME':<30}"
            f"{'CATEGORY':<20}"
            f"{'UNIT_PRICE':<20}"
            f"{'QUANTITY_IN_STOCK':<20}"
        )

        print("_" * 90)

        for product_id, product_name, category, unit_price, quantity_in_stock in product_list:
            print(
                f"{product_id:<5}"
                f"{product_name:<30}"
                f"{category:<20}"
                f"₦{unit_price:<18,.2f}"
                f"{quantity_in_stock:<20}"
            )

        print("=" * 90)

    else:
        print("No product is available yet")

    return


def search_product():
    """Search for products using part of the product name."""

    while True:
        product_search = input("Enter Search Word: ").strip()

        # Validate the search input before querying the database.
        if not product_search:
            print("Product search cannot be empty. Enter a valid product name")
            continue

        # LIKE with % allows partial matches.
        # Example: searching for 'phone' can find 'iPhone 15'.
        product_like = cursor.execute(
            """
            SELECT *
            FROM product_table
            WHERE product_name LIKE ?
            """,
            (f"%{product_search}%",)
        ).fetchall()

        if product_like:
            print(f"These are the products matching your search: {product_like}")
        else:
            print("No product related to the search")

        break

    return


def update_product():
    """Update the price of an existing product."""

    while True:
        product_to_update = input("Enter product name: ").strip()

        # First find the product ID because the ID is used to update
        # the correct database record.
        selected_id = cursor.execute(
            """
            SELECT id
            FROM product_table
            WHERE product_name = ?
            """,
            (product_to_update,)
        ).fetchone()

        if selected_id:
            try:
                updated_unit_price = float(
                    input("Enter the new product price: ")
                )

                if updated_unit_price <= 0:
                    print("Price must be greater than zero")
                    continue

                cursor.execute(
                    """
                    UPDATE product_table
                    SET unit_price = ?
                    WHERE id = ?
                    """,
                    (updated_unit_price, selected_id[0])
                )

                connection.commit()

                print("Product new price successfully updated")

            except ValueError:
                print("Input invalid. Enter a numeric value")

        else:
            print("Product name unknown. Enter a correct product name.")

        break

    return


def delete_product():
    """Delete a product from the inventory."""

    product_to_delete = input(
        "Enter the product to delete: "
    ).strip()

    id_to_delete = cursor.execute(
        """
        SELECT id
        FROM product_table
        WHERE product_name = ?
        """,
        (product_to_delete,)
    ).fetchone()

    if id_to_delete:
        try:
            cursor.execute(
                "DELETE FROM product_table WHERE id = ?",
                (id_to_delete[0],)
            )

            connection.commit()

            print("Product successfully deleted")

        except sqlite3.IntegrityError:
            # A product that already has sales records cannot be deleted
            # while foreign key protection is enabled.
            print(
                "This product cannot be deleted because it has "
                "associated sales records."
            )

    else:
        print("Unknown Product")

    return


def restock_product():
    """Increase the quantity of an existing product."""

    while True:
        product_to_restock = input(
            "Enter product to restock: "
        ).strip()

        id_of_restocked = cursor.execute(
            """
            SELECT id
            FROM product_table
            WHERE product_name = ?
            """,
            (product_to_restock,)
        ).fetchone()

        if id_of_restocked:
            try:
                amount_restocked = int(
                    input("Enter the quantity to restock: ")
                )

                if amount_restocked <= 0:
                    print("New stock must be greater than zero")

                else:
                    cursor.execute(
                        """
                        UPDATE product_table
                        SET quantity_in_stock = quantity_in_stock + ?
                        WHERE id = ?
                        """,
                        (amount_restocked, id_of_restocked[0])
                    )

                    connection.commit()

                    print("New stock successfully added")

            except ValueError:
                print("Invalid input. Input a numeric value")

        else:
            print("Product unknown")

        break

    return


def sell_product():
    """Record a sale and reduce the product's inventory."""

    while True:
        try:
            customer_name = input(
                "Enter customer name: "
            ).strip()

            product_name = input(
                "Enter name of product sold: "
            ).strip()

            quantity_bought = int(
                input("Enter number of quantity bought: ")
            )

            # Retrieve the product's ID, price, and current stock.
            needed_for_sales = cursor.execute(
                """
                SELECT id, unit_price, quantity_in_stock
                FROM product_table
                WHERE product_name = ?
                """,
                (product_name,)
            ).fetchone()

            # A sale must contain at least one product.
            if quantity_bought <= 0:
                print(
                    "Quantity bought cannot be zero or less than zero"
                )
                continue

            # Customer name is required.
            if not customer_name:
                print("Customer name cannot be empty")
                continue

            # Check that the product exists and that enough stock is available.
            if needed_for_sales and quantity_bought <= needed_for_sales[2]:

                # Calculate the total price using the current unit price.
                total_price = needed_for_sales[1] * quantity_bought

                # Record the sale.
                cursor.execute(
                    """
                    INSERT INTO sales_table
                    (customer_name, sold_product, product_id,
                     quantity_sold, price)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        customer_name,
                        product_name,
                        needed_for_sales[0],
                        quantity_bought,
                        total_price
                    )
                )

                # Reduce the inventory by the quantity sold.
                cursor.execute(
                    """
                    UPDATE product_table
                    SET quantity_in_stock = quantity_in_stock - ?
                    WHERE id = ?
                    """,
                    (
                        quantity_bought,
                        needed_for_sales[0]
                    )
                )

                # Save both the sale and inventory update.
                connection.commit()

                print("Sales successful")

            else:
                print(
                    "Product name unknown or quantity requested "
                    "is more than quantity available"
                )

            break

        except ValueError:
            print("Invalid input. Input a numeric value")

    return


def sales_history():
    """Display all recorded sales."""

    sales_made = cursor.execute(
        """
        SELECT id, customer_name, sold_product,
               product_id, quantity_sold, price
        FROM sales_table
        """
    ).fetchall()

    if sales_made:
        print("=" * 150)
        print("                                      SALES HISTORY")
        print("=" * 150)

        print(
            f"{'SALES_ID':<12}"
            f"{'CUSTOMER_NAME':<30}"
            f"{'PRODUCT':<30}"
            f"{'PRODUCT_ID':<15}"
            f"{'QUANTITY_SOLD':<20}"
            f"{'TOTAL_PRICE':<10}"
        )

        print("_" * 150)

        for sales_id, customer_name, sold_product, product_id, quantity_sold, total_price in sales_made:
            print(
                f"{sales_id:<12}"
                f"{customer_name:<30}"
                f"{sold_product:<30}"
                f"{product_id:<15}"
                f"{quantity_sold:<20}"
                f"₦{total_price:<10,.2f}"
            )

        print("=" * 150)

    else:
        print("No sales made yet")

    return


def inventory_report():
    """Calculate and display basic inventory statistics."""

    # [0] extracts the actual value from the one-row tuple returned
    # by fetchone().
    total_products = cursor.execute(
        "SELECT COUNT(product_name) FROM product_table"
    ).fetchone()[0] or 0

    total_unit_in_stock = cursor.execute(
        "SELECT SUM(quantity_in_stock) FROM product_table"
    ).fetchone()[0] or 0

    total_inventory_value = cursor.execute(
        """
        SELECT SUM(unit_price * quantity_in_stock)
        FROM product_table
        """
    ).fetchone()[0] or 0

    print(
        f"""
This is the inventory report:

Total Products: {total_products}
Total Units in Stock: {total_unit_in_stock}
Total Inventory Value: ₦{total_inventory_value:,.2f}
"""
    )

    return


def low_stock():
    """Display all products whose stock is at or below five units."""

    low_stock_report = cursor.execute(
        """
        SELECT product_name, quantity_in_stock
        FROM product_table
        WHERE quantity_in_stock <= ?
        """,
        (5,)
    ).fetchall()

    if low_stock_report:
        for product_name, quantity in low_stock_report:
            print(
                f"{product_name} is low in stock "
                f"with only {quantity} units remaining"
            )

    else:
        print("All products have enough stock available")

    return


def main_menu():
    """Display the main menu and control the application flow."""

    while True:
        print("""
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
""")

        option = input("Choose an option: ").strip()

        if option == "1":
            add_product()

        elif option == "2":
            view_products()

        elif option == "3":
            search_product()

        elif option == "4":
            update_product()

        elif option == "5":
            delete_product()

        elif option == "6":
            restock_product()

        elif option == "7":
            sell_product()

        elif option == "8":
            sales_history()

        elif option == "9":
            inventory_report()

        elif option == "10":
            low_stock()

        elif option == "11":
            print("Goodbye!")
            break

        else:
            print("Invalid input. Please choose an option from 1 to 11.")


# Start the application.
main_menu()

