import tkinter as tk
from tkinter import messagebox
import sqlite3

class PharmacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PharmaCare Management System - Login")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")  
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()
        self.current_user = None
        self.create_login_page()

    def create_login_page(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create main frame for centered layout
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Login page widgets
        tk.Label(main_frame, text="PharmaCare Login", font=("Arial", 16, "bold"), 
                bg="#f0f0f0", fg="#000000").grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(main_frame, text="Username", font=("Arial", 12), 
                bg="#f0f0f0", fg="#000000").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.username_entry = tk.Entry(main_frame, width=30, font=("Arial", 12),
                                     bd=2, relief="groove", bg="#ffffff", 
                                     highlightthickness=1, highlightcolor="#4CAF50")
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(main_frame, text="Password", font=("Arial", 12), 
                bg="#f0f0f0", fg="#000000").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.password_entry = tk.Entry(main_frame, width=30, show="*", font=("Arial", 12),
                                      bd=2, relief="groove", bg="#ffffff", 
                                      highlightthickness=1, highlightcolor="#4CAF50")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Button frame for row/column layout
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        # Login button with blue border
        tk.Button(button_frame, text="Login", command=self.login, 
                 bg="#4CAF50", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#2196F3", activebackground="#45a049").grid(row=0, column=0, padx=5)
        
        # Clear button with red border
        tk.Button(button_frame, text="Clear", command=self.clear_entries,
                 bg="#f44336", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#D81B60", activebackground="#da190b").grid(row=0, column=1, padx=5)

    def clear_entries(self):
        """Clear username and password entries"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return

        # Query the database for user
        self.cursor.execute("SELECT user_id, username, password, role, full_name FROM Users WHERE username = ? AND password = ?",
                          (username, password))
        user = self.cursor.fetchone()
        if user:
            self.current_user = {
                'user_id': user[0],
                'username': user[1],
                'role': user[3],
                'full_name': user[4]
            }
            if self.current_user['role'] == 'admin':
                self.show_admin_dashboard()
            else:
                self.show_user_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_admin_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from admin_dashboard import AdminDashboard
        AdminDashboard(self.root, self.current_user, self.show_login_page)

    def show_user_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from user_dashboard import UserDashboard
        UserDashboard(self.root, self.current_user, self.show_login_page)

    def show_login_page(self):
        self.current_user = None
        self.create_login_page()

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()