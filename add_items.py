import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
import os
import shutil
from datetime import datetime, date


class AddItems:
    def __init__(self, root, current_user, back_callback):
        self.root = root
        self.current_user = current_user
        self.back_callback = back_callback
        self.root.title("PharmaCare - Add/Edit Item")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")  
        self.conn = sqlite3.connect("pharmacy.db")
        self.cursor = self.conn.cursor()
        self.item_id = None
        self.image_path = None
        self.items_folder = "items"

        # Create items folder if it doesn't exist
        if not os.path.exists(self.items_folder):
            os.makedirs(self.items_folder)

        self.create_form()

    def create_form(self):
        # Main frame for centered layout
        main_frame = tk.Frame(self.root, bg="#ed79a9")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(
            main_frame,
            text="Add/Edit Item",
            font=("Arial", 16, "bold"),
            bg="#ed79a9",
            fg="#000000",
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Item Name
        tk.Label(
            main_frame,
            text="Item Name",
            font=("Arial", 12),
            bg="#ed79a9",
            fg="#000000",
        ).grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.item_name_entry = tk.Entry(
            main_frame,
            width=30,
            font=("Arial", 12),
            bd=2,
            relief="groove",
            bg="#ffffff",
            highlightthickness=1,
            highlightcolor="#4CAF50",
        )
        self.item_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Category (using Combobox instead of OptionMenu)
        tk.Label(
            main_frame,
            text="Category",
            font=("Arial", 12),
            bg="#ed79a9",
            fg="#000000",
        ).grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(
            main_frame,
            textvariable=self.category_var,
            font=("Arial", 12),
            width=27,
            state="readonly",
        )
        self.category_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.load_categories()

        # Description
        tk.Label(
            main_frame,
            text="Description",
            font=("Arial", 12),
            bg="#ed79a9",
            fg="#000000",
        ).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.description_entry = tk.Entry(
            main_frame,
            width=30,
            font=("Arial", 12),
            bd=2,
            relief="groove",
            bg="#ffffff",
            highlightthickness=1,
            highlightcolor="#4CAF50",
        )
        self.description_entry.grid(row=3, column=1, padx=10, pady=5)

        # Unit Price
        tk.Label(
            main_frame,
            text="Unit Price",
            font=("Arial", 12),
            bg="#ed79a9",
            fg="#000000",
        ).grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.unit_price_entry = tk.Entry(
            main_frame,
            width=30,
            font=("Arial", 12),
            bd=2,
            relief="groove",
            bg="#ffffff",
            highlightthickness=1,
            highlightcolor="#4CAF50",
        )
        self.unit_price_entry.grid(row=4, column=1, padx=10, pady=5)

        # Cost Price
        tk.Label(
            main_frame,
            text="Cost Price",
            font=("Arial", 12),
            bg="#ed79a9",
            fg="#000000",
        ).grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.cost_price_entry = tk.Entry(
            main_frame,
            width=30,
            font=("Arial", 12),
            bd=2,
            relief="groove",
            bg="#ffffff",
            highlightthickness=1,
            highlightcolor="#4CAF50",
        )
        self.cost_price_entry.grid(row=5, column=1, padx=10, pady=5)

        # Stock Quantity
        tk.Label(
            main_frame,
            text="Stock Quantity",
            font=("Arial", 12),
            bg="#ed79a9",
            fg="#000000",
        ).grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.stock_quantity_entry = tk.Entry(
            main_frame,
            width=30,
            font=("Arial", 12),
            bd=2,
            relief="groove",
            bg="#ffffff",
            highlightthickness=1,
            highlightcolor="#4CAF50",
        )
        self.stock_quantity_entry.grid(row=6, column=1, padx=10, pady=5)

        # Expiry Date
        tk.Label(
            main_frame,
            text="Expiry Date",
            font=("Arial", 12),
            bg="#ed79a9",
            fg="#000000",
        ).grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.expiry_date_entry = DateEntry(
            main_frame,
            date_pattern="yyyy-mm-dd",
            font=("Arial", 12),
            background="#ffffff",
            foreground="#000000",
            borderwidth=2,
            relief="groove",
            selectbackground="#4CAF50",
        )
        self.expiry_date_entry.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        # Item Image
        tk.Label(
            main_frame,
            text="Item Image",
            font=("Arial", 12),
            bg="#ed79a9",
            fg="#000000",
        ).grid(row=8, column=0, sticky="w", padx=10, pady=5)
        tk.Button(
            main_frame,
            text="Upload Image",
            command=self.upload_image,
            bg="#FFC107",
            fg="white",
            font=("Arial", 12),
            width=12,
            bd=3,
            relief="raised",
            highlightthickness=2,
            highlightbackground="#2196F3",
        ).grid(row=8, column=1, padx=10, pady=5, sticky="w")
        self.image_label = tk.Label(
            main_frame,
            text="No image selected",
            font=("Arial", 12),
            bg="#ed79a9",
            fg="#000000",
        )
        self.image_label.grid(row=9, column=0, columnspan=2, pady=5)

        # Button frame
        button_frame = tk.Frame(main_frame, bg="#ed79a9")
        button_frame.grid(row=10, column=0, columnspan=2, pady=20)

        tk.Button(
            button_frame,
            text="Save Item",
            command=self.save_item,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
            width=12,
            bd=3,
            relief="raised",
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="View Items",
            command=self.view_items,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12),
            width=12,
            bd=3,
            relief="raised",
        ).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(
            button_frame,
            text="Back to Dashboard",
            command=self.back_callback,
            bg="#F44336",
            fg="white",
            font=("Arial", 12),
            width=15,
            bd=3,
            relief="raised",
        ).grid(row=0, column=2, padx=5, pady=5)

    def load_categories(self):
        self.cursor.execute("SELECT category_id, category_name FROM ItemCategories")
        categories = self.cursor.fetchall()
        category_names = [cat[1] for cat in categories]
        self.category_dict = {cat[1]: cat[0] for cat in categories}

        self.category_menu["values"] = category_names
        if category_names:
            self.category_var.set(category_names[0])

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            filename = f"item_{os.path.basename(file_path)}"
            dest_path = os.path.join(self.items_folder, filename)
            shutil.copy(file_path, dest_path)
            self.image_path = dest_path
            self.image_label.config(text=f"Selected: {filename}")

    def load_item(self, item_id):
        self.item_id = item_id
        self.cursor.execute(
            """SELECT item_name, category_id, description, unit_price, cost_price, 
                      stock_quantity, expiry_date, item_image 
               FROM MedicalItems WHERE item_id = ?""",
            (item_id,),
        )
        item = self.cursor.fetchone()
        if not item:
            return

        self.item_name_entry.delete(0, tk.END)
        self.item_name_entry.insert(0, item[0])

        self.cursor.execute(
            "SELECT category_name FROM ItemCategories WHERE category_id = ?", (item[1],)
        )
        cat_row = self.cursor.fetchone()
        self.category_var.set(cat_row[0] if cat_row else "")

        self.description_entry.delete(0, tk.END)
        if item[2]:
            self.description_entry.insert(0, item[2])

        self.unit_price_entry.delete(0, tk.END)
        self.unit_price_entry.insert(0, str(item[3] if item[3] is not None else ""))

        self.cost_price_entry.delete(0, tk.END)
        self.cost_price_entry.insert(0, str(item[4] if item[4] is not None else ""))

        self.stock_quantity_entry.delete(0, tk.END)
        self.stock_quantity_entry.insert(0, str(item[5] if item[5] is not None else ""))

        expiry_val = item[6]
        expiry_dt = None
        if expiry_val:
            if isinstance(expiry_val, str):
                for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d-%m-%Y", "%m/%d/%Y"):
                    try:
                        expiry_dt = datetime.strptime(expiry_val, fmt).date()
                        break
                    except ValueError:
                        continue
            elif isinstance(expiry_val, (datetime, date)):
                expiry_dt = expiry_val if isinstance(expiry_val, date) else expiry_val.date()

        if expiry_dt:
            self.expiry_date_entry.set_date(expiry_dt)
        else:
            self.expiry_date_entry.set_date(datetime.today().date())

        self.image_path = item[7]
        self.image_label.config(
            text=f"Selected: {os.path.basename(self.image_path) if self.image_path else 'No image'}"
        )

    def save_item(self):
        item_name = self.item_name_entry.get()
        category_name = self.category_var.get()
        description = self.description_entry.get()
        unit_price = self.unit_price_entry.get()
        cost_price = self.cost_price_entry.get()
        stock_quantity = self.stock_quantity_entry.get()
        expiry_date_obj = self.expiry_date_entry.get_date()

        if not all([item_name, category_name, unit_price, cost_price, stock_quantity]):
            messagebox.showerror(
                "Error",
                "Required fields: Item Name, Category, Unit Price, Cost Price, Stock Quantity",
            )
            return

        expiry_date_str = expiry_date_obj.strftime("%Y-%m-%d")

        try:
            unit_price = float(unit_price)
            cost_price = float(cost_price)
            stock_quantity = int(stock_quantity)

            category_id = self.category_dict.get(category_name)

            if self.item_id:
                self.cursor.execute(
                    """UPDATE MedicalItems 
                       SET item_name = ?, category_id = ?, description = ?, 
                           unit_price = ?, cost_price = ?, stock_quantity = ?, 
                           expiry_date = ?, item_image = ?
                       WHERE item_id = ?""",
                    (
                        item_name,
                        category_id,
                        description,
                        unit_price,
                        cost_price,
                        stock_quantity,
                        expiry_date_str,
                        self.image_path,
                        self.item_id,
                    ),
                )
                messagebox.showinfo("Success", "Item updated successfully")
            else:
                self.cursor.execute(
                    """INSERT INTO MedicalItems 
                       (item_name, category_id, description, unit_price, cost_price, 
                        stock_quantity, expiry_date, item_image)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        item_name,
                        category_id,
                        description,
                        unit_price,
                        cost_price,
                        stock_quantity,
                        expiry_date_str,
                        self.image_path,
                    ),
                )
                messagebox.showinfo("Success", "Item added successfully")

            self.conn.commit()
            self.clear_form()
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {str(ve)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save item: {e}")

    def clear_form(self):
        self.item_id = None
        self.item_name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.unit_price_entry.delete(0, tk.END)
        self.cost_price_entry.delete(0, tk.END)
        self.stock_quantity_entry.delete(0, tk.END)
        self.expiry_date_entry.set_date(datetime.today().date())
        self.image_path = None
        self.image_label.config(text="No image selected")
        self.load_categories()

    def view_items(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from view_items import ViewItems

        ViewItems(self.root, self.current_user, self.back_callback)

    def __del__(self):
        self.conn.close()
