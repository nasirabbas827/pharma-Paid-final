import tkinter as tk
from tkinter import messagebox
import sqlite3

class AddCategories:
    def __init__(self, root, current_user, back_callback):
        self.root = root
        self.current_user = current_user
        self.back_callback = back_callback
        self.root.title("PharmaCare - Add/Edit Category")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")  
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()
        self.category_id = None  # For editing existing category
        self.create_form()

    def create_form(self):
        # Main frame for centered layout
        main_frame = tk.Frame(self.root, bg="#ed79a9")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(main_frame, text="Add/Edit Category", font=("Arial", 16, "bold"), 
                bg="#ed79a9", fg="#000000").grid(row=0, column=0, columnspan=2, pady=20)

        # Form field in grid layout
        tk.Label(main_frame, text="Category Name", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.category_name_entry = tk.Entry(main_frame, width=30, font=("Arial", 12),
                                          bd=2, relief="groove", bg="#ffffff", 
                                          highlightthickness=1, highlightcolor="#4CAF50")
        self.category_name_entry.grid(row=1, column=1, padx=10, pady=5)

        # Button frame for row/column layout
        button_frame = tk.Frame(main_frame, bg="#ed79a9")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        # Buttons with different colors and borders
        tk.Button(button_frame, text="Save Category", command=self.save_category, 
                 bg="#4CAF50", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#2196F3").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="View Categories", command=self.view_categories,
                 bg="#2196F3", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#FF9800").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Back to Dashboard", command=self.back_callback,
                 bg="#F44336", fg="white", font=("Arial", 12),
                 width=15, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#4CAF50").grid(row=0, column=2, padx=5, pady=5)

    def load_category(self, category_id):
        self.category_id = category_id
        self.cursor.execute("SELECT category_name FROM ItemCategories WHERE category_id = ?", (category_id,))
        category = self.cursor.fetchone()
        if category:
            self.category_name_entry.delete(0, tk.END)
            self.category_name_entry.insert(0, category[0])

    def save_category(self):
        category_name = self.category_name_entry.get()

        if not category_name:
            messagebox.showerror("Error", "Category name is required")
            return

        try:
            if self.category_id:  # Update existing category
                self.cursor.execute('''
                    UPDATE ItemCategories SET category_name = ?
                    WHERE category_id = ?
                ''', (category_name, self.category_id))
                messagebox.showinfo("Success", "Category updated successfully")
            else:  # Add new category
                self.cursor.execute('''
                    INSERT INTO ItemCategories (category_name)
                    VALUES (?)
                ''', (category_name,))
                messagebox.showinfo("Success", "Category added successfully")
            self.conn.commit()
            self.clear_form()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Category name already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save category: {e}")

    def clear_form(self):
        self.category_id = None
        self.category_name_entry.delete(0, tk.END)

    def view_categories(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from view_categories import ViewCategories
        ViewCategories(self.root, self.current_user, self.back_callback)

    def __del__(self):
        self.conn.close()