import customtkinter as ctk
import tkinter as tk
from PIL import Image
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    FUNNEL,
    CROSS,
    PINK,
    BLUE,
    BLUE_HOVER,
    VIOLET,
    PINK_HOVER,
    VIOLET_HOVER,
    GREEN,
)
from ..components.avatar import Avatar
from ..components.messagebox import MessageBox as mb
from ..components.data_table import DataTable
from ..components.rectangle import Rectangle
from receipts.thermal_receipt import ThermalPrinter


class RecordsPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color="transparent",
            # fg_color="#F8FAFC",
            # border_width=2,
            # border_color="#E2E8F0",
            # corner_radius=15,
        )
        self.controller = controller
        self.admin_db = controller.admin_db

        self.filter_icon = ctk.CTkImage(Image.open(FUNNEL), size=(30, 30))
        self.cross_icon = ctk.CTkImage(Image.open(CROSS), size=(26, 26))

        self.record_filter_frame = ctk.CTkFrame(
            self,
            height=230,
            width=1450,
            fg_color="#E2E8F0",
            corner_radius=20,
        )
        self.record_filter_frame.place(x=0, y=10)
        Avatar(
            self.record_filter_frame,
            width=60,
            height=60,
            image=self.filter_icon,
            fg_color=VIOLET,
        ).place(x=30, y=20)
        ctk.CTkLabel(
            self.record_filter_frame,
            text=" Record Filters",
            font=("Poppins", 22, "bold"),
            text_color="#1E293B",
        ).place(x=100, y=30)

        ctk.CTkLabel(
            self.record_filter_frame,
            text="Search",
            font=("Poppins", 18),
            text_color="#1E293B",
        ).place(x=31, y=110)

        self.search_entry = ctk.CTkEntry(
            self.record_filter_frame,
            width=360,
            height=50,
            corner_radius=9,
            font=("Inter", 18),
            fg_color="#D3D9E2",
            text_color="#1E293B",
            placeholder_text="Search records...",
            placeholder_text_color="#64748B",
            border_width=0,
        )

        self.delete_search_btn = ctk.CTkButton(
            self.record_filter_frame,
            text="",
            image=self.cross_icon,
            fg_color="#D3D9E2",
            width=0,
            bg_color="#D3D9E2",
            hover=False,
            cursor="hand2",
            command=self.delete_search,
        )
        self.search_entry.place(x=30, y=140)
        self.delete_search_btn.place(x=340, y=148)

        ctk.CTkLabel(
            self.record_filter_frame,
            text="Test Classification",
            font=("Poppins", 18),
            text_color="#1E293B",
        ).place(x=511, y=110)

        self.test_var = ctk.StringVar(value="All")

        self.filter_test_menu = ctk.CTkOptionMenu(
            self.record_filter_frame,
            values=["All", "Safe", "Mild", "Moderate", "Severe"],
            variable=self.test_var,
            width=230,
            height=50,
            font=("Inter", 18),
            fg_color="#D3D9E2",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Inter", 20),
            corner_radius=9,
            command=lambda value: self.apply_filters(),
        )

        self.filter_test_menu.place(x=510, y=140)

        ctk.CTkLabel(
            self.record_filter_frame,
            text="Eye Classification",
            font=("Poppins", 18),
            text_color="#1E293B",
        ).place(x=851, y=110)

        self.eye_var = ctk.StringVar(value="All")

        self.filter_eye_menu = ctk.CTkOptionMenu(
            self.record_filter_frame,
            values=["All", "Safe", "Mild", "Moderate", "Severe"],
            variable=self.eye_var,
            width=230,
            height=50,
            font=("Inter", 18),
            fg_color="#D3D9E2",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Inter", 20),
            corner_radius=9,
            command=lambda value: self.apply_filters(),
        )

        self.filter_eye_menu.place(x=850, y=140)

        ctk.CTkLabel(
            self.record_filter_frame,
            text="Risk Level",
            font=("Poppins", 18),
            text_color="#1E293B",
        ).place(x=1191, y=110)
        self.risk_var = ctk.StringVar(value="All")

        self.filter_risk_menu = ctk.CTkOptionMenu(
            self.record_filter_frame,
            values=["All", "Safe", "Mild", "Moderate", "Severe"],
            variable=self.risk_var,
            width=230,
            height=50,
            font=("Inter", 18),
            fg_color="#D3D9E2",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Inter", 20),
            corner_radius=9,
            command=lambda value: self.apply_filters(),
        )
        self.filter_risk_menu.place(x=1190, y=140)

        self.table_container = ctk.CTkFrame(
            self,
            width=1450,
            height=650,
            corner_radius=20,
            fg_color="#E2E8F0",
        )
        self.table_container.place(x=0, y=265)
        self.records_table = ctk.CTkFrame(
            self.table_container,
            fg_color="transparent",
            width=1410,
            height=610,
        )
        self.records_table.pack(fill="both", expand=True, padx=20, pady=20)
        self.records_table.pack_propagate(False)

        self.table_headers = [
            "Diagnostic ID",
            "Temperature",
            "Test Classification",
            "Eye  Classification",
            "Risk Level",
            "Actions",
        ]
        self.table_data = []
        self.table_actions = [
            {
                "text": "View",
                # "icon": self.view_icon,
                "color": BLUE,
                "hover": BLUE_HOVER,
                "command": self.view_record,
            },
            {
                "text": "Print",
                # "icon": self.print_icon,
                "color": PINK,
                "hover": PINK_HOVER,
                "command": self.print_record,
            },
        ]

        table_container = ctk.CTkScrollableFrame(
            self.records_table,
            fg_color="#E2E8F0",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        table_container.pack(fill="both", expand=True)
        self.table = DataTable(
            table_container,
            headers=self.table_headers,
            data=self.table_data,
            actions=self.table_actions,
            table_width=232,
            header_color=GREEN,
            row_color="#FFFFFF",
        )

        self.table.pack(
            fill="both",
            expand=True,
        )
        self.search_entry.bind("<KeyRelease>", lambda e: self.apply_filters())

    def apply_filters(self):
        keyword = self.search_entry.get().strip()
        test_class = self.test_var.get()
        eye_class = self.eye_var.get()
        risk_level = self.risk_var.get()

        records = self.admin_db.filter_records(
            keyword,
            test_class,
            eye_class,
            risk_level,
        )
        records = records or []

        self.full_records = records

        if records:
            table_data = [r.get("display", ("-", "-", "-", "-", "-")) for r in records]
        else:
            table_data = [("No Results", "-", "-", "-", "-", "-")]

        self.table.update_data(table_data)

    def delete_search(self):
        self.search_entry.delete(0, ctk.END)
        self.on_show()

    def clear_fields(self):
        self.search_entry.delete(0, ctk.END)
        self.test_var.set("All")
        self.eye_var.set("All")
        self.risk_var.set("All")

    def on_show(self):
        user = self.controller.current_user

        if not user:
            return

        user_id = user[0]
        records = self.controller.db.fetch_patient_records(user_id) or []

        # ✅ store full records
        self.full_records = records

        if records:
            self.table_data = [
                r.get("display", ("-", "-", "-", "-", "-")) for r in records
            ]
        else:
            self.table_data = [("No Data", "-", "-", "-", "-")]

        self.table.update_data(self.table_data)

        self.search_entry.configure(placeholder_text="Search records...")

    def view_record(self, index):

        record = self.full_records[index]

        x = self.record_filter_frame.winfo_rootx()
        y = self.record_filter_frame.winfo_rooty()

        self.top = RecordModal(self, row=record["full"], x=x, y=y)  # ✅ PASS DATA

        self.top.title("View Record")

        self.top.geometry(f"1400x700+{x}+{y}")

    def print_record(self, index):
        record = self.full_records[index]["full"]

        diagnostic_id = record["id"]

        data = self.controller.db.print_patient_results_table(diagnostic_id)

        if not data:
            print("No data to print")
            return

        printer = ThermalPrinter(
            device="/dev/usb/lp0", created_at=data.get("created_at")
        )

        printer.print_report(
            patient_id=data.get("patient_id", "N/A"),
            patient_name=data.get("patient_name", "N/A"),
            temperature=data.get("temperature", 0),
            contact_number=data.get("contact_number", "N/A"),
            test_result=data.get("test_result", "N/A"),
            test_conf=data.get("test_conf", 0),
            eye_classification=data.get("eye_classification", "N/A"),
            eye_conf=data.get("eye_conf", 0),
            risk_level=data.get("risk_level", "N/A"),
            recommendation=data.get("recommendation") or "No recommendation available",
        )

        printer.close()


class RecordModal(ctk.CTkToplevel):
    def __init__(self, master, row=None, x=100, y=100, *args, **kwargs):
        super().__init__(master, fg_color="#FFFFFF", *args, **kwargs)

        self.row = row
        self.pos_x = x
        self.pos_y = y

        self.build_ui()
        self.populate_data()

        # ✅ IMPORTANT: set geometry AFTER window is ready
        self.after(50, self.set_position)

        self.after(100, self.safe_grab)

    def set_position(self):
        width = 1400
        height = 700
        self.geometry(f"{width}x{height}+{self.pos_x}+{self.pos_y}")

    def safe_grab(self):
        try:
            self.grab_set()
        except:
            pass

    def build_ui(self):

        ctk.CTkLabel(self, text="Record Details", font=("Inter", 22, "bold")).place(
            x=30, y=20
        )
        self.id_badge = Rectangle(
            self,
            width=190,
            height=50,
            corner_radius=8,
            text="Diagnostic Id:",
            fg_color="#14B8A6",
            text_color="#FFFFFF",
            font=("Inter", 15, "bold"),
        )
        self.id_badge.place(x=1185, y=20)

        ctk.CTkLabel(
            self,
            text="Date Created",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=30, y=70)

        self.date_created_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.date_created_entry.place(x=30, y=110)

        ctk.CTkLabel(
            self,
            text="Temperature",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=360, y=70)

        self.temperature_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.temperature_entry.place(x=360, y=110)

        ctk.CTkLabel(
            self,
            text="Test Classification",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=30, y=170)

        self.test_class_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.test_class_entry.place(x=30, y=210)

        ctk.CTkLabel(
            self,
            text="Test Confidence",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=360, y=170)

        self.test_conf_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.test_conf_entry.place(x=360, y=210)

        ctk.CTkLabel(
            self,
            text="Eye Classification",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=30, y=270)

        self.eye_class_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.eye_class_entry.place(x=30, y=310)

        ctk.CTkLabel(
            self,
            text="Eye Confidence",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=360, y=270)

        self.eye_conf_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.eye_conf_entry.place(x=360, y=310)

        ctk.CTkLabel(
            self,
            text="Test Contributing Factors",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=30, y=370)

        self.test_factors_text_box = ctk.CTkTextbox(
            self,
            width=300,
            height=200,
            corner_radius=9,
            fg_color="#E2E8F0",
            border_spacing=5,
            font=("Roboto", 18),
            text_color="#111827",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        self.test_factors_text_box.place(x=30, y=410)

        ctk.CTkLabel(
            self,
            text="Test Answers",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=360, y=370)

        self.test_answers_text_box = ctk.CTkTextbox(
            self,
            width=300,
            height=200,
            corner_radius=9,
            fg_color="#E2E8F0",
            border_spacing=5,
            font=("Roboto", 18),
            text_color="#111827",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        self.test_answers_text_box.place(x=360, y=410)

        ctk.CTkLabel(
            self,
            text="Eye Image",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=700, y=70)

        self.eye_image_container = ctk.CTkFrame(
            self, width=320, height=230, corner_radius=9
        )
        self.eye_image_container.place(x=700, y=110)
        self.eye_image = ctk.CTkFrame(
            self.eye_image_container,
            height=200,
            width=300,
            fg_color="transparent",
        )
        self.eye_image.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.eye_label = ctk.CTkLabel(self.eye_image, text="")
        self.eye_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self,
            text="Eye Scan",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=1050, y=70)

        self.eye_scan_container = ctk.CTkFrame(
            self,
            width=320,
            height=230,
            corner_radius=9,
            # fg_color="#F8FAFC",
            # border_color="#E2E8F0",
        )
        self.eye_scan_container.place(x=1050, y=110)
        self.eye_scan = ctk.CTkFrame(
            self.eye_scan_container,
            height=200,
            width=300,
            fg_color="transparent",
        )
        self.eye_scan.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.eye_scan_label = ctk.CTkLabel(self.eye_scan, text="")
        self.eye_scan_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self,
            text="Risk Level",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=700, y=350)

        self.risk_level_entry = ctk.CTkEntry(
            self,
            width=320,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.risk_level_entry.place(x=700, y=390)

        ctk.CTkLabel(
            self,
            text="Recommendation",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=700, y=450)

        self.recommendation_text_box = ctk.CTkTextbox(
            self,
            width=670,
            height=120,
            corner_radius=9,
            fg_color="#E2E8F0",
            border_spacing=5,
            font=("Roboto", 18),
            text_color="#111827",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        self.recommendation_text_box.place(x=700, y=490)

        ctk.CTkButton(
            self,
            width=170,
            height=50,
            text="Close",
            fg_color="#EF4444",
            font=("Inter", 18, "bold"),
            command=lambda: self.destroy(),
        ).place(x=1200, y=630)

    def populate_data(self):

        from datetime import datetime

        data = self.row

        diag_id = data.get("id")
        formatted_id = f"D{int(diag_id)}" if diag_id else "N/A"
        self.id_badge.set_text(f"Diagnostic ID: {formatted_id}")

        # ✅ FORMAT DATE
        raw_date = data.get("created_at")
        if raw_date:
            try:
                if isinstance(raw_date, str):
                    raw_date = datetime.fromisoformat(raw_date)

                formatted_date = raw_date.strftime("%b %d, %Y | %I:%M %p")
            except:
                formatted_date = str(raw_date)
        else:
            formatted_date = "N/A"

        self.date_created_entry.insert(0, formatted_date)
        self.date_created_entry.configure(state="disabled")

        self.temperature_entry.insert(0, str(data.get("temp", "")))
        self.temperature_entry.configure(state="disabled")

        self.test_class_entry.insert(0, str(data.get("test_class", "")))
        self.test_class_entry.configure(state="disabled")

        self.test_conf_entry.insert(0, str(data.get("test_conf", "")))
        self.test_conf_entry.configure(state="disabled")

        self.eye_class_entry.insert(0, str(data.get("eye_class", "")))
        self.eye_class_entry.configure(state="disabled")

        self.eye_conf_entry.insert(0, str(data.get("eye_conf", "")))
        self.eye_conf_entry.configure(state="disabled")

        self.risk_level_entry.insert(0, str(data.get("risk", "")))
        self.risk_level_entry.configure(state="disabled")

        self.load_ctk_image(data.get("eye_image"), self.eye_label)
        self.load_ctk_image(data.get("eye_scan"), self.eye_scan_label)

        import json

        self.test_factors_text_box.insert(
            "0.0", json.dumps(data.get("factors", []), indent=2)
        )
        self.test_factors_text_box.configure(state="disabled")

        self.test_answers_text_box.insert(
            "0.0", json.dumps(data.get("answers", []), indent=2)
        )
        self.test_answers_text_box.configure(state="disabled")

        self.recommendation_text_box.insert(
            "0.0",
            str(data.get("recommendation", "")),
        )
        self.recommendation_text_box.configure(state="disabled")

    def load_ctk_image(self, path, label, size=(350, 240)):
        from PIL import Image

        if not path:
            return

        try:
            # Load from file path
            img = Image.open(path)

            # Resize
            img = img.resize(size)

            # Convert to CTkImage
            ctk_img = ctk.CTkImage(light_image=img, size=size)

            # ⚠️ IMPORTANT: store reference
            label.image = ctk_img

            # Display
            label.configure(image=ctk_img, text="")

        except Exception as e:
            print("IMAGE LOAD ERROR:", e)
