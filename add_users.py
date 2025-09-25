import tkinter as tk
from tkinter import messagebox
import sqlite3

class AddUsers:
    def __init__(self, root, current_user, back_callback):
        self.root = root
        self.current_user = current_user
        self.back_callback = back_callback
        self.root.title("PharmaCare - Add/Edit User")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")  
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()
        self.user_id = None  # For editing existing user
        self.create_form()

    def create_form(self):
        # Main frame for centered layout
        main_frame = tk.Frame(self.root, bg="#ed79a9")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(main_frame, text="Add/Edit User", font=("Arial", 16, "bold"), 
                bg="#ed79a9", fg="#000000").grid(row=0, column=0, columnspan=2, pady=20)

        # Form fields in grid layout
        tk.Label(main_frame, text="Username", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.username_entry = tk.Entry(main_frame, width=30, font=("Arial", 12),
                                     bd=2, relief="groove", bg="#ffffff", 
                                     highlightthickness=1, highlightcolor="#4CAF50")
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(main_frame, text="Password", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.password_entry = tk.Entry(main_frame, width=30, show="*", font=("Arial", 12),
                                      bd=2, relief="groove", bg="#ffffff", 
                                      highlightthickness=1, highlightcolor="#4CAF50")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(main_frame, text="Email", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = tk.Entry(main_frame, width=30, font=("Arial", 12),
                                   bd=2, relief="groove", bg="#ffffff", 
                                   highlightthickness=1, highlightcolor="#4CAF50")
        self.email_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(main_frame, text="Full Name", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.full_name_entry = tk.Entry(main_frame, width=30, font=("Arial", 12),
                                       bd=2, relief="groove", bg="#ffffff", 
                                       highlightthickness=1, highlightcolor="#4CAF50")
        self.full_name_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(main_frame, text="Role", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.role_var = tk.StringVar(value="user")
        tk.Radiobutton(main_frame, text="Admin", variable=self.role_var, value="admin",
                      bg="#ed79a9", fg="#000000", font=("Arial", 12),
                      selectcolor="#ffffff").grid(row=5, column=1, sticky="w", padx=10)
        tk.Radiobutton(main_frame, text="User", variable=self.role_var, value="user",
                      bg="#ed79a9", fg="#000000", font=("Arial", 12),
                      selectcolor="#ffffff").grid(row=6, column=1, sticky="w", padx=10)

        # Button frame for row/column layout
        button_frame = tk.Frame(main_frame, bg="#ed79a9")
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        # Buttons with different colors and borders
        tk.Button(button_frame, text="Save User", command=self.save_user, 
                 bg="#4CAF50", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#2196F3").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="View Users", command=self.view_users,
                 bg="#2196F3", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#FF9800").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Back to Dashboard", command=self.back_callback,
                 bg="#F44336", fg="white", font=("Arial", 12),
                 width=15, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#4CAF50").grid(row=0, column=2, padx=5, pady=5)

    def load_user(self, user_id):
        self.user_id = user_id
        self.cursor.execute("SELECT username, password, email, full_name, role FROM Users WHERE user_id = ?", (user_id,))
        user = self.cursor.fetchone()
        if user:
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, user[0])
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, user[1])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, user[2])
            self.full_name_entry.delete(0, tk.END)
            self.full_name_entry.insert(0, user[3])
            self.role_var.set(user[4])

    def save_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        full_name = self.full_name_entry.get()
        role = self.role_var.get()

        if not all([username, password, email, full_name]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            if self.user_id:  # Update existing user
                self.cursor.execute('''
                    UPDATE Users SET username = ?, password = ?, email = ?, full_name = ?, role = ?
                    WHERE user_id = ?
                ''', (username, password, email, full_name, role, self.user_id))
                messagebox.showinfo("Success", "User updated successfully")
            else:  # Add new user
                self.cursor.execute('''
                    INSERT INTO Users (username, password, email, full_name, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', (username, password, email, full_name, role))
                messagebox.showinfo("Success", "User added successfully")
            self.conn.commit()
            self.clear_form()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username or email already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save user: {e}")

    def clear_form(self):
        self.user_id = None
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.full_name_entry.delete(0, tk.END)
        self.role_var.set("user")

    def view_users(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from view_users import ViewUsers
        ViewUsers(self.root, self.current_user, self.back_callback)

    def __del__(self):
        self.conn.close()