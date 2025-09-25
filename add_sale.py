import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class AddSale:
    def __init__(self, root, current_user, back_callback, item_id=None):
        self.root = root
        self.current_user = current_user
        self.back_callback = back_callback
        self.item_id = item_id

        # Window setup
        self.root.title("PharmaCare - Add Sale")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")  

        # DB connection
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()

        # Create form UI
        self.create_form()

    def create_form(self):
        # Main container
        container = tk.Frame(self.root, bg="white", bd=5, relief="ridge")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(container, text="Add Sale", font=("Arial", 18, "bold"),
                 bg="white", fg="#000000").grid(row=0, column=0, columnspan=2, pady=15)

        # Item Dropdown
        tk.Label(container, text="Item:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.item_var = tk.StringVar()
        self.item_menu = tk.OptionMenu(container, self.item_var, "")
        self.item_menu.config(font=("Arial", 12), bg="#f0f0f0")
        self.item_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Stock label
        tk.Label(container, text="Available Stock:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.stock_label = tk.Label(container, text="Select an item", font=("Arial", 12), bg="white")
        self.stock_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Quantity entry with border
        tk.Label(container, text="Quantity Sold:", font=("Arial", 12), bg="white").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.quantity_entry = tk.Entry(container, width=30, font=("Arial", 12),
                                       bd=3, relief="solid", highlightthickness=1,
                                       highlightbackground="#4CAF50")
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=5)

        # Total Amount
        tk.Label(container, text="Total Amount:", font=("Arial", 12), bg="white").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.total_amount_label = tk.Label(container, text="0.00", font=("Arial", 12), bg="white")
        self.total_amount_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Button frame
        button_frame = tk.Frame(container, bg="white")
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)

        # Buttons with colors
        tk.Button(button_frame, text="Calculate Total", command=self.calculate_total,
                  bg="#4CAF50", fg="white", font=("Arial", 12), width=14, bd=3, relief="raised").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Save Sale", command=self.save_sale,
                  bg="#2196F3", fg="white", font=("Arial", 12), width=14, bd=3, relief="raised").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="View Items", command=self.view_items,
                  bg="#FF9800", fg="white", font=("Arial", 12), width=14, bd=3, relief="raised").grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Back to Dashboard", command=self.back_callback,
                  bg="#F44336", fg="white", font=("Arial", 12), width=16, bd=3, relief="raised").grid(row=0, column=3, padx=5)

        # Load items after widgets
        self.load_items()

        # Bind item selection
        self.item_var.trace("w", self.update_stock_label)

    def load_items(self):
        self.cursor.execute("SELECT item_id, item_name, unit_price, stock_quantity FROM MedicalItems")
        items = self.cursor.fetchall()
        self.item_dict = {item[1]: (item[0], item[2], item[3]) for item in items}

        menu = self.item_menu["menu"]
        menu.delete(0, "end")

        for name in self.item_dict.keys():
            menu.add_command(label=name, command=lambda value=name: self.item_var.set(value))

        if self.item_dict:
            if self.item_id:
                self.cursor.execute("SELECT item_name FROM MedicalItems WHERE item_id = ?", (self.item_id,))
                result = self.cursor.fetchone()
                if result:
                    self.item_var.set(result[0])
            else:
                first_item = list(self.item_dict.keys())[0]
                self.item_var.set(first_item)
            self.update_stock_label()

    def update_stock_label(self, *args):
        item_name = self.item_var.get()
        if item_name in self.item_dict:
            stock_quantity = self.item_dict[item_name][2]
            self.stock_label.config(text=f"{stock_quantity}")
            self.calculate_total()

    def calculate_total(self):
        item_name = self.item_var.get()
        quantity = self.quantity_entry.get()
        if not quantity:
            self.total_amount_label.config(text="0.00")
            return
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            if item_name in self.item_dict:
                unit_price = self.item_dict[item_name][1]
                total_amount = quantity * unit_price
                self.total_amount_label.config(text=f"{total_amount:.2f}")
        except ValueError:
            self.total_amount_label.config(text="0.00")
            messagebox.showerror("Error", "Invalid quantity")

    def save_sale(self):
        item_name = self.item_var.get()
        quantity = self.quantity_entry.get()

        if not all([item_name, quantity]):
            messagebox.showerror("Error", "Item and Quantity are required")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            item_id, unit_price, stock_quantity = self.item_dict.get(item_name)
            if quantity > stock_quantity:
                raise ValueError(f"Cannot sell {quantity}; only {stock_quantity} available")

            total_amount = quantity * unit_price
            sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insert sale
            self.cursor.execute('''
                INSERT INTO Sales (item_id, user_id, quantity_sold, sale_date, total_amount)
                VALUES (?, ?, ?, ?, ?)
            ''', (item_id, self.current_user['user_id'], quantity, sale_date, total_amount))

            # Update stock
            self.cursor.execute('''
                UPDATE MedicalItems SET stock_quantity = stock_quantity - ?
                WHERE item_id = ?
            ''', (quantity, item_id))

            self.conn.commit()
            messagebox.showinfo("Success", "Sale added and stock updated successfully")
            self.clear_form()

        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save sale: {e}")

    def clear_form(self):
        self.quantity_entry.delete(0, tk.END)
        self.total_amount_label.config(text="0.00")
        self.item_id = None
        self.load_items()

    def view_items(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.back_callback()

    def __del__(self):
        self.conn.close()
