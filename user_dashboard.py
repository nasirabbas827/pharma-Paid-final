import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3, os
from PIL import Image, ImageTk


class UserDashboard:
    def __init__(self, root, user, logout_callback):
        self.root = root
        self.user = user
        self.logout_callback = logout_callback

        # Window setup
        self.root.title("PharmaCare - User Dashboard")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")

        # DB Connection
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()

        # Cache for image paths
        self.image_cache = {}

        # Build UI
        self.create_dashboard()

    def create_dashboard(self):
        # Container frame
        container = tk.Frame(self.root, bg="white", bd=5, relief="ridge")
        container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.9)

        # Title
        tk.Label(container, text=f"Welcome, {self.user['full_name']} (User)",
                 font=("Arial", 16, "bold"), bg="white", fg="#000").grid(row=0, column=0, columnspan=4, pady=15)

        # Search form row
        tk.Label(container, text="Search by ID or Name:", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.search_entry = tk.Entry(container, font=("Arial", 12), width=30, bd=3, relief="solid",
                                     highlightthickness=1, highlightbackground="#4CAF50")
        self.search_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Button(container, text="Search", command=self.search_items,
                  bg="#4CAF50", fg="white", font=("Arial", 12), width=12, bd=3, relief="raised").grid(row=1, column=2, padx=10, pady=5)
        tk.Button(container, text="Clear", command=lambda: self.load_items(),
                  bg="#FF9800", fg="white", font=("Arial", 12), width=12, bd=3, relief="raised").grid(row=1, column=3, padx=10, pady=5)

        # Table for items
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), foreground="black")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)

        self.tree = ttk.Treeview(container,
                                 columns=("ID", "Name", "Category", "Unit Price", "Stock", "Expiry Date", "Image"),
                                 show="headings")
        self.tree.grid(row=2, column=0, columnspan=4, padx=10, pady=15, sticky="nsew")

        container.grid_rowconfigure(2, weight=1)
        for i in range(4):
            container.grid_columnconfigure(i, weight=1)

        # Table headings
        self.tree.heading("ID", text="Item ID")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Unit Price", text="Unit Price")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Expiry Date", text="Expiry Date")
        self.tree.heading("Image", text="Image")

        # Column sizes
        self.tree.column("ID", width=70)
        self.tree.column("Name", width=150)
        self.tree.column("Category", width=120)
        self.tree.column("Unit Price", width=90)
        self.tree.column("Stock", width=90)
        self.tree.column("Expiry Date", width=110)
        self.tree.column("Image", width=110)

        # Load items
        self.load_items()

        # Buttons row
        button_frame = tk.Frame(container, bg="white")
        button_frame.grid(row=3, column=0, columnspan=4, pady=15)

        tk.Button(button_frame, text="Sale Now", command=self.sale_selected_item,
                  bg="#2196F3", fg="white", font=("Arial", 12), width=14, bd=3, relief="raised").grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="Logout", command=self.logout,
                  bg="#F44336", fg="white", font=("Arial", 12), width=14, bd=3, relief="raised").grid(row=0, column=1, padx=10)

        # Bind click for image preview
        self.tree.bind("<ButtonRelease-1>", self.handle_tree_click)

    def load_items(self, search_term=""):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = '''
            SELECT mi.item_id, mi.item_name, ic.category_name, mi.unit_price, 
                   mi.stock_quantity, mi.expiry_date, mi.item_image
            FROM MedicalItems mi
            JOIN ItemCategories ic ON mi.category_id = ic.category_id
        '''
        if search_term:
            query += " WHERE mi.item_id LIKE ? OR mi.item_name LIKE ?"
            self.cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        else:
            self.cursor.execute(query)

        for row in self.cursor.fetchall():
            item_id, item_name, category_name, unit_price, stock_quantity, expiry_date, item_image = row
            image_display = item_image.split('/')[-1] if item_image else "No image"
            self.tree.insert("", "end", values=(item_id, item_name, category_name, unit_price, stock_quantity, expiry_date, image_display))
            if item_image:
                self.image_cache[item_id] = item_image

    def handle_tree_click(self, event):
        item = self.tree.selection()
        if not item:
            return
        col = self.tree.identify_column(event.x)
        item_id = self.tree.item(item)["values"][0]
        if col == "#7" and item_id in self.image_cache:  # Image column
            self.show_image(item_id)

    def sale_selected_item(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Warning", "Please select an item to sell")
            return
        item_id = self.tree.item(item)["values"][0]
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_sale import AddSale
        AddSale(self.root, self.user, self.show_dashboard, item_id)

    def show_image(self, item_id):
        image_path = self.image_cache.get(item_id)
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((120, 120), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_window = tk.Toplevel(self.root)
                img_window.title("Item Image")
                tk.Label(img_window, image=photo).pack(pady=10)
                img_window.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display image: {e}")
        else:
            messagebox.showinfo("Info", "No image available")

    def search_items(self):
        search_term = self.search_entry.get()
        self.load_items(search_term)

    def show_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_dashboard()

    def logout(self):
        self.logout_callback()

    def __del__(self):
        self.conn.close()
