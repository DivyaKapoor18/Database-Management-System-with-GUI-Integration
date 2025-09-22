import os
import cx_Oracle

dsn = cx_Oracle.makedsn(
    os.getenv("DB_HOST"),
    os.getenv("DB_PORT"),
    service_name=os.getenv("DB_SERVICE")
)

connection = cx_Oracle.connect(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    dsn=dsn
)

cur = conn.cursor()

# SQL Statements


# List of queries
queries = [
    # Add Merchandise to the Merchandise Table
    """
    INSERT INTO Merchandise (MerchID, MerchName, Price, Gender, Quantity, MerchSize, MerchType, Colour)
    VALUES (104, 'Shirt', 69.99, 'Male', 90, 'M', 'Shirt', 'Blue')
    """,
    
    # Delete a Transaction with TransactionID = 1
    """
    DELETE FROM Transaction 
    WHERE TransactionID = 1
    """,
    
    # Total Cart Amount Grouped by Customer ID
    """
    SELECT CustomerID AS "Customer ID", SUM(TotalAmount) AS "Total Cart Amount"
    FROM Cart
    GROUP BY CustomerID
    ORDER BY "Total Cart Amount" DESC
    """,
    
    # Retrieve Distinct Customer Names in Alphabetical Order
    """
    SELECT DISTINCT CustomerName AS "Customer Name"
    FROM Customer
    ORDER BY CustomerName
    """,
    
    # Retrieve Merchandise Ordered by Type and Stock Status
    """
    SELECT DISTINCT MerchName AS "Merchandise Name", MerchType AS "Type", 
        CASE WHEN Quantity > 0 THEN 'In Stock' ELSE 'Out of Stock' END AS "Status"
    FROM Merchandise
    ORDER BY MerchType, "Status"
    """,
    
    # List All Orders Placed by a Specific Customer
    """
    SELECT OrderID, PaymentMethod, ShippingAddress, Status, OrderDate, TotalAmount
    FROM Orders
    WHERE CustomerID = 2
    """,
    
    # Update Stock Quantity for a Specific Item
    """
    UPDATE Inventory
    SET Stocks = Stocks - 5
    WHERE MerchID = 101
    """,
    
    # Retrieve Merchandise Items Stored in Each Cart
    """
    SELECT CartMerchID AS "Cart Merchandise ID", CartID AS "Cart ID", MerchID AS "Merchandise ID"
    FROM Cart_Merchandise
    ORDER BY CartID
    """,
    
    # Group Transactions by Method and Type
    """
    SELECT TransactionMethod AS "Payment Method", TransactionType AS "Transaction Type", COUNT(*) AS "Number of Transactions"
    FROM Transaction
    GROUP BY TransactionMethod, TransactionType
    ORDER BY "Number of Transactions" DESC
    """,
    
    # Retrieve Merchandise That is Out of Stock
    """
    SELECT MerchName AS "Merchandise Name", Quantity AS "Stocks"
    FROM Merchandise
    WHERE Quantity = 0
    """,
    
    # Join Customer, Orders, and Transaction Tables
    """
    SELECT C.CustomerName, O.Status AS "Order Status", T.TransactionMethod, T.TransactionDate
    FROM Customer C
    JOIN Orders O ON C.CustomerID = O.CustomerID
    JOIN Transaction T ON O.OrderID = T.OrderID
    ORDER BY C.CustomerName, T.TransactionDate DESC
    """,
    
    # Retrieve Total Amount Spent and Merchandise Details
    """
    SELECT C.CustomerName, O.OrderID, M.MerchName, CM.Quantity, 
           SUM(M.Price * CM.Quantity) AS "Total Spent"
    FROM Customer C
    JOIN Orders O ON C.CustomerID = O.CustomerID
    JOIN Cart_Merchandise CM ON O.OrderID = CM.CartID
    JOIN Merchandise M ON CM.MerchID = M.MerchID
    GROUP BY C.CustomerName, O.OrderID, M.MerchName, CM.Quantity
    ORDER BY C.CustomerName
    """,
    
    # Retrieve Customer Names, Order IDs, Purchased Merchandise, and Shipping Addresses
    """
    SELECT C.CustomerName, O.OrderID, M.MerchName, M.Price, O.ShippingAddress
    FROM Customer C
    JOIN Orders O ON C.CustomerID = O.CustomerID
    JOIN Cart_Merchandise CM ON O.OrderID = CM.CartID
    JOIN Merchandise M ON CM.MerchID = M.MerchID
    ORDER BY C.CustomerName, O.OrderID
    """,
    
    # Create View: Customer Order Summary
    """
    CREATE VIEW CustomerOrderSummary AS
    SELECT C.CustomerName, O.OrderID, O.Status, O.TotalAmount
    FROM Customer C
    JOIN Orders O ON C.CustomerID = O.CustomerID
    """,
    
    # Create View: Transaction Summary
    """
    CREATE VIEW TransactionSummary AS
    SELECT T.TransactionID, C.CustomerName, O.OrderID, T.TransactionMethod, T.TransactionDate
    FROM Transaction T
    JOIN Orders O ON T.OrderID = O.OrderID
    JOIN Customer C ON O.CustomerID = C.CustomerID
    """,
    
    # Create View: Inventory Details
    """
    CREATE VIEW InventoryDetails AS
    SELECT M.MerchName, I.TotalSales, I.Stocks, I.Status
    FROM Merchandise M
    JOIN Inventory I ON M.MerchID = I.MerchID
    """
]
drop_table_statements = [
    "DROP TABLE Inventory CASCADE CONSTRAINTS",
    "DROP TABLE Transaction CASCADE CONSTRAINTS",
    "DROP TABLE Cart_Merchandise CASCADE CONSTRAINTS",
    "DROP TABLE Merchandise CASCADE CONSTRAINTS",
    "DROP TABLE Cart CASCADE CONSTRAINTS",
    "DROP TABLE Orders CASCADE CONSTRAINTS",
    "DROP TABLE Customer CASCADE CONSTRAINTS"
]

