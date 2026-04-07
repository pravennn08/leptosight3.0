import customtkinter as ctk
from tkinter import ttk
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

ctk.set_appearance_mode("light")  # or "dark"
ctk.set_default_color_theme("blue")


def connect_db():
    try:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
    except Exception as e:
        print(f"DB Error: {e}")
        return None


class DBViewer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Database Viewer")
        self.geometry("1000x650")

        # ===== HEADER =====
        self.header = ctk.CTkFrame(self, height=70, fg_color="#F8FAFC")
        self.header.pack(fill="x")

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Database Viewer",
            font=("Poppins", 24, "bold"),
            text_color="#0F172A",
        )
        self.title_label.pack(side="left", padx=20, pady=15)

        # ===== CONTROLS =====
        self.control_frame = ctk.CTkFrame(self, height=80)
        self.control_frame.pack(fill="x", padx=20, pady=10)

        # Table selector
        self.table_option = ctk.CTkOptionMenu(
            self.control_frame,
            values=["users", "diagnostic", "rate_limits"],
            command=self.on_table_change,
            width=200,
        )
        self.table_option.set("users")
        self.table_option.pack(side="left", padx=10, pady=20)

        # Refresh button
        self.refresh_btn = ctk.CTkButton(
            self.control_frame,
            text="Refresh",
            command=self.load_data,
            fg_color="#14B8A6",
            hover_color="#0D9488",
        )
        self.refresh_btn.pack(side="left", padx=10)

        # ===== TABLE FRAME =====
        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Treeview (table)
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="#0F172A",
            rowheight=30,
            fieldbackground="#FFFFFF",
        )

        style.configure("Treeview.Heading", font=("Poppins", 12, "bold"))

        self.tree = ttk.Treeview(self.table_frame)
        self.tree.pack(fill="both", expand=True)

        # Bind events
        self.tree.bind("<ButtonRelease-1>", self.on_cell_click)
        self.tree.bind("<Double-1>", self.on_double_click)

        # ===== CELL VIEWER =====
        self.cell_frame = ctk.CTkFrame(self)
        self.cell_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.cell_label = ctk.CTkLabel(
            self.cell_frame, text="Selected Cell Value:", font=("Poppins", 14, "bold")
        )
        self.cell_label.pack(anchor="w", padx=10, pady=(10, 5))

        self.cell_value = ctk.CTkTextbox(self.cell_frame, height=80)
        self.cell_value.pack(fill="x", padx=10, pady=5)

        self.copy_btn = ctk.CTkButton(
            self.cell_frame,
            text="Copy",
            command=self.copy_cell_value,
            fg_color="#64748B",
            hover_color="#475569",
        )
        self.copy_btn.pack(anchor="e", padx=10, pady=10)

        # Load initial data
        self.load_data()

    def on_table_change(self, value):
        self.load_data()

    def load_data(self):
        table_name = self.table_option.get()

        conn = connect_db()
        if not conn:
            return

        cursor = conn.cursor()

        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]

            # Clear table
            self.tree.delete(*self.tree.get_children())

            # Setup columns
            self.tree["columns"] = colnames
            self.tree["show"] = "headings"

            for col in colnames:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor="center")

            # Insert data
            for row in rows:
                self.tree.insert("", "end", values=row)

        except Exception as e:
            print("Error:", e)

        finally:
            cursor.close()
            conn.close()

    def on_cell_click(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return

        # Detect region
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        # Get column index
        col = self.tree.identify_column(event.x)
        col_index = int(col.replace("#", "")) - 1

        values = self.tree.item(selected_item, "values")

        if col_index < len(values):
            cell_value = str(values[col_index])

            # Show value
            self.cell_value.delete("1.0", "end")
            self.cell_value.insert("1.0", cell_value)

    def on_double_click(self, event):
        self.copy_cell_value()

    def copy_cell_value(self):
        value = self.cell_value.get("1.0", "end").strip()
        if value:
            self.clipboard_clear()
            self.clipboard_append(value)
            print("Copied:", value)


if __name__ == "__main__":
    app = DBViewer()
    app.mainloop()
