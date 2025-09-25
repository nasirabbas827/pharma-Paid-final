import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from PIL import Image, ImageTk

class ViewItems:
    def __init__(self, root, current_user, back_callback):
        self.root = root
        self.current_user = current_user
        self.back_callback = back_callback
        self.root.title("PharmaCare - View Items")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")  
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()
        self.image_cache = {}  # Cache for image objects
        self.create_view()

    def create_view(self):
        # Main frame for centered layout
        main_frame = tk.Frame(self.root, bg="#ed79a9")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(main_frame, text="Item List", font=("Arial", 16, "bold"), 
                bg="#ed79a9", fg="#000000").grid(row=0, column=0, columnspan=2, pady=20)

        # Search bar in grid layout
        tk.Label(main_frame, text="Search by ID or Name", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.search_entry = tk.Entry(main_frame, width=30, font=("Arial", 12),
                                   bd=2, relief="groove", bg="#ffffff", 
                                   highlightthickness=1, highlightcolor="#4CAF50")
        self.search_entry.grid(row=1, column=1, padx=10, pady=5)

        # Search button
        tk.Button(main_frame, text="Search", command=self.search_items,
                 bg="#2196F3", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#FF9800").grid(row=2, column=0, columnspan=2, pady=5)

        # Create treeview for displaying items
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#000000")
        style.configure("Treeview", font=("Arial", 11), rowheight=25, background="#ffffff")

        self.tree = ttk.Treeview(main_frame, columns=("ID", "Name", "Category", "Unit Price", "Cost Price", "Stock", "Expiry Date", "Image", "Actions"), 
                                show="headings", style="Treeview")
        self.tree.heading("ID", text="Item ID")
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Unit Price", text="Unit Price")
        self.tree.heading("Cost Price", text="Cost Price")
        self.tree.heading("Stock", text="Stock Quantity")
        self.tree.heading("Expiry Date", text="Expiry Date")
        self.tree.heading("Image", text="Image")
        self.tree.heading("Actions", text="Actions")
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Name", width=200, anchor="center")
        self.tree.column("Category", width=150, anchor="center")
        self.tree.column("Unit Price", width=100, anchor="center")
        self.tree.column("Cost Price", width=100, anchor="center")
        self.tree.column("Stock", width=100, anchor="center")
        self.tree.column("Expiry Date", width=120, anchor="center")
        self.tree.column("Image", width=120, anchor="center")
        self.tree.column("Actions", width=150, anchor="center")
        self.tree.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=3, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Load items
        self.load_items()

        # Button frame for row/column layout
        button_frame = tk.Frame(main_frame, bg="#ed79a9")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        # Buttons with different colors and borders
        tk.Button(button_frame, text="Add Item", command=self.add_item, 
                 bg="#4CAF50", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#2196F3").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Back to Dashboard", command=self.back_callback,
                 bg="#F44336", fg="white", font=("Arial", 12),
                 width=15, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#4CAF50").grid(row=0, column=1, padx=5, pady=5)

    def load_items(self, search_term=""):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch items from database
        query = '''
            SELECT mi.item_id, mi.item_name, ic.category_name, mi.unit_price, mi.cost_price, mi.stock_quantity, mi.expiry_date, mi.item_image
            FROM MedicalItems mi
            JOIN ItemCategories ic ON mi.category_id = ic.category_id
        '''
        if search_term:
            query += " WHERE mi.item_id LIKE ? OR mi.item_name LIKE ?"
            self.cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        else:
            self.cursor.execute(query)
        for item in self.cursor.fetchall():
            item_id, item_name, category_name, unit_price, cost_price, stock_quantity, expiry_date, item_image = item
            image_display = item_image.split('/')[-1] if item_image else "No image"
            self.tree.insert("", "end", values=(item_id, item_name, category_name, unit_price, cost_price, stock_quantity, expiry_date, image_display, "View/Edit/Delete"))
            if item_image:
                self.image_cache[item_id] = item_image

        # Bind single-click to handle actions
        self.tree.bind("<ButtonRelease-1>", self.handle_tree_click)

    def handle_tree_click(self, event):
        item = self.tree.selection()
        if not item:
            return
        col = self.tree.identify_column(event.x)
        item_id = self.tree.item(item)["values"][0]
        if col == "#9":  # Actions column
            self.show_action_menu(item_id)
        elif col == "#8" and item_id in self.image_cache:  # Image column
            self.show_image(item_id)

    def show_action_menu(self, item_id):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Edit", command=lambda: self.edit_item(item_id))
        menu.add_command(label="Delete", command=lambda: self.delete_item(item_id))
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def show_image(self, item_id):
        image_path = self.image_cache.get(item_id)
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_window = tk.Toplevel(self.root)
                img_window.title("Item Image")
                tk.Label(img_window, image=photo).pack(pady=10)
                img_window.image = photo  # Keep a reference
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display image: {e}")
        else:
            messagebox.showinfo("Info", "No image available")

    def search_items(self):
        search_term = self.search_entry.get()
        self.load_items(search_term)

    def edit_item(self, item_id):
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_items import AddItems
        add_item_page = AddItems(self.root, self.current_user, self.back_callback)
        add_item_page.load_item(item_id)

    def delete_item(self, item_id):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Sales WHERE item_id = ?", (item_id,))
            if self.cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "Cannot delete item; it is used in sales")
                return
            self.cursor.execute("SELECT COUNT(*) FROM Purchases WHERE item_id = ?", (item_id,))
            if self.cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "Cannot delete item; it is used in purchases")
                return
            self.cursor.execute("DELETE FROM MedicalItems WHERE item_id = ?", (item_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Item deleted successfully")
            self.load_items()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete item: {e}")

    def add_item(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_items import AddItems
        AddItems(self.root, self.current_user, self.back_callback)

    def __del__(self):
        self.conn.close()