sql_create_statements = [
    """
   CREATE TABLE Customer (
       CustomerID NUMBER PRIMARY KEY,
       CustomerName VARCHAR2(100) NOT NULL,
       Email VARCHAR2(100) UNIQUE NOT NULL,
       Phone VARCHAR2(15),
       Address VARCHAR2(255)
   )
   """,
   """
   CREATE TABLE Cart (
       CartID NUMBER PRIMARY KEY,
       TotalAmount NUMBER(10, 2),
       CustomerID NUMBER,
       FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
   )
   """,
   """
   CREATE TABLE Merchandise (
       MerchID NUMBER PRIMARY KEY,
       MerchName VARCHAR2(100) NOT NULL,
       Price NUMBER(10, 2),
       Gender VARCHAR2(10),
       Quantity NUMBER,
       MerchSize VARCHAR2(10),
       MerchType VARCHAR2(50),
       Colour VARCHAR2(50)
   )
   """,
   """
   CREATE TABLE Cart_Merchandise (
       CartMerchID NUMBER PRIMARY KEY,
       CartID NUMBER REFERENCES Cart(CartID),
       MerchID NUMBER REFERENCES Merchandise(MerchID)
   )
   """,
   """
   CREATE TABLE Orders (
       OrderID NUMBER PRIMARY KEY,
       PaymentMethod VARCHAR2(50),
       ShippingAddress VARCHAR2(255),
       Status VARCHAR2(50),
       OrderDate DATE,
       TotalAmount NUMBER(10, 2),
       CustomerID NUMBER,
       FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
   )
   """,
   """
   CREATE TABLE Transaction (
       TransactionID NUMBER PRIMARY KEY,
       TransactionMethod VARCHAR2(50),
       TransactionType VARCHAR2(50),
       TransactionDate DATE,
       CustomerID NUMBER,
       OrderID NUMBER,
       FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
       FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
   )
   """,
   """
   CREATE TABLE Inventory (
       ItemID NUMBER,
       MerchID NUMBER,
       TotalSales NUMBER,
       Stocks NUMBER,
       OrgName VARCHAR2(100),
       TotalInventory NUMBER,
       Status VARCHAR2(50),
       CONSTRAINT PK_Inventory PRIMARY KEY (ItemID, MerchID),
       FOREIGN KEY (MerchID) REFERENCES Merchandise(MerchID)
   )
   """
]

