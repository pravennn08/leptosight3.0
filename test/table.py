# import customtkinter
# from CTkTable import *

# customtkinter.set_appearance_mode("light")

# root = customtkinter.CTk()
# root.geometry("800x400")
# root.configure(fg_color="#F4F7F9")

# def on_click(value):
#     print(f"Clicked value: {value}")

# values = [
#     ["Patient ID", "Name", "Eye Status", "Risk Level", "Date"],
#     ["001", "Juan Dela Cruz", "Normal", "SAFE ✅", "2026-04-10"],
#     ["002", "Maria Santos", "Dry Eyes", "MILD ⚠️", "2026-04-10"],
#     ["003", "Pedro Reyes", "Strain", "MODERATE ⚠️", "2026-04-09"],
#     ["004", "Ana Lopez", "Blurred Vision", "SEVERE 🔴", "2026-04-08"],
# ]

# table = CTkTable(
#     master=root,
#     values=values,
#     row=len(values),
#     column=len(values[0]),

#     colors=["#FFFFFF", "#F9FAFB"],
#     header_color="#22A699",
#     hover_color="#D1FAE5",

#     corner_radius=12,
#     justify="center",
#     font=("Segoe UI", 12),

#     command=on_click   # ✅ FIX HERE (NOT in configure)
# )

# table.pack(padx=20, pady=20)

# root.mainloop()

import customtkinter as ctk

class TableUI(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.place(x=40, y=230)

        self.data = [
            ["DX-001", "36.8", "Negative", "98.5%", "Normal", "97.2%"],
            ["DX-002", "37.5", "Suspected", "85.3%", "Dry Eyes", "88.1%"],
            ["DX-003", "38.2", "Positive", "92.7%", "Strain", "90.4%"],
            ["DX-004", "39.1", "Positive", "96.2%", "Blurred Vision", "94.8%"],
            ["DX-005", "36.5", "Negative", "99.1%", "Normal", "98.6%"],
        ]

        self.headers = [
            "Diagnostic ID", "Temp (°C)", "Test Class",
            "Test Conf", "Eye Class", "Eye Conf", "Action"
        ]

        self.build_table()

    def build_table(self):
        # Header
        for col, text in enumerate(self.headers):
            label = ctk.CTkLabel(
                self,
                text=text,
                fg_color="#22A699",
                text_color="white",
              
                font=("Segoe UI", 13, "bold"),
                width=150,
                height=40
            )
            label.grid(row=0, column=col, padx=0, pady=5, sticky="nsew")

        # Rows
        for row_index, row_data in enumerate(self.data, start=1):
            for col_index, value in enumerate(row_data):
                cell = ctk.CTkLabel(
                    self,
                    text=value,
                    fg_color="red" if row_index % 2 == 0 else "blue",
                    text_color="#1F2937",
                    corner_radius=6,
                    width=150,
                    height=40
                )
                cell.grid(row=row_index, column=col_index, padx=5, pady=5, sticky="nsew")

            # 🔥 ACTION COLUMN (REAL BUTTONS)
            action_frame = ctk.CTkFrame(self, fg_color="transparent")
            action_frame.grid(row=row_index, column=len(self.headers)-1, padx=5, pady=5)

            view_btn = ctk.CTkButton(
                action_frame,
                text="View",
                width=60,
                height=30,
                fg_color="#22A699",
                hover_color="#1B8F82",
                command=lambda r=row_data: self.view_record(r)
            )
            view_btn.pack(side="left", padx=2)

            print_btn = ctk.CTkButton(
                action_frame,
                text="Print",
                width=60,
                height=30,
                fg_color="#3B82F6",
                hover_color="#2563EB",
                command=lambda r=row_data: self.print_record(r)
            )
            print_btn.pack(side="left", padx=2)

        # Make columns expand evenly
        for col in range(len(self.headers)):
            self.grid_columnconfigure(col, weight=1)

    def view_record(self, row):
        print("VIEW:", row)

    def print_record(self, row):
        print("PRINT:", row)


# RUN
root = ctk.CTk()
root.geometry("1200x600")
root.configure(fg_color="#F4F7F9")

table = TableUI(root)

root.mainloop()