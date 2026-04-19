import customtkinter as ctk
from PIL import Image
import json
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    RED,
    PRIMARY,
    RED_HOVER,
    GREEN,
    GREEN_HOVER,
    EYE,
    LOGO,
)
from CTkMessagebox import CTkMessagebox as mb
from ..components.square import Square
from ..components.rectangle import Rectangle
from receipts.thermal_receipt import ThermalPrinter


class UpdateRecordModal(ctk.CTkToplevel):
    def __init__(self, master, row, controller, x=100, y=100, *args, **kwargs):
        super().__init__(master, fg_color="#FFFFFF", *args, **kwargs)
        self.controller = controller
        self.row = row
        self.pos_x = x
        self.pos_y = y

        self.eye_icon = ctk.CTkImage(Image.open(EYE), size=(35, 35))
        # self.percent_icon = ctk.CTkImage(Image.open(PERCENT), size=(35, 35))

        self.after(50, self.set_position)
        self.after(100, self.safe_grab)
        # SYSTEM LOGO
        self.logo_img = ctk.CTkImage(
            light_image=Image.open(LOGO),
            size=(51, 51),
        )

        self.container = ctk.CTkFrame(
            self,
            width=1410,
            height=850,
            # fg_color="#E2E8F0",
            fg_color="transparent",
        )
        self.container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        Square(
            self.container,
            size=60,
            image=self.logo_img,
            fg_color=PRIMARY,
        ).place(x=10, y=0)
        ctk.CTkLabel(
            self.container,
            text="LeptoSight",
            font=("Inter", 22, "bold"),
            text_color=TEXT_PRIMARY,
        ).place(x=90, y=5)

        ctk.CTkLabel(
            self.container,
            text="An AI-Powered for Early Detection of Leptospirosis",
            font=("Inter", 16),
            wraplength=670,
            justify="left",
            text_color=TEXT_SECONDARY,
        ).place(x=90, y=30)

        ctk.CTkLabel(
            self.container,
            text="Update Record",
            font=("Inter", 22, "bold"),
            text_color="#1E293B",
        ).place(x=10, y=90)

        self.id_badge = Rectangle(
            self.container,
            width=190,
            height=40,
            corner_radius=8,
            text="Diagnostic ID: N/A",
            fg_color="#EC4899",
            text_color="#FFFFFF",
            font=("Inter", 15, "bold"),
        )
        self.id_badge.place(x=1210, y=0)

        ctk.CTkLabel(
            self.container,
            text="Patient Name",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=130)

        self.user_id_badge = Rectangle(
            self.container,
            width=130,
            height=35,
            corner_radius=7,
            text="Patient ID: N/A",
            fg_color="#8B5CF6",
            text_color="#FFFFFF",
            font=("Inter", 13, "bold"),
        )
        self.user_id_badge.place(x=180, y=125)

        self.full_name_entry = ctk.CTkEntry(
            self.container,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            text_color="#1E293B",  # dark readable text
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.full_name_entry.place(x=10, y=170)

        ctk.CTkLabel(
            self.container,
            text="Patient Phone Number",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=361, y=130)

        self.phone_number_entry = ctk.CTkEntry(
            self.container,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            border_width=0,
            fg_color="#E2E8F0",
            text_color="#1E293B",  # dark readable text
        )
        self.phone_number_entry.place(x=360, y=170)

        ctk.CTkLabel(
            self.container,
            text="Date Created",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=235)

        self.date_created_entry = ctk.CTkEntry(
            self.container,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            border_width=0,
            fg_color="#E2E8F0",
            text_color="#1E293B",
        )
        self.date_created_entry.place(x=10, y=275)

        ctk.CTkLabel(
            self.container,
            text="Temperature",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=361, y=235)

        self.temperature_entry = ctk.CTkEntry(
            self.container,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            border_width=0,
            fg_color="#E2E8F0",
            text_color="#1E293B",
        )
        self.temperature_entry.place(x=360, y=275)

        ctk.CTkLabel(
            self.container,
            text="Test Classification",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=340)

        # self.test_class_entry = ctk.CTkEntry(
        #     self.container,
        #     width=300,
        #     height=50,
        #     corner_radius=9,
        #     font=("Roboto", 18),
        #     border_width=0,
        #     fg_color="#E2E8F0",
        #     text_color="#1E293B",
        # )
        # self.test_class_entry.place(x=10, y=380)

        self.test_class_var = ctk.StringVar(value="Safe")
        self.test_class_menu = ctk.CTkOptionMenu(
            self.container,
            values=["Safe", "Mild", "Moderate", "Severe"],
            variable=self.test_class_var,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#E2E8F0",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Roboto", 19),
        )
        self.test_class_menu.place(x=10, y=380)

        ctk.CTkLabel(
            self.container,
            text="Test Confidence",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=361, y=340)

        self.test_conf_entry = ctk.CTkEntry(
            self.container,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            border_width=0,
            fg_color="#E2E8F0",
            text_color="#1E293B",
        )
        self.test_conf_entry.place(x=360, y=380)

        ctk.CTkLabel(
            self.container,
            text="Eye Classification",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=445)

        # self.eye_class_entry = ctk.CTkEntry(
        #     self.container,
        #     width=300,
        #     height=50,
        #     corner_radius=9,
        #     font=("Roboto", 18),
        #     border_width=0,
        #     fg_color="#E2E8F0",
        #     text_color="#1E293B",
        # )
        # self.eye_class_entry.place(x=10, y=485)
        self.eye_class_var = ctk.StringVar(value="Safe")
        self.eye_class_menu = ctk.CTkOptionMenu(
            self.container,
            values=["Safe", "Mild", "Moderate", "Severe"],
            variable=self.eye_class_var,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#E2E8F0",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Roboto", 19),
        )
        self.eye_class_menu.place(x=10, y=485)

        ctk.CTkLabel(
            self.container,
            text="Eye Confidence",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=361, y=445)

        self.eye_conf_entry = ctk.CTkEntry(
            self.container,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            border_width=0,
            fg_color="#E2E8F0",
            text_color="#1E293B",
        )
        self.eye_conf_entry.place(x=360, y=485)

        ctk.CTkLabel(
            self.container,
            text="Test Contributing Factors",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=550)

        self.test_factors_text_box = ctk.CTkTextbox(
            self.container,
            width=300,
            height=200,
            corner_radius=9,
            fg_color="#E2E8F0",
            border_spacing=5,
            font=("Roboto", 18),
            text_color="#1E293B",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        self.test_factors_text_box.place(x=10, y=590)

        ctk.CTkLabel(
            self.container,
            text="Test Answers",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=360, y=550)

        self.test_answers_text_box = ctk.CTkTextbox(
            self.container,
            width=300,
            height=200,
            corner_radius=9,
            fg_color="#E2E8F0",
            border_spacing=5,
            font=("Roboto", 18),
            text_color="#1E293B",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        self.test_answers_text_box.place(x=360, y=590)

        ctk.CTkLabel(
            self.container,
            text="Eye Image",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=711, y=130)

        self.eye_image_container = ctk.CTkFrame(
            self.container,
            width=320,
            height=230,
            corner_radius=9,
            fg_color="#E2E8F0",
        )
        self.eye_image_container.place(x=710, y=170)
        self.eye_image = ctk.CTkFrame(
            self.eye_image_container,
            width=300,
            height=210,
            fg_color="transparent",
        )
        self.eye_image.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.eye_label = ctk.CTkLabel(self.eye_image, text="")
        self.eye_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self.container,
            text="Eye Scan",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=1080, y=130)

        self.eye_scan_container = ctk.CTkFrame(
            self.container,
            width=320,
            height=230,
            corner_radius=9,
            fg_color="#E2E8F0",
        )
        self.eye_scan_container.place(x=1080, y=170)
        self.eye_scan = ctk.CTkFrame(
            self.eye_scan_container,
            width=300,
            height=210,
            fg_color="transparent",
        )
        self.eye_scan.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.eye_scan_label = ctk.CTkLabel(self.eye_scan, text="")
        self.eye_scan_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self.container,
            text="Risk Level",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=711, y=415)

        # self.risk_level_entry = ctk.CTkEntry(
        #     self.container,
        #     width=320,
        #     height=50,
        #     corner_radius=9,
        #     font=("Roboto", 18),
        #     border_width=0,
        #     fg_color="#E2E8F0",
        #     text_color="#1E293B",
        # )
        # self.risk_level_entry.place(x=710, y=455)

        self.risk_level_var = ctk.StringVar(value="Safe")
        self.risk_level_menu = ctk.CTkOptionMenu(
            self.container,
            values=["Safe", "Mild", "Moderate", "Severe"],
            variable=self.risk_level_var,
            width=320,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#E2E8F0",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8",
            text_color="#1E293B",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Roboto", 19),
        )
        self.risk_level_menu.place(x=710, y=455)

        ctk.CTkLabel(
            self.container,
            text="PDF Path",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=1081, y=415)

        self.pdf_path_entry = ctk.CTkEntry(
            self.container,
            width=320,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            border_width=0,
            fg_color="#E2E8F0",
            text_color="#1E293B",
        )
        self.pdf_path_entry.place(x=1080, y=455)

        ctk.CTkLabel(
            self.container,
            text="Recommendation",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=711, y=520)

        self.recommendation_text_box = ctk.CTkTextbox(
            self.container,
            width=690,
            height=150,
            corner_radius=9,
            fg_color="#E2E8F0",
            border_spacing=5,
            font=("Roboto", 18),
            text_color="#1E293B",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        self.recommendation_text_box.place(x=710, y=560)

        self.update_button = ctk.CTkButton(
            self.container,
            width=150,
            height=50,
            text="Update",
            fg_color="#14B8A6",
            hover_color="#0D9488",
            text_color="#FFFFFF",
            font=("Inter", 18, "bold"),
            command=self.update_record,
            corner_radius=9,
        )
        self.update_button.place(x=1250, y=740)

        ctk.CTkButton(
            self.container,
            width=150,
            height=50,
            text="Cancel",
            fg_color="#E2E8F0",
            hover_color="#CBD5E1",
            text_color="#1E293B",
            font=("Inter", 18, "bold"),
            corner_radius=9,
            command=lambda: self.destroy(),
        ).place(x=1070, y=740)

        self.print_record_btn = ctk.CTkButton(
            self.container,
            width=150,
            height=50,
            text="Print",
            fg_color=RED,
            hover_color=RED_HOVER,
            text_color="#FFFFFF",
            font=("Inter", 18, "bold"),
            corner_radius=9,
            command=self.print_record,
        )
        self.print_record_btn.place(x=710, y=740)

        self.populate_data()

    def populate_data(self):
        data = self.row
        user_id = data.get("patient_id")
        self.user_id_badge.set_text(f"User ID: {user_id}")

        diagnostic_id = data.get("id")
        self.id_badge.set_text(f"Diagnostic ID: {diagnostic_id}")

        self.full_name_entry.delete(0, "end")
        self.full_name_entry.insert(0, data.get("patient_name") or "")
        self.full_name_entry.configure(state=ctk.DISABLED)

        self.phone_number_entry.delete(0, "end")
        self.phone_number_entry.insert(0, data.get("contact_number") or "")
        self.phone_number_entry.configure(state=ctk.DISABLED)

        self.date_created_entry.delete(0, "end")
        self.date_created_entry.insert(0, self.format_datetime(data.get("created_at")))
        self.date_created_entry.configure(state="disabled")

        self.temperature_entry.delete(0, "end")
        self.temperature_entry.insert(0, str(data.get("temperature", "")))

        self.test_class_menu.set(data.get("test_result"))

        self.test_conf_entry.delete(0, "end")
        self.test_conf_entry.insert(0, str(data.get("test_conf", "")))
        self.test_conf_entry.configure(state="disabled")

        self.eye_class_menu.set(data.get("eye_classification"))

        self.eye_conf_entry.delete(0, "end")
        self.eye_conf_entry.insert(0, str(data.get("eye_conf", "")))
        self.eye_conf_entry.configure(state="disabled")

        self.test_factors_text_box.insert(
            "0.0", json.dumps(data.get("factors", []), indent=2)
        )
        self.test_factors_text_box.configure(state="disabled")

        self.test_answers_text_box.insert(
            "0.0", json.dumps(data.get("answers", []), indent=2)
        )
        self.test_answers_text_box.configure(state="disabled")

        self.load_ctk_image(data.get("eye_image"), self.eye_label)
        self.load_ctk_image(data.get("eye_scan"), self.eye_scan_label)

        self.risk_level_menu.set(data.get("risk_level"))

        self.pdf_path_entry.delete(0, "end")
        self.pdf_path_entry.insert(0, str(data.get("pdf_path", "")))
        self.pdf_path_entry.configure(state="disabled")

        self.recommendation_text_box.insert(
            "0.0",
            str(data.get("recommendation", "")),
        )
        self.recommendation_text_box.configure(state="disabled")

    def validate(self):
        temp_raw = self.temperature_entry.get().strip()

        if not temp_raw:
            return "Temperature is required"
        try:
            temp = float(temp_raw)
        except ValueError:
            return "Temperature must be a valid number (e.g., 36.5)"

        if temp < 30 or temp > 45:
            return "Temperature must be between 30°C and 45°C"

        test_class = self.test_class_menu.get()
        eye_class = self.eye_class_menu.get()
        risk_level = self.risk_level_menu.get()

        if test_class == "Select":
            return "Select test classification"

        if eye_class == "Select":
            return "Select eye classification"

        if risk_level == "Select":
            return "Select risk level"

        return None

    def update_record(self):
        error = self.validate()
        if error:
            mb(
                self.controller,
                title="Error",
                message=error,
                option_1="Okay",
                icon="cancel",
                fg_color="#FFFFFF",
                border_width=1,
                border_color="#E2E8F0",
                text_color="#0F172A",
                title_color="#0F172A",
                font=("Inter", 16),
                height=260,
                button_color="#14B8A6",
                button_hover_color="#0D9488",
                button_text_color="#FFFFFF",
                button_width=100,
                button_height=55,
            )
            return

        temp = self.temperature_entry.get()
        test_class = self.test_class_menu.get()
        eye_class = self.eye_class_menu.get()
        risk_level = self.risk_level_menu.get()

        record_id = self.row["id"]

        success = self.controller.admin_db.update_record(
            record_id,
            temp,
            test_class,
            eye_class,
            risk_level,
        )

        if success:

            mb(
                self.controller,
                title="Update Record",
                message="Record updated successfully",
                option_1="Thanks",
                icon="check",
                fg_color="#FFFFFF",
                border_width=1,
                border_color="#E2E8F0",
                text_color="#0F172A",
                title_color="#0F172A",
                font=("Inter", 16),
                height=260,
                button_color="#14B8A6",
                button_hover_color="#0D9488",
                button_text_color="#FFFFFF",
                button_width=100,
                button_height=55,
            )
            self.controller.frames["PatientRecordsPage"].on_show()
            self.destroy()

        else:
            mb(
                self.controller,
                title="Error",
                message="Update record failed",
                option_1="Okay",
                icon="cancel",
                fg_color="#FFFFFF",
                border_width=1,
                border_color="#E2E8F0",
                text_color="#0F172A",
                title_color="#0F172A",
                font=("Inter", 16),
                height=260,
                button_color="#14B8A6",
                button_hover_color="#0D9488",
                button_text_color="#FFFFFF",
                button_width=100,
                button_height=55,
            )

    def print_record(self):
        data = self.row
        diagnostic_id = data.get("id")
        if not data:
            print("No data to print")
            return

        msg = mb(
            self.controller,
            title="Print Record",
            message="Are you sure you want to print this record?",
            icon="warning",
            option_1="Print",
            option_2="Cancel",
            fg_color="#FFFFFF",
            border_width=1,
            border_color="#E2E8F0",
            text_color="#0F172A",
            title_color="#0F172A",
            font=("Inter", 16),
            height=260,
            button_color=GREEN,
            button_hover_color=GREEN_HOVER,
            button_text_color="#FFFFFF",
            button_width=100,
            button_height=55,
        )
        if msg.get() != "Print":
            return

        else:

            data = self.controller.db.print_patient_results_table(diagnostic_id)

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
                recommendation=data.get("recommendation")
                or "No recommendation available",
            )

            printer.close()

    def format_datetime(self, value):
        from datetime import datetime

        if not value:
            return "N/A"

        try:
            if isinstance(value, str):
                value = datetime.fromisoformat(value)

            return value.strftime("%b %d, %Y | %I:%M %p")
        except:
            return str(value)

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

    def set_position(self):
        width = 1450
        height = 880
        self.geometry(f"{width}x{height}+{self.pos_x}+{self.pos_y+30}")

    def safe_grab(self):
        try:
            self.grab_set()
        except:
            pass

    def close(self):
        try:
            self.grab_release()
        except:
            pass
        self.destroy()