sql_populate_statements = [
    """
  INSERT INTO Customer (CustomerID, CustomerName, Email, Phone, Address)
  VALUES (1, 'John Doe', 'john.doe@example.com', '123-456-7890', '123 Maple St, Toronto, ON, M1N 2P3')
  """,
  """
  INSERT INTO Customer (CustomerID, CustomerName, Email, Phone, Address)
  VALUES (2, 'Jane Smith', 'jane.smith@example.com', '098-765-4321', '456 Oak St, Ottawa, ON, K1A 0B1')
  """,
  """
  INSERT INTO Customer (CustomerID, CustomerName, Email, Phone, Address)
  VALUES (3, 'Alice Johnson', 'alice.johnson@example.com', '567-890-1234', '789 Birch St, Hamilton, ON, L8P 4X5')
  """,
  """
  INSERT ALL
      INTO Cart (CartID, TotalAmount, CustomerID) VALUES (1, 69.98, 1)
      INTO Cart (CartID, TotalAmount, CustomerID) VALUES (2, 49.99, 2)
      INTO Cart (CartID, TotalAmount, CustomerID) VALUES (3, 79.99, 3)
  SELECT 1 FROM DUAL
  """,
  """
  INSERT INTO Merchandise (MerchID, MerchName, Price, Gender, Quantity, MerchSize, MerchType, Colour)
  VALUES (101, 'T-shirt', 19.99, 'Unisex', 100, 'M', 'Clothing', 'Red')
  """,
  """
  INSERT INTO Merchandise (MerchID, MerchName, Price, Gender, Quantity, MerchSize, MerchType, Colour)
  VALUES (102, 'Jeans', 49.99, 'Unisex', 50, 'L', 'Clothing', 'Blue')
  """,
  """
  INSERT INTO Merchandise (MerchID, MerchName, Price, Gender, Quantity, MerchSize, MerchType, Colour)
  VALUES (103, 'Sneakers', 79.99, 'Unisex', 75, '10', 'Footwear', 'White')
  """,
  """
  INSERT ALL
      INTO Cart_Merchandise (CartMerchID, CartID, MerchID) VALUES (1, 1, 101)
      INTO Cart_Merchandise (CartMerchID, CartID, MerchID) VALUES (2, 1, 102)
      INTO Cart_Merchandise (CartMerchID, CartID, MerchID) VALUES (3, 2, 102)
      INTO Cart_Merchandise (CartMerchID, CartID, MerchID) VALUES (4, 3, 103)
  SELECT 1 FROM DUAL
  """,
  """
  INSERT ALL
      INTO Orders (OrderID, PaymentMethod, ShippingAddress, Status, OrderDate, TotalAmount, CustomerID) 
      VALUES (1, 'Credit Card', '123 Maple St, Toronto, ON', 'Shipped', TO_DATE('2024-09-01', 'YYYY-MM-DD'), 69.98, 1)
      INTO Orders (OrderID, PaymentMethod, ShippingAddress, Status, OrderDate, TotalAmount, CustomerID) 
      VALUES (2, 'PayPal', '456 Oak St, Ottawa, ON', 'Processing', TO_DATE('2024-09-05', 'YYYY-MM-DD'), 49.99, 2)
      INTO Orders (OrderID, PaymentMethod, ShippingAddress, Status, OrderDate, TotalAmount, CustomerID) 
      VALUES (3, 'Credit Card', '789 Birch St, Hamilton, ON', 'Delivered', TO_DATE('2024-09-10', 'YYYY-MM-DD'), 79.99, 3)
  SELECT 1 FROM DUAL
  """,
  """
  INSERT ALL
      INTO Transaction (TransactionID, TransactionMethod, TransactionType, TransactionDate, CustomerID, OrderID) 
      VALUES (1, 'Credit Card', 'Debit', TO_DATE('2024-09-01', 'YYYY-MM-DD'), 1, 1)
      INTO Transaction (TransactionID, TransactionMethod, TransactionType, TransactionDate, CustomerID, OrderID) 
      VALUES (2, 'PayPal', 'Debit', TO_DATE('2024-09-05', 'YYYY-MM-DD'), 2, 2)
      INTO Transaction (TransactionID, TransactionMethod, TransactionType, TransactionDate, CustomerID, OrderID) 
      VALUES (3, 'Credit Card', 'Debit', TO_DATE('2024-09-10', 'YYYY-MM-DD'), 3, 3)
  SELECT 1 FROM DUAL
  """,
  """
  INSERT ALL
      INTO Inventory (ItemID, MerchID, TotalSales, Stocks, OrgName, TotalInventory, Status) 
      VALUES (1, 101, 10, 90, 'Fashion Corp', 100, 'In Stock')
      INTO Inventory (ItemID, MerchID, TotalSales, Stocks, OrgName, TotalInventory, Status) 
      VALUES (2, 102, 5, 45, 'Denim Co.', 50, 'In Stock')
      INTO Inventory (ItemID, MerchID, TotalSales, Stocks, OrgName, TotalInventory, Status) 
      VALUES (3, 103, 3, 72, 'Footwear Inc.', 75, 'In Stock')
  SELECT 1 FROM DUAL
  """
]

