import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from PIL import Image, ImageTk

class ViewPurchases:
    def __init__(self, root, current_user, back_callback):
        self.root = root
        self.current_user = current_user
        self.back_callback = back_callback
        self.root.title("PharmaCare - View Purchases")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")  
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()
        self.image_cache = {}
        self.create_view()

    def create_view(self):
        # Main frame for centered layout
        main_frame = tk.Frame(self.root, bg="#ed79a9")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(main_frame, text="Purchase List", font=("Arial", 16, "bold"), 
                bg="#ed79a9", fg="#000000").grid(row=0, column=0, columnspan=2, pady=20)

        # Search bar in grid layout
        tk.Label(main_frame, text="Search by ID or Item Name", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.search_entry = tk.Entry(main_frame, width=30, font=("Arial", 12),
                                   bd=2, relief="groove", bg="#ffffff", 
                                   highlightthickness=1, highlightcolor="#4CAF50")
        self.search_entry.grid(row=1, column=1, padx=10, pady=5)

        # Search button
        tk.Button(main_frame, text="Search", command=self.search_purchases,
                 bg="#2196F3", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#FF9800").grid(row=2, column=0, columnspan=2, pady=5)

        # Create treeview for displaying purchases
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#000000")
        style.configure("Treeview", font=("Arial", 11), rowheight=25, background="#ffffff")

        self.tree = ttk.Treeview(main_frame, columns=("ID", "Item Name", "Quantity", "Total Cost", "Date", "Image", "Actions"), 
                                show="headings", style="Treeview")
        self.tree.heading("ID", text="Purchase ID")
        self.tree.heading("Item Name", text="Item Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Total Cost", text="Total Cost")
        self.tree.heading("Date", text="Purchase Date")
        self.tree.heading("Image", text="Image")
        self.tree.heading("Actions", text="Actions")
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Item Name", width=200, anchor="center")
        self.tree.column("Quantity", width=100, anchor="center")
        self.tree.column("Total Cost", width=120, anchor="center")
        self.tree.column("Date", width=150, anchor="center")
        self.tree.column("Image", width=120, anchor="center")
        self.tree.column("Actions", width=120, anchor="center")
        self.tree.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=3, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Load purchases
        self.load_purchases()

        # Button frame for row/column layout
        button_frame = tk.Frame(main_frame, bg="#ed79a9")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        # Buttons with different colors and borders
        tk.Button(button_frame, text="Add Purchase", command=self.add_purchase, 
                 bg="#4CAF50", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#2196F3").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Back to Dashboard", command=self.back_callback,
                 bg="#F44336", fg="white", font=("Arial", 12),
                 width=15, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#4CAF50").grid(row=0, column=1, padx=5, pady=5)

    def load_purchases(self, search_term=""):
        for item in self.tree.get_children():
            self.tree.delete(item)

        query = '''
            SELECT p.purchase_id, mi.item_name, p.quantity_purchased, p.total_cost, p.purchase_date, mi.item_image
            FROM Purchases p
            JOIN MedicalItems mi ON p.item_id = mi.item_id
        '''
        if search_term:
            query += " WHERE p.purchase_id LIKE ? OR mi.item_name LIKE ?"
            self.cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        else:
            self.cursor.execute(query)
        for purchase in self.cursor.fetchall():
            purchase_id, item_name, quantity, total_cost, purchase_date, item_image = purchase
            image_display = item_image.split('/')[-1] if item_image else "No image"
            self.tree.insert("", "end", values=(purchase_id, item_name, quantity, total_cost, purchase_date, image_display, "Delete"))
            if item_image:
                self.image_cache[purchase_id] = item_image

        self.tree.bind("<ButtonRelease-1>", self.handle_tree_click)

    def search_purchases(self):
        search_term = self.search_entry.get()
        self.load_purchases(search_term)

    def handle_tree_click(self, event):
        item = self.tree.selection()
        if not item:
            return
        col = self.tree.identify_column(event.x)
        purchase_id = self.tree.item(item)["values"][0]
        if col == "#7":  # Actions column
            self.delete_purchase(purchase_id)
        elif col == "#6" and purchase_id in self.image_cache:  # Image column
            self.show_image(purchase_id)

    def show_image(self, purchase_id):
        image_path = self.image_cache.get(purchase_id)
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                img_window = tk.Toplevel(self.root)
                img_window.title("Item Image")
                tk.Label(img_window, image=photo).pack(pady=10)
                img_window.image = photo
            except Exception as e:
                messagebox.showerror("Error", f"Failed to display image: {e}")
        else:
            messagebox.showinfo("Info", "No image available")

    def delete_purchase(self, purchase_id):
        try:
            self.cursor.execute("SELECT item_id, quantity_purchased FROM Purchases WHERE purchase_id = ?", (purchase_id,))
            purchase = self.cursor.fetchone()
            if not purchase:
                messagebox.showerror("Error", "Purchase not found")
                return
            item_id, quantity = purchase
            # Update stock quantity
            self.cursor.execute('''
                UPDATE MedicalItems SET stock_quantity = stock_quantity - ?
                WHERE item_id = ?
            ''', (quantity, item_id))
            self.cursor.execute("DELETE FROM Purchases WHERE purchase_id = ?", (purchase_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Purchase deleted and stock updated")
            self.load_purchases()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete purchase: {e}")

    def add_purchase(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_purchase import AddPurchase
        AddPurchase(self.root, self.current_user, self.back_callback)

    def __del__(self):
        self.conn.close()