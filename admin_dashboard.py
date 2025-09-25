import tkinter as tk
from tkinter import messagebox

class AdminDashboard:
    def __init__(self, root, user, logout_callback):
        self.root = root
        self.user = user
        self.logout_callback = logout_callback
        self.root.title("PharmaCare - Admin Dashboard")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")  
        self.create_dashboard()

    def create_dashboard(self):
        # Main frame for centered layout
        main_frame = tk.Frame(self.root, bg="#ed79a9")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome label
        tk.Label(main_frame, text=f"Welcome, {self.user['full_name']} (Admin)", 
                font=("Arial", 16, "bold"), bg="#ed79a9", fg="#000000").grid(row=0, column=0, columnspan=4, pady=20)

        # Button frame for grid layout
        button_frame = tk.Frame(main_frame, bg="#ed79a9")
        button_frame.grid(row=1, column=0, columnspan=4, pady=10)

        # Dashboard buttons in a 3x4 grid with colored borders
        tk.Button(button_frame, text="Add User", command=self.add_user, width=15,
                 bg="#4CAF50", fg="white", font=("Arial", 12), bd=3, relief="raised",
                 highlightthickness=2, highlightbackground="#2196F3").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="View Users", command=self.view_users, width=15,
                 bg="#2196F3", fg="white", font=("Arial", 12), bd=3, relief="raised",
                 highlightthickness=2, highlightbackground="#FF9800").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Add Categories", command=self.add_categories, width=15,
                 bg="#FF9800", fg="white", font=("Arial", 12), bd=3, relief="raised",
                 highlightthickness=2, highlightbackground="#4CAF50").grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="View Categories", command=self.view_categories, width=15,
                 bg="#9C27B0", fg="white", font=("Arial", 12), bd=3, relief="raised",
                 highlightthickness=2, highlightbackground="#F44336").grid(row=0, column=3, padx=5, pady=5)
        tk.Button(button_frame, text="Add Items", command=self.add_items, width=15,
                 bg="#F44336", fg="white", font=("Arial", 12), bd=3, relief="raised",
                 highlightthickness=2, highlightbackground="#2196F3").grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="View Items", command=self.view_items, width=15,
                 bg="#3F51B5", fg="white", font=("Arial", 12), bd=3, relief="raised",
                 highlightthickness=2, highlightbackground="#FF9800").grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Add Purchase", command=self.add_purchase, width=15,
                 bg="#009688", fg="white", font=("Arial", 12), bd=3, relief="raised",
                 highlightthickness=2, highlightbackground="#4CAF50").grid(row=1, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="View Purchases", command=self.view_purchases, width=15,
                 bg="#E91E63", fg="white", font=("Arial", 12), bd=3, relief="raised",
                 highlightthickness=2, highlightbackground="#F44336").grid(row=1, column=3, padx=5, pady=5)
        tk.Button(button_frame, text="View Sales", command=self.view_sales, width=15,
                 bg="#FFC107", fg="white", font=("Arial", 12), bd=3, relief="raised",
                 highlightthickness=2, highlightbackground="#2196F3").grid(row=2, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Generate Reports", command=self.generate_reports, width=15,
                 bg="#607D8B", fg="white", font=("Arial", 12), bd=3, relief="raised",
                 highlightthickness=2, highlightbackground="#FF9800").grid(row=2, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Logout", command=self.logout, width=15,
                 bg="#D81B60", fg="white", font=("Arial", 12), bd=3, relief="raised",
                 highlightthickness=2, highlightbackground="#4CAF50").grid(row=2, column=2, padx=5, pady=5)

    def add_user(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_users import AddUsers
        AddUsers(self.root, self.user, self.show_dashboard)

    def view_users(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from view_users import ViewUsers
        ViewUsers(self.root, self.user, self.show_dashboard)

    def add_categories(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_categories import AddCategories
        AddCategories(self.root, self.user, self.show_dashboard)

    def view_categories(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from view_categories import ViewCategories
        ViewCategories(self.root, self.user, self.show_dashboard)

    def add_items(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_items import AddItems
        AddItems(self.root, self.user, self.show_dashboard)

    def view_items(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from view_items import ViewItems
        ViewItems(self.root, self.user, self.show_dashboard)

    def add_purchase(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from add_purchase import AddPurchase
        AddPurchase(self.root, self.user, self.show_dashboard)

    def view_purchases(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from view_purchase import ViewPurchases
        ViewPurchases(self.root, self.user, self.show_dashboard)

    def view_sales(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from view_sales import ViewSales
        ViewSales(self.root, self.user, self.show_dashboard)

    def generate_reports(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        from generate_reports import GenerateReports
        GenerateReports(self.root, self.user, self.show_dashboard)

    def show_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_dashboard()

    def logout(self):
        self.logout_callback()