import pandas as pd
import os
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

DATA_FILE = "sales.csv"

# Ensure CSV exists
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Customer", "Product", "Quantity", "Price"])
    df.to_csv(DATA_FILE, index=False)

# Save sale
def save_sale():
    date = date_entry.get()
    customer = customer_entry.get()
    product = product_entry.get()
    quantity = quantity_entry.get()
    price = price_entry.get()

    if not (date and customer and product and quantity and price):
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        quantity = int(quantity)
        price = float(price)
    except ValueError:
        messagebox.showerror("Error", "Quantity must be an integer and Price must be a float")
        return

    new_sale = pd.DataFrame([[date, customer, product, quantity, price]],
                            columns=["Date", "Customer", "Product", "Quantity", "Price"])
    df = pd.read_csv(DATA_FILE)
    df = pd.concat([df, new_sale], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    messagebox.showinfo("Success", "✅ Sale added successfully")
    clear_fields()
    view_sales()

def clear_fields():
    date_entry.delete(0, END)
    customer_entry.delete(0, END)
    product_entry.delete(0, END)
    quantity_entry.delete(0, END)
    price_entry.delete(0, END)

def view_sales():
    for row in sales_tree.get_children():
        sales_tree.delete(row)

    df = pd.read_csv(DATA_FILE)
    for index, row in df.iterrows():
        sales_tree.insert("", "end", values=list(row))

def show_report():
    df = pd.read_csv(DATA_FILE)
    df["Total"] = df["Quantity"] * df["Price"]
    total_sales = df["Total"].sum()
    messagebox.showinfo("📊 Sales Report", f"Total Sales Value: ₹{total_sales:.2f}")

# GUI Setup
root = Tk()
root.title("💼 Sales Data Management System")
root.geometry("900x650")
root.config(bg="#894646")

# --- Header ---
header = Label(root, text="📋 Sales Data Management System", font=("Helvetica", 20, "bold"), fg="#333", bg="#894646")
header.pack(pady=20)

# --- Form Section ---
form_frame = Frame(root, bg="#f4f4f4")
form_frame.pack(fill=X, padx=20)

Label(form_frame, text="Date (YYYY-MM-DD):", font=("Helvetica", 12), bg="#f4f4f4").grid(row=0, column=0, sticky=W, pady=5)
date_entry = Entry(form_frame, font=("Helvetica", 12))
date_entry.grid(row=0, column=1, padx=10, pady=5)

Label(form_frame, text="Customer Name:", font=("Helvetica", 12), bg="#f4f4f4").grid(row=1, column=0, sticky=W, pady=5)
customer_entry = Entry(form_frame, font=("Helvetica", 12))
customer_entry.grid(row=1, column=1, padx=10, pady=5)

Label(form_frame, text="Product Name:", font=("Helvetica", 12), bg="#f4f4f4").grid(row=2, column=0, sticky=W, pady=5)
product_entry = Entry(form_frame, font=("Helvetica", 12))
product_entry.grid(row=2, column=1, padx=10, pady=5)

Label(form_frame, text="Quantity:", font=("Helvetica", 12), bg="#f4f4f4").grid(row=3, column=0, sticky=W, pady=5)
quantity_entry = Entry(form_frame, font=("Helvetica", 12))
quantity_entry.grid(row=3, column=1, padx=10, pady=5)

Label(form_frame, text="Price per Unit:", font=("Helvetica", 12), bg="#f4f4f4").grid(row=4, column=0, sticky=W, pady=5)
price_entry = Entry(form_frame, font=("Helvetica", 12))
price_entry.grid(row=4, column=1, padx=10, pady=5)

# --- Buttons ---
btn_frame = Frame(root, bg="#f4f4f4")
btn_frame.pack(pady=15)

add_btn = Button(btn_frame, text="➕ Add Sale", font=("Helvetica", 12, "bold"), bg="#28a745", fg="white", width=15, command=save_sale)
add_btn.grid(row=0, column=0, padx=10)

report_btn = Button(btn_frame, text="📊 Show Report", font=("Helvetica", 12, "bold"), bg="#007bff", fg="white", width=15, command=show_report)
report_btn.grid(row=0, column=1, padx=10)

# --- Table Section ---
table_label = Label(root, text="📈 Sales Records", font=("Helvetica", 16, "bold"), fg="#444", bg="#f4f4f4")
table_label.pack(pady=10)

table_frame = Frame(root)
table_frame.pack(fill=BOTH, expand=True, padx=20)

style = ttk.Style()
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
style.configure("Treeview", font=("Helvetica", 11), rowheight=25)

cols = ["Date", "Customer", "Product", "Quantity", "Price"]
sales_tree = ttk.Treeview(table_frame, columns=cols, show='headings')
for col in cols:
    sales_tree.heading(col, text=col)
    sales_tree.column(col, anchor=CENTER, width=150)

sales_tree.pack(fill=BOTH, expand=True)

view_sales()  # Load data initially
root.mainloop()
