import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

class AddPurchase:
    def __init__(self, root, current_user, back_callback):
        self.root = root
        self.current_user = current_user
        self.back_callback = back_callback
        self.root.title("PharmaCare - Add Purchase")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")  
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()
        self.create_form()

    def create_form(self):
        # Main frame for centered layout
        main_frame = tk.Frame(self.root, bg="#ed79a9")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(main_frame, text="Add Purchase", font=("Arial", 16, "bold"), 
                 bg="#ed79a9", fg="#000000").grid(row=0, column=0, columnspan=2, pady=20)

        # Form fields in grid layout
        tk.Label(main_frame, text="Item", font=("Arial", 12), 
                 bg="#ed79a9", fg="#000000").grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.item_var = tk.StringVar()
        self.item_menu = ttk.OptionMenu(main_frame, self.item_var, "")
        self.item_menu.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Style for OptionMenu
        style = ttk.Style()
        style.configure("TMenubutton", font=("Arial", 12), background="#ffffff",
                        foreground="#000000", padding=5)

        self.load_items()

        tk.Label(main_frame, text="Quantity Purchased", font=("Arial", 12), 
                 bg="#ed79a9", fg="#000000").grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.quantity_entry = tk.Entry(main_frame, width=30, font=("Arial", 12),
                                       bd=2, relief="groove", bg="#ffffff", 
                                       highlightthickness=1, highlightcolor="#4CAF50")
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        # Button frame
        button_frame = tk.Frame(main_frame, bg="#ed79a9")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        # Buttons with different colors and borders
        tk.Button(button_frame, text="Save Purchase", command=self.save_purchase, 
                  bg="#4CAF50", fg="white", font=("Arial", 12),
                  width=12, bd=3, relief="raised", highlightthickness=2,
                  highlightbackground="#2196F3").grid(row=0, column=0, padx=5, pady=5)

        tk.Button(button_frame, text="View Purchases", command=self.view_purchases,
                  bg="#2196F3", fg="white", font=("Arial", 12),
                  width=12, bd=3, relief="raised", highlightthickness=2,
                  highlightbackground="#FF9800").grid(row=0, column=1, padx=5, pady=5)

        tk.Button(button_frame, text="Back to Dashboard", command=self.back_callback,
                  bg="#F44336", fg="white", font=("Arial", 12),
                  width=15, bd=3, relief="raised", highlightthickness=2,
                  highlightbackground="#4CAF50").grid(row=0, column=2, padx=5, pady=5)

    def load_items(self):
        self.cursor.execute("SELECT item_id, item_name, cost_price FROM MedicalItems")
        items = self.cursor.fetchall()
        item_names = [item[1] for item in items]
        self.item_dict = {item[1]: (item[0], item[2]) for item in items}  # item_id, cost_price
        menu = self.item_menu["menu"]
        menu.delete(0, "end")
        for name in item_names:
            menu.add_command(label=name, command=lambda value=name: self.item_var.set(value))
        if item_names:
            self.item_var.set(item_names[0])

    def save_purchase(self):
        item_name = self.item_var.get()
        quantity = self.quantity_entry.get()

        if not all([item_name, quantity]):
            messagebox.showerror("Error", "Item and Quantity are required")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Quantity must be positive")

            item_id, cost_price = self.item_dict.get(item_name)
            total_cost = quantity * cost_price
            purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insert purchase
            self.cursor.execute('''
                INSERT INTO Purchases (item_id, user_id, quantity_purchased, purchase_date, total_cost)
                VALUES (?, ?, ?, ?, ?)
            ''', (item_id, self.current_user['user_id'], quantity, purchase_date, total_cost))

            # Update stock quantity
            self.cursor.execute('''
                UPDATE MedicalItems SET stock_quantity = stock_quantity + ?
                WHERE item_id = ?
            ''', (quantity, item_id))

            self.conn.commit()
            messagebox.showinfo("Success", "Purchase added and stock updated successfully")
            self.clear_form()
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save purchase: {e}")

    def clear_form(self):
        self.quantity_entry.delete(0, tk.END)
        self.load_items()

    def view_purchases(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from view_purchase import ViewPurchases
        ViewPurchases(self.root, self.current_user, self.back_callback)

    def __del__(self):
        self.conn.close()
