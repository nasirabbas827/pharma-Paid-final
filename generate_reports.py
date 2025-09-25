import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

class GenerateReports:
    def __init__(self, root, current_user, back_callback):
        self.root = root
        self.current_user = current_user
        self.back_callback = back_callback
        self.root.title("PharmaCare - Generate Reports")
        self.root.geometry("1100x600")
        self.root.configure(bg="#ed79a9")  
        self.conn = sqlite3.connect('pharmacy.db')
        self.cursor = self.conn.cursor()
        self.reports_folder = "reports"
        if not os.path.exists(self.reports_folder):
            os.makedirs(self.reports_folder)
        self.create_form()

    def create_form(self):
        # Main frame for centered layout
        main_frame = tk.Frame(self.root, bg="#ed79a9")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(main_frame, text="Generate Reports", font=("Arial", 16, "bold"), 
                bg="#ed79a9", fg="#000000").grid(row=0, column=0, columnspan=2, pady=20)

        # Report type selection
        tk.Label(main_frame, text="Report Type", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.report_var = tk.StringVar(value="Stock")
        tk.Radiobutton(main_frame, text="Stock", variable=self.report_var, value="Stock",
                      font=("Arial", 12), bg="#ed79a9", fg="#000000", 
                      selectcolor="#ffffff", activebackground="#ed79a9").grid(row=1, column=1, sticky="w", padx=10, pady=2)
        tk.Radiobutton(main_frame, text="Sales", variable=self.report_var, value="Sales",
                      font=("Arial", 12), bg="#ed79a9", fg="#000000", 
                      selectcolor="#ffffff", activebackground="#ed79a9").grid(row=2, column=1, sticky="w", padx=10, pady=2)
        tk.Radiobutton(main_frame, text="Purchases", variable=self.report_var, value="Purchases",
                      font=("Arial", 12), bg="#ed79a9", fg="#000000", 
                      selectcolor="#ffffff", activebackground="#ed79a9").grid(row=3, column=1, sticky="w", padx=10, pady=2)
        tk.Radiobutton(main_frame, text="Profit", variable=self.report_var, value="Profit",
                      font=("Arial", 12), bg="#ed79a9", fg="#000000", 
                      selectcolor="#ffffff", activebackground="#ed79a9").grid(row=4, column=1, sticky="w", padx=10, pady=2)

        # Date range selection
        tk.Label(main_frame, text="Start Date", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.start_date_entry = DateEntry(main_frame, date_pattern="yyyy-mm-dd", 
                                         font=("Arial", 12), background="#ffffff", 
                                         foreground="#000000", borderwidth=2, 
                                         relief="groove", selectbackground="#4CAF50")
        self.start_date_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        tk.Label(main_frame, text="End Date", font=("Arial", 12), 
                bg="#ed79a9", fg="#000000").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.end_date_entry = DateEntry(main_frame, date_pattern="yyyy-mm-dd", 
                                       font=("Arial", 12), background="#ffffff", 
                                       foreground="#000000", borderwidth=2, 
                                       relief="groove", selectbackground="#4CAF50")
        self.end_date_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Button frame for row/column layout
        button_frame = tk.Frame(main_frame, bg="#ed79a9")
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)

        # Buttons with different colors and borders
        tk.Button(button_frame, text="Generate Report", command=self.generate_report, 
                 bg="#4CAF50", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#2196F3").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Download PDF", command=self.download_pdf,
                 bg="#2196F3", fg="white", font=("Arial", 12),
                 width=12, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#FF9800").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Back to Dashboard", command=self.back_callback,
                 bg="#F44336", fg="white", font=("Arial", 12),
                 width=15, bd=3, relief="raised", highlightthickness=2,
                 highlightbackground="#4CAF50").grid(row=0, column=2, padx=5, pady=5)

        # Treeview for report display
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#000000")
        style.configure("Treeview", font=("Arial", 11), rowheight=25, background="#ffffff")
        self.tree = ttk.Treeview(main_frame, show="headings", style="Treeview")
        self.tree.grid(row=8, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=8, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.report_data = []

    def generate_report(self):
        report_type = self.report_var.get()
        start_date = self.start_date_entry.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date_entry.get_date().strftime("%Y-%m-%d")

        # Validate dates
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if start > end:
                messagebox.showerror("Error", "Start date must be before end date")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid date format")
            return

        self.report_data = []
        self.tree["columns"] = []

        if report_type == "Stock":
            self.generate_stock_report()
        elif report_type == "Sales":
            self.generate_sales_report(start_date, end_date)
        elif report_type == "Purchases":
            self.generate_purchases_report(start_date, end_date)
        elif report_type == "Profit":
            self.generate_profit_report(start_date, end_date)

        self.display_report()

    def generate_stock_report(self):
        self.tree["columns"] = ("ID", "Item Name", "Category", "Stock Quantity", "Unit Price", "Image")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.column("Item Name", width=200)

        self.cursor.execute('''
            SELECT mi.item_id, mi.item_name, ic.category_name, mi.stock_quantity, mi.unit_price, mi.item_image
            FROM MedicalItems mi
            JOIN ItemCategories ic ON mi.category_id = ic.category_id
        ''')
        self.report_data = self.cursor.fetchall()

    def generate_sales_report(self, start_date, end_date):
        self.tree["columns"] = ("Sale ID", "Item Name", "Quantity Sold", "Total Amount", "Sale Date", "Image")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.column("Item Name", width=200)

        self.cursor.execute('''
            SELECT s.sale_id, mi.item_name, s.quantity_sold, s.total_amount, s.sale_date, mi.item_image
            FROM Sales s
            JOIN MedicalItems mi ON s.item_id = mi.item_id
            WHERE s.sale_date BETWEEN ? AND ?
        ''', (start_date, f"{end_date} 23:59:59"))
        self.report_data = self.cursor.fetchall()

    def generate_purchases_report(self, start_date, end_date):
        self.tree["columns"] = ("Purchase ID", "Item Name", "Quantity Purchased", "Total Cost", "Purchase Date", "Image")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.column("Item Name", width=200)

        self.cursor.execute('''
            SELECT p.purchase_id, mi.item_name, p.quantity_purchased, p.total_cost, p.purchase_date, mi.item_image
            FROM Purchases p
            JOIN MedicalItems mi ON p.item_id = mi.item_id
            WHERE p.purchase_date BETWEEN ? AND ?
        ''', (start_date, f"{end_date} 23:59:59"))
        self.report_data = self.cursor.fetchall()

    def generate_profit_report(self, start_date, end_date):
        self.tree["columns"] = ("Item Name", "Total Sales", "Total Purchases", "Profit")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.cursor.execute('''
            SELECT mi.item_name,
                   COALESCE(SUM(s.quantity_sold * mi.unit_price), 0) as total_sales,
                   COALESCE(SUM(p.quantity_purchased * mi.cost_price), 0) as total_purchases
            FROM MedicalItems mi
            LEFT JOIN Sales s ON mi.item_id = s.item_id AND s.sale_date BETWEEN ? AND ?
            LEFT JOIN Purchases p ON mi.item_id = p.item_id AND p.purchase_date BETWEEN ? AND ?
            GROUP BY mi.item_id, mi.item_name
        ''', (start_date, f"{end_date} 23:59:59", start_date, f"{end_date} 23:59:59"))
        data = self.cursor.fetchall()
        self.report_data = [(item_name, total_sales, total_purchases, total_sales - total_purchases) for item_name, total_sales, total_purchases in data]

    def display_report(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.report_data:
            self.tree.insert("", "end", values=row)
        if self.report_var.get() != "Profit":
            self.tree.bind("<ButtonRelease-1>", self.handle_tree_click)

    def handle_tree_click(self, event):
        item = self.tree.selection()
        if not item:
            return
        col = self.tree.identify_column(event.x)
        row_values = self.tree.item(item)["values"]
        if col == f"#{len(self.tree['columns'])}":  # Image column
            image_path = row_values[-1]
            if image_path and os.path.exists(image_path):
                try:
                    from PIL import Image, ImageTk
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

    def download_pdf(self):
        if not self.report_data:
            messagebox.showerror("Error", "Generate a report first")
            return

        report_type = self.report_var.get()
        start_date = self.start_date_entry.get_date().strftime("%Y-%m-%d")
        end_date = self.end_date_entry.get_date().strftime("%Y-%m-%d")
        filename = f"{self.reports_folder}/{report_type.lower()}_report_{start_date}_to_{end_date}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph(f"{report_type} Report", styles['Heading1']))
        elements.append(Paragraph(f"Date Range: {start_date} to {end_date}", styles['Normal']))
        elements.append(Spacer(1, 12))

        data = [self.tree["columns"]] + [list(row) for row in self.report_data]
        if report_type != "Profit":
            data = [row[:-1] + [row[-1].split('/')[-1] if row[-1] else "No image"] for row in data]

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

        if report_type != "Profit":
            elements.append(Spacer(1, 12))
            elements.append(Paragraph("Images:", styles['Heading2']))
            for row in self.report_data:
                image_path = row[-1]
                if image_path and os.path.exists(image_path):
                    img = Image(image_path, width=50, height=50)
                    elements.append(img)

        doc.build(elements)
        messagebox.showinfo("Success", f"Report saved as {filename}")

    def __del__(self):
        self.conn.close()