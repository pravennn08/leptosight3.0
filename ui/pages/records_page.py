import customtkinter as ctk
import tkinter as tk
from PIL import Image
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    GREEN,
    CAMERA,
    FLASH,
    SAVE,
    CHECK,
    BLUE,
    RED,
    EYE,
    DISTANCE,
    PRIMARY,
    CAMERA_TIPS,
    CAMERA_PROMPT,
    RECOMMENDATIONS,
    SECONDARY,
    QUESTIONS,
    CHEVRON_LEFT,
    CHEVRON_RIGHT,
    YELLOW,
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

        ctk.CTkLabel(
            self, text="Records", font=("Arial", 33, "bold"), text_color=TEXT_PRIMARY
        ).place(x=40, y=10)
        ctk.CTkLabel(
            self,
            text="Please center your eye in the frame and hold steady while the scan is in progress.",
            font=("Poppins", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=40, y=60)

        self.actions_frame = ctk.CTkFrame(
            self, width=1400, height=100, fg_color="transparent"
        )
        self.actions_frame.place(x=40, y=120)

        self.search_btn = ctk.CTkButton(
            self.actions_frame,
            text="Search",
            font=("Inter", 15, "bold"),
            text_color="#FFFFFF",
            width=150,
            height=55,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            corner_radius=9,
            command=self.handle_search,
        )
        self.search_btn.place(x=560, y=35)

        self.search_entry = ctk.CTkEntry(
            self.actions_frame,
            width=540,
            height=55,
            corner_radius=9,
            font=("Roboto", 17),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            text_color=TEXT_PRIMARY,
            border_width=2,
        )
        self.search_entry.place(x=5, y=35)
        self.search_entry.bind("<KeyRelease>", lambda e: self.handle_search())

        self.table_container = ctk.CTkFrame(
            self,
            width=1400,
            height=670,
            fg_color="transparent",
        )
        self.table_container.place(x=40, y=230)

        self.records_table = ctk.CTkFrame(
            self.table_container,
            fg_color="transparent",
            width=1400,
            height=670,
        )

        self.records_table.pack(fill="both", expand=True)
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
                "color": "#3B82F6",
                "hover": "#2563EB",
                "command": self.view_record,
            },
            {
                "text": "Print",
                # "icon": self.print_icon,
                "color": "#DC2626",
                "hover": "#B91C1C",
                "command": self.print_record,
            },
        ]

        table_container = ctk.CTkScrollableFrame(
            self.records_table,
            fg_color="#E2E8F0",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        table_container.pack(fill="both", expand=True, pady=(10))

        self.table = DataTable(
            table_container,
            headers=self.table_headers,
            data=self.table_data,
            actions=self.table_actions,
            table_width=230,
            header_color=GREEN,
            row_color="#FFFFFF",
        )

        self.table.pack(
            fill="both",
            expand=True,
        )

    def handle_search(self):
        user = self.controller.current_user

        if not user:
            return

        user_id = user[0]
        keyword = self.search_entry.get().strip()

        if not keyword:
            records = self.controller.db.fetch_patient_records(user_id)
        else:
            records = self.controller.db.search_patient_records(user_id, keyword)

        records = records or []
        self.full_records = records
        if records:
            table_data = [r.get("display", ("-", "-", "-", "-", "-")) for r in records]
        else:
            table_data = [("No Results", "-", "-", "-", "-")]

        self.table.update_data(table_data)

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

        x = self.actions_frame.winfo_rootx()
        y = self.actions_frame.winfo_rooty()

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