# Helper Function to Execute Queries
def execute_query(query):
    try:
        cur.execute(query)
        if query.strip().upper().startswith("SELECT"):
            rows = cur.fetchall()
            result_window = tk.Toplevel(root)
            result_window.title("Query Results")
            tree = ttk.Treeview(result_window)
            tree.pack(expand=True, fill="both")

            # Get actual column names
            columns = [desc[0] for desc in cur.description]
            tree["columns"] = columns

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=150)

            # Insert data
            for row in rows:
                tree.insert("", "end", values=row)

        else:
            conn.commit()
            if not query.strip().upper().startswith(("DROP", "CREATE", "INSERT")):
                messagebox.showinfo("Success", "Query executed successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Functions for Menu Options
def drop_tables():
    try:
        for sql in drop_table_statements:
            execute_query(sql)
        messagebox.showinfo("Success", "All tables dropped successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_tables():
    try:
        for sql in sql_create_statements:
            execute_query(sql)
        messagebox.showinfo("Success", "All tables created successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def populate_tables():
    try:
        for sql in sql_populate_statements:
            execute_query(sql)
        messagebox.showinfo("Success", "All tables populated successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def custom_query_window():
    query_window = tk.Toplevel(root)
    query_window.title("Custom Query")

    tk.Label(query_window, text="Enter SQL Query:").pack(pady=10)
    query_text = tk.Text(query_window, height=10, width=50)
    query_text.pack()

    def run_custom_query():
        query = query_text.get("1.0", tk.END).strip()
        execute_query(query)

    tk.Button(query_window, text="Execute", command=run_custom_query).pack(pady=10)

def predefined_queries_window():
    predefined_window = tk.Toplevel(root)
    predefined_window.title("Predefined Queries")

    tk.Label(predefined_window, text="Select a Predefined Query:").pack(pady=10)

    # Dropdown menu for predefined queries
    query_var = tk.StringVar(predefined_window)
    query_var.set("Select Query")
    query_dropdown = ttk.Combobox(predefined_window, textvariable=query_var, width=80)
    query_dropdown["values"] = queries
    query_dropdown.pack(pady=10)

    def run_predefined_query():
        selected_query = query_var.get()
        if selected_query and selected_query != "Select Query":
            execute_query(selected_query)
        else:
            messagebox.showwarning("Warning", "Please select a query.")

    tk.Button(predefined_window, text="Execute Query", command=run_predefined_query).pack(pady=10)
    
def search_window():
    search_win = tk.Toplevel(root)
    search_win.title("Search Table")

    tk.Label(search_win, text="Select a Table:").pack(pady=10)
    
    # Dropdown for table selection
    table_var = tk.StringVar(search_win)
    tables = ["Customer", "Orders", "Cart", "Merchandise", "Transaction", "Cart_Merchandise", "Inventory"]  # Add tables here
    table_dropdown = ttk.Combobox(search_win, textvariable=table_var, values=tables, state="readonly")
    table_dropdown.pack(pady=5)

    def on_table_select():
        selected_table = table_var.get()
        if selected_table:
            # Fetch columns for the selected table
            try:
                cur.execute(f"SELECT column_name FROM user_tab_columns WHERE table_name = '{selected_table.upper()}'")
                columns = [row[0] for row in cur.fetchall()]
                if columns:
                    # Clear previous widgets
                    for widget in search_win.winfo_children():
                        if widget.winfo_class() != "TCombobox":
                            widget.destroy()

                    # Attribute dropdown
                    tk.Label(search_win, text=f"Select an Attribute from {selected_table}:").pack(pady=10)
                    attribute_var = tk.StringVar(search_win)
                    attribute_dropdown = ttk.Combobox(search_win, textvariable=attribute_var, values=columns, state="readonly")
                    attribute_dropdown.pack(pady=5)

                    # Entry for search value
                    tk.Label(search_win, text="Enter Value to Search:").pack(pady=10)
                    search_value_entry = tk.Entry(search_win)
                    search_value_entry.pack(pady=5)

                    def perform_search():
                        selected_attribute = attribute_var.get()
                        search_value = search_value_entry.get()
                        if selected_attribute and search_value:
                            query = f"SELECT * FROM {selected_table} WHERE {selected_attribute} LIKE '%{search_value}%'"
                            execute_query(query)
                        else:
                            messagebox.showwarning("Warning", "Please select an attribute and enter a value.")

                    tk.Button(search_win, text="Search", command=perform_search).pack(pady=10)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to retrieve attributes: {e}")

    # Add event binding to dropdown
    table_dropdown.bind("<<ComboboxSelected>>", lambda _: on_table_select())

def update_query_window():
    update_window = tk.Toplevel(root)
    update_window.title("Update Query")

    tk.Label(update_window, text="Select a Table:").pack(pady=5)
    
    # Dropdown for table selection
    table_var = tk.StringVar(update_window)
    table_dropdown = ttk.Combobox(update_window, textvariable=table_var, width=50)
    table_dropdown["values"] = ["Customer", "Cart", "Merchandise", "Cart_Merchandise", "Orders", "Transaction", "Inventory"]
    table_dropdown.pack(pady=5)

    def choose_attribute():
        selected_table = table_var.get()
        if not selected_table:
            messagebox.showwarning("Warning", "Please select a table first.")
            return

        # Fetch column names from the selected table
        try:
            cur.execute(f"SELECT * FROM {selected_table} WHERE ROWNUM = 1")
            columns = [desc[0] for desc in cur.description]

            # Display dropdown for attributes
            tk.Label(update_window, text="Select an Attribute to Update:").pack(pady=5)
            attr_var = tk.StringVar(update_window)
            attr_dropdown = ttk.Combobox(update_window, textvariable=attr_var, width=50)
            attr_dropdown["values"] = columns
            attr_dropdown.pack(pady=5)

            tk.Label(update_window, text="Enter New Value for the Attribute:").pack(pady=5)
            new_value_entry = tk.Entry(update_window, width=50)
            new_value_entry.pack(pady=5)

            tk.Label(update_window, text="Enter Condition (e.g., CustomerID = 1):").pack(pady=5)
            condition_entry = tk.Entry(update_window, width=50)
            condition_entry.pack(pady=5)

            def execute_update_query():
                attr = attr_var.get()
                new_value = new_value_entry.get()
                condition = condition_entry.get()

                if not attr or not new_value or not condition:
                    messagebox.showwarning("Warning", "Please fill in all fields.")
                    return

                # Construct and execute the update query
                try:
                    query = f"UPDATE {selected_table} SET {attr} = '{new_value}' WHERE {condition}"
                    execute_query(query)
                    messagebox.showinfo("Success", "Update query executed successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to execute update query: {str(e)}")

            tk.Button(update_window, text="Execute Update", command=execute_update_query).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch columns: {str(e)}")
            
    tk.Button(update_window, text="Choose Attribute", command=choose_attribute).pack(pady=10)

def delete_query_window():
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Query")

    tk.Label(delete_window, text="Select a Table:").pack(pady=5)
    
    # Dropdown for table selection
    table_var = tk.StringVar(delete_window)
    table_dropdown = ttk.Combobox(delete_window, textvariable=table_var, width=50)
    table_dropdown["values"] = ["Customer", "Cart", "Merchandise", "Cart_Merchandise", "Orders", "Transaction", "Inventory"]
    table_dropdown.pack(pady=5)

    tk.Label(delete_window, text="Enter Condition for Deletion (e.g., CustomerID = 1):").pack(pady=5)
    condition_entry = tk.Entry(delete_window, width=50)
    condition_entry.pack(pady=5)

    def execute_delete_query():
        selected_table = table_var.get()
        condition = condition_entry.get()

        if not selected_table or not condition:
            messagebox.showwarning("Warning", "Please select a table and provide a condition.")
            return

        # Construct and execute the delete query
        try:
            query = f"DELETE FROM {selected_table} WHERE {condition}"
            execute_query(query)
            messagebox.showinfo("Success", "Delete query executed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute delete query: {str(e)}")

    tk.Button(delete_window, text="Execute Delete", command=execute_delete_query).pack(pady=10)


def on_close():
    try:
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error while closing resources: {e}")
    root.destroy()

# Main GUI Window
root = tk.Tk()
root.title("Database Management System")

tk.Label(root, text="Database Operations", font=("Helvetica", 16)).pack(pady=10)

tk.Button(root, text="Drop Tables", command=drop_tables).pack(pady=5)
tk.Button(root, text="Create Tables", command=create_tables).pack(pady=5)
tk.Button(root, text="Populate Tables", command=populate_tables).pack(pady=5)
tk.Button(root, text="Custom Query", command=custom_query_window).pack(pady=5)
tk.Button(root, text="Predefined Queries", command=predefined_queries_window).pack(pady=5)
tk.Button(root, text="Search", command=search_window).pack(pady=5)
tk.Button(root, text="Update", command=update_query_window).pack(pady=5)
tk.Button(root, text="Delete", command=delete_query_window).pack(pady=5)
tk.Button(root, text="Exit", command=on_close).pack(pady=5)

root.mainloop()

# Close database connection


root.protocol("WM_DELETE_WINDOW", on_close)
