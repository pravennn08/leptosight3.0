import customtkinter as ctk
from tkinter import ttk, messagebox, Menu
import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import sql
import threading
from datetime import datetime
import re

load_dotenv()

# Configure CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Modern color scheme
COLORS = {
    "primary": "#3B82F6",
    "primary_hover": "#2563EB",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "info": "#8B5CF6",
    "background": "#0F172A",
    "surface": "#1E293B",
    "surface_light": "#334155",
    "text": "#F1F5F9",
    "text_secondary": "#94A3B8",
    "border": "#2D3A4F",
}


def connect_db():
    """Establish database connection with retry logic"""
    try:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            connect_timeout=5,
        )
    except Exception as e:
        print(f"DB Error: {e}")
        return None


class ModernTable(ctk.CTkFrame):
    """Custom modern table widget with enhanced features"""

    def __init__(self, parent, db_viewer=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.db_viewer = db_viewer

        # Create Treeview with custom style
        style = ttk.Style()
        style.theme_use("clam")

        # Configure Treeview style
        style.configure(
            "Modern.Treeview",
            background=COLORS["surface"],
            foreground=COLORS["text"],
            fieldbackground=COLORS["surface"],
            borderwidth=0,
            font=("Inter", 12),
        )

        style.configure(
            "Modern.Treeview.Heading",
            background=COLORS["surface_light"],
            foreground=COLORS["text"],
            borderwidth=0,
            font=("Inter", 13, "bold"),
        )

        style.map("Modern.Treeview", background=[("selected", COLORS["primary"])])

        # Create scrollbars
        self.scroll_y = ttk.Scrollbar(self, orient="vertical")
        self.scroll_x = ttk.Scrollbar(self, orient="horizontal")

        # Create treeview
        self.tree = ttk.Treeview(
            self,
            style="Modern.Treeview",
            yscrollcommand=self.scroll_y.set,
            xscrollcommand=self.scroll_x.set,
        )

        self.scroll_y.configure(command=self.tree.yview)
        self.scroll_x.configure(command=self.tree.xview)

        # Pack components
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scroll_y.grid(row=0, column=1, sticky="ns")
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Bind events
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Control-c>", lambda e: self.copy_selected_cells())
        self.tree.bind("<Control-C>", lambda e: self.copy_selected_cells())

    def show_context_menu(self, event):
        """Show right-click context menu using tkinter Menu"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)

            # Get column info
            column = self.tree.identify_column(event.x)
            col_index = int(column.replace("#", "")) - 1 if column else -1

            # Create menu using tkinter Menu (not CTkMenu)
            self.context_menu = Menu(
                self, tearoff=False, bg=COLORS["surface"], fg=COLORS["text"]
            )
            self.context_menu.add_command(
                label="📋 Copy Value", command=self.copy_selected_value
            )
            self.context_menu.add_command(
                label="📄 Copy Row", command=self.copy_selected_row
            )
            self.context_menu.add_command(
                label="📊 Copy All Selected Columns", command=self.copy_selected_cells
            )
            self.context_menu.add_separator()
            self.context_menu.add_command(
                label="✏️ Edit Row", command=lambda: self.event_generate("<<EditRow>>")
            )

            # Show the menu
            self.context_menu.post(event.x_root, event.y_root)

    def copy_selected_value(self):
        """Copy selected cell value to clipboard"""
        selected = self.tree.selection()
        if selected:
            # Get the column under cursor (need to get from last right-click)
            # For simplicity, copy the first selected cell
            values = self.tree.item(selected[0])["values"]
            if values:
                self.clipboard_clear()
                self.clipboard_append(str(values[0]))
                messagebox.showinfo("Copied", "Value copied to clipboard!")

    def copy_selected_row(self):
        """Copy entire selected row to clipboard"""
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])["values"]
            row_text = "\t".join(str(v) for v in values)
            self.clipboard_clear()
            self.clipboard_append(row_text)
            messagebox.showinfo("Copied", "Row copied to clipboard!")

    def copy_selected_cells(self):
        """Copy all selected cells/columns to clipboard"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select rows to copy")
            return

        # Get all columns
        columns = self.tree["columns"]

        # Build data for clipboard
        clipboard_data = []

        # Add header row
        headers = [col.replace("_", " ").title() for col in columns]
        clipboard_data.append("\t".join(headers))

        # Add data rows
        for item in selected_items:
            values = self.tree.item(item)["values"]
            row_data = [str(v) for v in values]
            clipboard_data.append("\t".join(row_data))

        # Copy to clipboard
        result = "\n".join(clipboard_data)
        self.clipboard_clear()
        self.clipboard_append(result)

        messagebox.showinfo(
            "Copied",
            f"Copied {len(selected_items)} row(s) with {len(columns)} columns to clipboard!",
        )


