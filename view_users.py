import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ViewUsers:
    def __init__(self, root, current_user, back_callback):
        self.root = root
        self.current_user = current_user
        self.back_callback = back_callback
        self.root.title("PharmaCare - View Users")
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
        tk.Label(main_frame, text="User List", font=("Arial", 16, "bold"), 
                bg="#ed79a9", fg="#000000").grid(row=0, column=0, columnspan=2, pady=20)

        # Create treeview for displaying users
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#000000")
        style.configure("Treeview", font=("Arial", 11), rowheight=25, background="#ffffff")

        self.tree = ttk.Treeview(main_frame, columns=("ID", "Username", "Email", "Full Name", "Role"), 
                                show="headings", style="Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Full Name", text="Full Name")
        self.tree.heading("Role", text="Role")
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Username", width=200, anchor="center")
        self.tree.column("Email", width=250, anchor="center")
        self.tree.column("Full Name", width=200, anchor="center")
        self.tree.column("Role", width=150, anchor="center")
        self.tree.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Load users
        self.load_users()

        # Button frame for row/column layout
        button_frame = tk.Frame(main_frame, bg="#ed79a9")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        # Buttons with different colors and borders
        tk.Button(button_frame, text="Add User", command=self.add_user, 
                 bg="#4CAF50", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#2196F3").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Back to Dashboard", command=self.back_callback,
                 bg="#F44336", fg="white", font=("Arial", 12),
                 width=15, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#FF9800").grid(row=0, column=1, padx=5, pady=5)

    def load_users(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch users from database
        self.cursor.execute("SELECT user_id, username, email, full_name, role FROM Users")
        for user in self.cursor.fetchall():
            self.tree.insert("", "end", values=user)

        # Bind double-click to edit
        self.tree.bind("<Double-1>", self.edit_user)

    def edit_user(self, event):
        item = self.tree.selection()
        if not item:
            return
        user_id = self.tree.item(item)["values"][0]
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_users import AddUsers
        add_user_page = AddUsers(self.root, self.current_user, self.back_callback)
        add_user_page.load_user(user_id)

    def delete_user(self, user_id):
        if user_id == self.current_user['user_id']:
            messagebox.showerror("Error", "Cannot delete the currently logged-in user")
            return
        try:
            self.cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "User deleted successfully")
            self.load_users()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {e}")

    def add_user(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_users import AddUsers
        AddUsers(self.root, self.current_user, self.back_callback)

    def __del__(self):
        self.conn.close()