import customtkinter as ctk
from PIL import Image
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    EYE,
    LOGO,
    PRIMARY,
)
import re
from service.models.user_model import User

from ..components.square import Square
from ..components.rectangle import Rectangle
from CTkMessagebox import CTkMessagebox as mb


class UpdateUserModal(ctk.CTkToplevel):
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
            width=990,
            height=760,
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
            text="Update User",
            font=("Inter", 22, "bold"),
            text_color="#1E293B",
        ).place(x=10, y=90)

        self.id_badge = Rectangle(
            self.container,
            width=130,
            height=40,
            corner_radius=8,
            text="User ID: N/A",
            fg_color="#8B5CF6",
            text_color="#FFFFFF",
            font=("Inter", 15, "bold"),
        )
        self.id_badge.place(x=850, y=10)

        ctk.CTkLabel(
            self.container,
            text="Full Name",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=140)

        self.full_name_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            text_color="#1E293B",  # dark readable text
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.full_name_entry.place(x=10, y=180)

        ctk.CTkLabel(
            self.container,
            text="Email",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=581, y=140)

        self.email_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            border_width=0,
            fg_color="#E2E8F0",
            text_color="#1E293B",  # dark readable text
        )
        self.email_entry.place(x=580, y=180)

        ctk.CTkLabel(
            self.container,
            text="Phone Number",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=240)

        self.phone_number_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            text_color="#1E293B",  # dark readable text
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.phone_number_entry.place(x=10, y=280)

        ctk.CTkLabel(
            self.container,
            text="Role",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=581, y=240)

        self.roles = ctk.StringVar(value="Patient")
        self.role_option_menu = ctk.CTkOptionMenu(
            self.container,
            values=["Patient", "Personnel", "Admin"],
            variable=self.roles,
            width=400,
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
        self.role_option_menu.place(x=580, y=280)

        ctk.CTkLabel(
            self.container,
            text="Password",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=340)

        self.password_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 17),
            text_color="#1E293B",
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.password_entry.place(x=10, y=380)

        ctk.CTkLabel(
            self.container,
            text="Status",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=581, y=340)

        self.status = ctk.StringVar(value="Verified")
        self.status_option_menu = ctk.CTkOptionMenu(
            self.container,
            values=["Verified", "Pending"],
            variable=self.status,
            width=400,
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
        self.status_option_menu.place(x=580, y=380)

        ctk.CTkLabel(
            self.container,
            text="Last Login",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=440)

        self.last_login_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            text_color="#1E293B",  # dark readable text
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.last_login_entry.place(x=10, y=480)

        ctk.CTkLabel(
            self.container,
            text="Created At",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=581, y=440)

        self.created_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            text_color="#1E293B",  # dark readable text
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.created_entry.place(x=580, y=480)

        ctk.CTkLabel(
            self.container,
            text="Updated At",
            font=("Poppins", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=11, y=540)

        self.updated_entry = ctk.CTkEntry(
            self.container,
            width=400,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            text_color="#1E293B",  # dark readable text
            fg_color="#E2E8F0",
            border_width=0,
        )
        self.updated_entry.place(x=10, y=580)

        self.update_button = ctk.CTkButton(
            self.container,
            width=150,
            height=50,
            text="Save",
            fg_color="#14B8A6",
            hover_color="#0D9488",
            text_color="#FFFFFF",
            font=("Inter", 18, "bold"),
            command=self.update_account,
            corner_radius=9,
        )
        self.update_button.place(x=830, y=690)

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
        ).place(x=650, y=690)
        self.populate_data()

    def populate_data(self):

        data = self.row
        user_id = data.get("id")
        self.id_badge.set_text(f"User ID: {user_id}")

        self.full_name_entry.delete(0, "end")
        self.full_name_entry.insert(0, data.get("name") or "")

        self.email_entry.delete(0, "end")
        self.email_entry.insert(0, data.get("email") or "")

        self.phone_number_entry.delete(0, "end")
        self.phone_number_entry.insert(0, data.get("phone_number"))

        self.password_entry.insert(0, data.get("password"))
        self.password_entry.configure(state="disabled", show="*")

        role = data.get("role")
        self.role_option_menu.set(role.capitalize() if role else "Patient")

        verified = data.get("is_verified")
        is_verified = str(verified).lower() in ("true", "1", "t")
        self.status_option_menu.set("Verified" if is_verified else "Pending")

        self.created_entry.delete(0, "end")
        self.created_entry.insert(0, self.format_datetime(data.get("created_at")))
        self.created_entry.configure(state="disabled")

        self.updated_entry.delete(0, "end")
        self.updated_entry.insert(0, self.format_datetime(data.get("updated_at")))
        self.updated_entry.configure(state="disabled")

        self.last_login_entry.delete(0, "end")
        self.last_login_entry.insert(0, self.format_datetime(data.get("last_login_at")))
        self.last_login_entry.configure(state="disabled")

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

    def validate_data(self):
        name = self.full_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone_number = self.phone_number_entry.get().strip()
        role = self.role_option_menu.get().lower()

        valid_roles = ["patient", "personnel", "admin"]

        if not name or not email or not phone_number:
            return "All fields are required."

        if len(name) < 2:
            return "Full name is too short."

        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}$"
        if not re.match(email_pattern, email):
            return "Please enter a valid email address."

        if not (
            (
                phone_number.startswith("09")
                and phone_number.isdigit()
                and len(phone_number) == 11
            )
            or (
                phone_number.startswith("+639")
                and phone_number[1:].isdigit()
                and len(phone_number) == 13
            )
        ):
            return "Invalid phone format. Use 09123456789 or +639123456789"

        if role not in valid_roles:
            return "Please select a valid role."

        return None

    def update_account(self):

        error = self.validate_data()

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

        user_id = self.row.get("id")

        name = self.full_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_number_entry.get().strip()

        role = self.role_option_menu.get().lower()
        is_verified = self.status_option_menu.get() == "Verified"

        phone = User.normalize_phone(self.phone_number_entry.get().strip())

        result = self.controller.admin_db.update_user(
            user_id=user_id,
            name=name,
            email=email,
            phone_number=phone,
            role=role,
            is_verified=is_verified,
        )

        # =========================
        # 🔥 HANDLE RESPONSES
        # =========================
        if result == "USER_UPDATED":

            mb(
                self.controller,
                title="Save",
                message="User updated successfully",
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
            self.controller.frames["UsersPage"].on_show()
            self.destroy()

        elif result == "EMAIL_EXISTS":

            mb(
                self.controller,
                title="Error",
                message="Email already exists",
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

        elif result == "PHONE_EXISTS":

            mb(
                self.controller,
                title="Error",
                message="Phone number already exists",
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

        elif result == "USER_NOT_FOUND":
            mb(
                self.controller,
                title="Error",
                message="User not found",
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

        else:
            mb(
                self.controller,
                title="Error",
                message="Update failed",
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

    def set_position(self):
        width = 1030
        height = 790
        self.geometry(f"{width}x{height}+{self.pos_x +200}+{self.pos_y+30}")

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