class DBViewer(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Modern Database Viewer")
        self.geometry("1200x700")
        self.minsize(800, 500)

        # Set icon (if available)
        try:
            self.iconbitmap("icon.ico")
        except:
            pass

        # Variables
        self.current_table = ctk.StringVar(value="users")
        self.search_term = ctk.StringVar()
        self.filter_column = ctk.StringVar(value="All Columns")
        self.rows_per_page = 50
        self.current_page = 1
        self.total_rows = 0
        self.is_loading = False
        self.edit_window = None  # Store reference to edit window

        # Setup UI
        self.setup_ui()

        # Load initial data
        self.load_data()

    def setup_ui(self):
        """Setup the complete user interface"""

        # ===== HEADER =====
        header = ctk.CTkFrame(self, height=80, fg_color=COLORS["surface"])
        header.pack(fill="x")
        header.pack_propagate(False)

        # Title and subtitle
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(
            title_frame,
            text="Modern Database Viewer",
            font=("Inter", 28, "bold"),
            text_color=COLORS["primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Efficient Database Management Interface",
            font=("Inter", 12),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w")

        # Stats display
        self.stats_label = ctk.CTkLabel(
            header, text="", font=("Inter", 12), text_color=COLORS["text_secondary"]
        )
        self.stats_label.pack(side="right", padx=20)

        # ===== MAIN CONTENT =====
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)

        # Left sidebar for filters
        sidebar = ctk.CTkFrame(main_container, width=250, fg_color=COLORS["surface"])
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)

        self.setup_sidebar(sidebar)

        # Right content area
        content = ctk.CTkFrame(main_container, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True)

        # Toolbar
        toolbar = ctk.CTkFrame(content, height=50, fg_color=COLORS["surface"])
        toolbar.pack(fill="x", pady=(0, 10))
        toolbar.pack_propagate(False)

        self.setup_toolbar(toolbar)

        # Table
        self.setup_table(content)

        # Status bar
        self.setup_status_bar()

    def setup_sidebar(self, sidebar):
        """Setup left sidebar with filters and options"""

        # Section title
        ctk.CTkLabel(
            sidebar,
            text="Database Explorer",
            font=("Inter", 16, "bold"),
            text_color=COLORS["primary"],
        ).pack(anchor="w", padx=15, pady=(15, 10))

        # Table selector
        ctk.CTkLabel(
            sidebar,
            text="Table",
            font=("Inter", 12, "bold"),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.table_menu = ctk.CTkOptionMenu(
            sidebar,
            values=["users", "diagnostic", "rate_limits"],
            command=lambda x: self.load_data(),
            font=("Inter", 12),
            fg_color=COLORS["surface_light"],
            button_color=COLORS["primary"],
            button_hover_color=COLORS["primary_hover"],
        )
        self.table_menu.pack(fill="x", padx=15, pady=(0, 15))

        # Search section
        ctk.CTkLabel(
            sidebar,
            text="Search",
            font=("Inter", 12, "bold"),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.search_entry = ctk.CTkEntry(
            sidebar,
            textvariable=self.search_term,
            placeholder_text="Search...",
            font=("Inter", 12),
            fg_color=COLORS["surface_light"],
        )
        self.search_entry.pack(fill="x", padx=15, pady=(0, 5))
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_data())

        # Filter column
        ctk.CTkLabel(
            sidebar,
            text="Filter by Column",
            font=("Inter", 12, "bold"),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.filter_menu = ctk.CTkOptionMenu(
            sidebar,
            values=["All Columns"],
            command=lambda x: self.load_data(),
            font=("Inter", 12),
            fg_color=COLORS["surface_light"],
            button_color=COLORS["primary"],
        )
        self.filter_menu.pack(fill="x", padx=15, pady=(0, 15))

        # Copy button
        ctk.CTkButton(
            sidebar,
            text="📋 Copy Selected Rows",
            command=self.copy_selected_to_clipboard,
            font=("Inter", 12, "bold"),
            fg_color=COLORS["info"],
            hover_color="#7C3AED",
        ).pack(fill="x", padx=15, pady=(10, 5))

        # Export button
        ctk.CTkButton(
            sidebar,
            text="📥 Export Data",
            command=self.export_data,
            font=("Inter", 12, "bold"),
            fg_color=COLORS["success"],
            hover_color="#059669",
        ).pack(fill="x", padx=15, pady=(5, 5))

        # Refresh button
        ctk.CTkButton(
            sidebar,
            text="🔄 Refresh",
            command=self.load_data,
            font=("Inter", 12, "bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
        ).pack(fill="x", padx=15, pady=(5, 15))

    def setup_toolbar(self, toolbar):
        """Setup top toolbar with actions"""

        # Edit button
        self.edit_btn = ctk.CTkButton(
            toolbar,
            text="✏️ Edit Selected",
            command=self.open_edit_window,
            font=("Inter", 12, "bold"),
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
        )
        self.edit_btn.pack(side="left", padx=10, pady=10)

        # Delete button
        self.delete_btn = ctk.CTkButton(
            toolbar,
            text="🗑️ Delete Selected",
            command=self.delete_row,
            font=("Inter", 12, "bold"),
            fg_color=COLORS["danger"],
            hover_color="#DC2626",
        )
        self.delete_btn.pack(side="left", padx=(0, 10), pady=10)

        # Copy button
        self.copy_btn = ctk.CTkButton(
            toolbar,
            text="📋 Copy Selected",
            command=self.copy_selected_to_clipboard,
            font=("Inter", 12, "bold"),
            fg_color=COLORS["info"],
            hover_color="#7C3AED",
        )
        self.copy_btn.pack(side="left", padx=5, pady=10)

        # Separator
        separator = ctk.CTkFrame(toolbar, width=2, fg_color=COLORS["border"])
        separator.pack(side="left", fill="y", padx=10, pady=5)

        # Pagination
        self.prev_btn = ctk.CTkButton(
            toolbar,
            text="◀ Previous",
            command=self.prev_page,
            font=("Inter", 12),
            fg_color=COLORS["surface_light"],
            width=100,
        )
        self.prev_btn.pack(side="left", padx=5, pady=10)

        self.page_label = ctk.CTkLabel(
            toolbar,
            text="Page 1",
            font=("Inter", 12, "bold"),
            text_color=COLORS["text"],
        )
        self.page_label.pack(side="left", padx=10)

        self.next_btn = ctk.CTkButton(
            toolbar,
            text="Next ▶",
            command=self.next_page,
            font=("Inter", 12),
            fg_color=COLORS["surface_light"],
            width=100,
        )
        self.next_btn.pack(side="left", padx=5, pady=10)

        # Rows per page
        ctk.CTkLabel(
            toolbar,
            text="Rows per page:",
            font=("Inter", 11),
            text_color=COLORS["text_secondary"],
        ).pack(side="right", padx=(0, 5))

        self.rows_select = ctk.CTkOptionMenu(
            toolbar,
            values=["20", "50", "100", "200"],
            command=lambda x: self.change_rows_per_page(),
            font=("Inter", 11),
            fg_color=COLORS["surface_light"],
            width=80,
        )
        self.rows_select.set("50")
        self.rows_select.pack(side="right", padx=10)

    def setup_table(self, parent):
        """Setup the main table widget"""
        table_frame = ctk.CTkFrame(parent, fg_color=COLORS["surface"])
        table_frame.pack(fill="both", expand=True)

        self.table = ModernTable(table_frame, db_viewer=self, fg_color="transparent")
        self.table.pack(fill="both", expand=True, padx=1, pady=1)

        # Bind events
        self.table.tree.bind("<<EditRow>>", lambda e: self.open_edit_window())
        self.table.tree.bind("<Double-1>", lambda e: self.open_edit_window())

    def setup_status_bar(self):
        """Setup status bar at bottom"""
        self.status_bar = ctk.CTkFrame(self, height=30, fg_color=COLORS["surface"])
        self.status_bar.pack(fill="x", side="bottom")

        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=("Inter", 11),
            text_color=COLORS["text_secondary"],
        )
        self.status_label.pack(side="left", padx=10)

        self.progress_bar = ctk.CTkProgressBar(
            self.status_bar,
            width=200,
            height=8,
            fg_color=COLORS["surface_light"],
            progress_color=COLORS["primary"],
        )
        self.progress_bar.pack(side="right", padx=10)
        self.progress_bar.set(0)

    def copy_selected_to_clipboard(self):
        """Copy selected rows to clipboard"""
        if hasattr(self, "table") and self.table:
            self.table.copy_selected_cells()

    def load_data(self):
        """Load data from database with pagination and filtering"""
        if self.is_loading:
            return

        self.is_loading = True
        self.progress_bar.start()
        self.status_label.configure(text="Loading data...")

        # Run in thread to prevent UI freezing
        thread = threading.Thread(target=self._load_data_thread)
        thread.start()

    def _load_data_thread(self):
        """Background thread for loading data"""
        table = self.table_menu.get()
        search = self.search_term.get().strip()
        filter_col = self.filter_menu.get()

        conn = connect_db()
        if not conn:
            self.after(
                0,
                lambda: self.status_label.configure(text="Database connection failed!"),
            )
            self.is_loading = False
            self.progress_bar.stop()
            return

        cursor = conn.cursor()

        try:
            # Get column names
            cursor.execute(
                sql.SQL("SELECT * FROM {} LIMIT 0").format(sql.Identifier(table))
            )
            columns = [desc[0] for desc in cursor.description]

            # Update filter menu if needed
            if (
                len(columns) > 0
                and self.filter_menu.cget("values") != ["All Columns"] + columns
            ):
                self.after(
                    0,
                    lambda: self.filter_menu.configure(
                        values=["All Columns"] + columns
                    ),
                )

            # Build query with pagination
            offset = (self.current_page - 1) * self.rows_per_page

            if search:
                # Search across columns
                if filter_col != "All Columns" and filter_col in columns:
                    where_clause = sql.SQL("{}::text ILIKE %s").format(
                        sql.Identifier(filter_col)
                    )
                    search_pattern = f"%{search}%"
                else:
                    conditions = [
                        sql.SQL("{}::text ILIKE %s").format(sql.Identifier(col))
                        for col in columns
                    ]
                    where_clause = sql.SQL(" OR ").join(conditions)
                    search_pattern = f"%{search}%"

                # Count total rows
                count_query = sql.SQL("SELECT COUNT(*) FROM {} WHERE {}").format(
                    sql.Identifier(table), where_clause
                )
                cursor.execute(count_query, (search_pattern,))
                self.total_rows = cursor.fetchone()[0]

                # Get paginated results
                query = sql.SQL(
                    "SELECT * FROM {} WHERE {} ORDER BY id ASC LIMIT %s OFFSET %s"
                ).format(sql.Identifier(table), where_clause)
                cursor.execute(query, (search_pattern, self.rows_per_page, offset))
            else:
                # Count total rows
                count_query = sql.SQL("SELECT COUNT(*) FROM {}").format(
                    sql.Identifier(table)
                )
                cursor.execute(count_query)
                self.total_rows = cursor.fetchone()[0]

                # Get paginated results
                query = sql.SQL(
                    "SELECT * FROM {} ORDER BY id ASC LIMIT %s OFFSET %s"
                ).format(sql.Identifier(table))
                cursor.execute(query, (self.rows_per_page, offset))

            rows = cursor.fetchall()

            # Update UI in main thread
            self.after(0, lambda: self._update_table(columns, rows))

        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {str(e)}"))
            print("Load Error:", e)

        finally:
            cursor.close()
            conn.close()
            self.is_loading = False
            self.after(0, lambda: self.progress_bar.stop())

    def _update_table(self, columns, rows):
        """Update table with loaded data"""
        self.table.tree.delete(*self.table.tree.get_children())
        self.table.tree["columns"] = columns
        self.table.tree["show"] = "headings"

        for col in columns:
            self.table.tree.heading(col, text=col.replace("_", " ").title())
            self.table.tree.column(col, width=150, minwidth=100)

        for row in rows:
            # Format values for better display
            formatted_row = []
            for value in row:
                if isinstance(value, datetime):
                    formatted_row.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                elif isinstance(value, bool):
                    formatted_row.append("✓" if value else "✗")
                elif value is None:
                    formatted_row.append("—")
                else:
                    formatted_row.append(str(value))
            self.table.tree.insert("", "end", values=formatted_row)

        # Update stats
        total_pages = (self.total_rows + self.rows_per_page - 1) // self.rows_per_page
        start_row = (self.current_page - 1) * self.rows_per_page + 1
        end_row = min(start_row + len(rows) - 1, self.total_rows)

        stats_text = f"Showing {start_row}-{end_row} of {self.total_rows} rows"
        self.stats_label.configure(text=stats_text)
        self.page_label.configure(text=f"Page {self.current_page} of {total_pages}")

        # Update pagination buttons
        self.prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
        self.next_btn.configure(
            state="normal" if self.current_page < total_pages else "disabled"
        )

        self.status_label.configure(text=f"Loaded {len(rows)} rows")

    def change_rows_per_page(self):
        """Change number of rows per page"""
        self.rows_per_page = int(self.rows_select.get())
        self.current_page = 1
        self.load_data()

    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.load_data()

    def next_page(self):
        """Go to next page"""
        self.current_page += 1
        self.load_data()

    def delete_row(self):
        """Delete selected row"""
        selected = self.table.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to delete")
            return

        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this row? This action cannot be undone.",
            icon="warning",
        )

        if not result:
            return

        item = self.table.tree.item(selected[0])
        row_id = item["values"][0]  # Assuming first column is ID

        table = self.table_menu.get()
        conn = connect_db()

        if not conn:
            messagebox.showerror("Error", "Database connection failed")
            return

        cursor = conn.cursor()

        try:
            query = sql.SQL("DELETE FROM {} WHERE id = %s").format(
                sql.Identifier(table)
            )
            cursor.execute(query, (row_id,))
            conn.commit()

            messagebox.showinfo("Success", "Row deleted successfully")
            self.load_data()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete row: {str(e)}")
            print("Delete Error:", e)

        finally:
            cursor.close()
            conn.close()

    def export_data(self):
        """Export current view to CSV"""
        from tkinter import filedialog

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Data",
        )

        if not file_path:
            return

        # Get all data (without pagination)
        table = self.table_menu.get()
        conn = connect_db()

        if not conn:
            messagebox.showerror("Error", "Database connection failed")
            return

        cursor = conn.cursor()

        try:
            cursor.execute(
                sql.SQL("SELECT * FROM {} ORDER BY id ASC").format(
                    sql.Identifier(table)
                )
            )
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            import csv

            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(columns)
                writer.writerows(rows)

            messagebox.showinfo("Success", f"Data exported to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")

        finally:
            cursor.close()
            conn.close()

    def open_edit_window(self):
        """Open edit window for selected row - FIXED MODAL"""
        selected = self.table.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a row to edit")
            return

        # Close existing edit window if open
        if self.edit_window and self.edit_window.winfo_exists():
            self.edit_window.destroy()

        item = self.table.tree.item(selected[0])
        values = item["values"]
        columns = self.table.tree["columns"]

        # Create edit window
        self.edit_window = ctk.CTkToplevel(self)
        self.edit_window.title("Edit Row")
        self.edit_window.geometry("500x600")
        self.edit_window.minsize(400, 400)

        # Make it modal - FIXED order
        self.edit_window.transient(self)  # Set parent relationship
        self.edit_window.focus_force()  # Force focus
        self.edit_window.grab_set()  # Now grab the focus
        self.edit_window.wait_visibility()  # Wait for window to be visible

        # Scrollable form
        form = ctk.CTkScrollableFrame(self.edit_window, fg_color=COLORS["surface"])
        form.pack(fill="both", expand=True, padx=20, pady=20)

        entries = {}
        current_id = values[0]

        for i, col in enumerate(columns):
            # Label
            label = ctk.CTkLabel(
                form,
                text=col.replace("_", " ").title(),
                font=("Inter", 12, "bold"),
                text_color=COLORS["text"],
            )
            label.pack(anchor="w", pady=(10, 5))

            # Entry
            entry = ctk.CTkEntry(
                form, font=("Inter", 12), fg_color=COLORS["surface_light"], height=35
            )

            val = values[i]
            if isinstance(val, list):
                entry.insert(0, ", ".join(str(v) for v in val))
            elif val == "—" or val is None:
                entry.insert(0, "")
            else:
                entry.insert(0, str(val))

            if col.lower() == "id":
                entry.configure(state="disabled", fg_color=COLORS["border"])

            entry.pack(fill="x", pady=(0, 5))
            entries[col] = entry

        # Buttons
        btn_frame = ctk.CTkFrame(self.edit_window, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.close_edit_window,
            font=("Inter", 12),
            fg_color=COLORS["surface_light"],
            hover_color=COLORS["border"],
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Update Row",
            command=lambda: self.update_row(entries, current_id),
            font=("Inter", 12, "bold"),
            fg_color=COLORS["success"],
            hover_color="#059669",
        ).pack(side="right", padx=5)

    def close_edit_window(self):
        """Close the edit window properly"""
        if self.edit_window and self.edit_window.winfo_exists():
            self.edit_window.grab_release()
            self.edit_window.destroy()
            self.edit_window = None

    def update_row(self, entries, row_id):
        """Update row in database"""
        table = self.table_menu.get()
        conn = connect_db()

        if not conn:
            messagebox.showerror("Error", "Database connection failed")
            return

        cursor = conn.cursor()

        try:
            updates = []
            values = []

            for col, entry in entries.items():
                if col.lower() == "id":
                    continue

                val = entry.get().strip()

                # Skip empty values (keep original)
                if not val:
                    continue

                # Try to convert to appropriate type
                if val.lower() in ["true", "false"]:
                    val = val.lower() == "true"
                elif val.isdigit():
                    val = int(val)
                elif re.match(r"^\d+\.\d+$", val):
                    val = float(val)

                updates.append(f"{col} = %s")
                values.append(val)

            if not updates:
                messagebox.showwarning("No Changes", "No changes to update")
                return

            values.append(row_id)
            query = f"UPDATE {table} SET {', '.join(updates)} WHERE id = %s"
            cursor.execute(query, values)
            conn.commit()

            messagebox.showinfo("Success", "Row updated successfully")
            self.close_edit_window()
            self.load_data()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {str(e)}")
            print("Update Error:", e)

        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app = DBViewer()
    app.mainloop()
