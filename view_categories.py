import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ViewCategories:
    def __init__(self, root, current_user, back_callback):
        self.root = root
        self.current_user = current_user
        self.back_callback = back_callback
        self.root.title("PharmaCare - View Categories")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")  
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()
        self.create_view()

    def create_view(self):
        # Main frame for centered layout
        main_frame = tk.Frame(self.root, bg="#ed79a9")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(main_frame, text="Category List", font=("Arial", 16, "bold"), 
                bg="#ed79a9", fg="#000000").grid(row=0, column=0, columnspan=2, pady=20)

        # Search bar in grid layout
        tk.Label(main_frame, text="Search by ID or Name", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.search_entry = tk.Entry(main_frame, width=30, font=("Arial", 12),
                                   bd=2, relief="groove", bg="#ffffff", 
                                   highlightthickness=1, highlightcolor="#4CAF50")
        self.search_entry.grid(row=1, column=1, padx=10, pady=5)

        # Search button
        tk.Button(main_frame, text="Search", command=self.search_categories,
                 bg="#2196F3", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#FF9800").grid(row=2, column=0, columnspan=2, pady=5)

        # Create treeview for displaying categories
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#000000")
        style.configure("Treeview", font=("Arial", 11), rowheight=25, background="#ffffff")

        self.tree = ttk.Treeview(main_frame, columns=("ID", "Name"), 
                                show="headings", style="Treeview")
        self.tree.heading("ID", text="Category ID")
        self.tree.heading("Name", text="Category Name")
        self.tree.column("ID", width=150, anchor="center")
        self.tree.column("Name", width=300, anchor="center")
        self.tree.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=3, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Load categories
        self.load_categories()

        # Button frame for row/column layout
        button_frame = tk.Frame(main_frame, bg="#ed79a9")
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        # Buttons with different colors and borders
        tk.Button(button_frame, text="Add Category", command=self.add_category, 
                 bg="#4CAF50", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#2196F3").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Back to Dashboard", command=self.back_callback,
                 bg="#F44336", fg="white", font=("Arial", 12),
                 width=15, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#4CAF50").grid(row=0, column=1, padx=5, pady=5)

    def load_categories(self, search_term=""):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch categories from database
        query = "SELECT category_id, category_name FROM ItemCategories"
        if search_term:
            query += " WHERE category_id LIKE ? OR category_name LIKE ?"
            self.cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        else:
            self.cursor.execute(query)
        for category in self.cursor.fetchall():
            self.tree.insert("", "end", values=category)

        # Bind double-click to edit
        self.tree.bind("<Double-1>", self.edit_category)

    def search_categories(self):
        search_term = self.search_entry.get()
        self.load_categories(search_term)

    def edit_category(self, event):
        item = self.tree.selection()
        if not item:
            return
        category_id = self.tree.item(item)["values"][0]
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_categories import AddCategories
        add_category_page = AddCategories(self.root, self.current_user, self.back_callback)
        add_category_page.load_category(category_id)

    def delete_category(self, category_id):
        try:
            # Check if category is used in MedicalItems
            self.cursor.execute("SELECT COUNT(*) FROM MedicalItems WHERE category_id = ?", (category_id,))
            if self.cursor.fetchone()[0] > 0:
                messagebox.showerror("Error", "Cannot delete category; it is used by medical items")
                return
            self.cursor.execute("DELETE FROM ItemCategories WHERE category_id = ?", (category_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Category deleted successfully")
            self.load_categories()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete category: {e}")

    def add_category(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_categories import AddCategories
        AddCategories(self.root, self.current_user, self.back_callback)

    def __del__(self):
        self.conn.close()