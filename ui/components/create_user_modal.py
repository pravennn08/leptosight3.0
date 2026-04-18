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
from CTkMessagebox import CTkMessagebox as mb


class CreateUserModal(ctk.CTkToplevel):
    def __init__(self, master, controller, x=100, y=100, *args, **kwargs):
        super().__init__(master, fg_color="#FFFFFF", *args, **kwargs)
        self.controller = controller

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
            height=560,
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
            text="Add User",
            font=("Inter", 22, "bold"),
            text_color="#1E293B",
        ).place(x=10, y=90)

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
            placeholder_text="Full Name",
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
            placeholder_text="Email",
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
            placeholder_text="Phone Number",
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
            font=("Roboto", 18),
            text_color="#1E293B",
            fg_color="#E2E8F0",
            border_width=0,
            placeholder_text="Password",
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

        self.create_acc_button = ctk.CTkButton(
            self.container,
            width=190,
            height=50,
            text="Create Account",
            fg_color="#14B8A6",
            hover_color="#0D9488",
            text_color="#FFFFFF",
            font=("Inter", 18, "bold"),
            corner_radius=9,
            command=self.add_account,
        )
        self.create_acc_button.place(x=790, y=490)

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
        ).place(x=610, y=490)

    def validate_data(self):
        name = self.full_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone_number = self.phone_number_entry.get().strip()
        role = self.role_option_menu.get().lower()
        valid_roles = ["patient", "personnel", "admin"]
        password = self.password_entry.get()

        if not name or not email or not phone_number or not password:
            return "All fields are required."

        if len(name) < 2:
            return "Full name is too short."

        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}$"
        if not re.match(email_pattern, email):
            return "Please enter a valid email address."

        if not phone_number.isdigit() or len(phone_number) != 11:
            return "Phoine number must be 11 digits (ex: 09123456789)."

        if not role or role not in valid_roles:
            return "Please select a valid role."

        if len(password) < 8:
            return "Password must be at least 8 characters long."

        return None

    def add_account(self):

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

        name = self.full_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_number_entry.get().strip()
        password = self.password_entry.get().strip()

        role = self.role_option_menu.get().lower()
        status_text = self.status_option_menu.get()
        is_verified = status_text == "Verified"

        # =========================
        # 🔥 VALIDATION
        # =========================

        # =========================
        # CREATE MODEL
        # =========================
        user = User(
            name=name,
            email=email,
            phone_number=phone,
            password=password,
            role=role,
            is_verified=is_verified,
        )

        # =========================
        # CALL SERVICE
        # =========================
        result = self.controller.admin_db.add_account(user)

        # =========================
        # HANDLE RESULT
        # =========================
        if isinstance(result, tuple):  # success

            mb(
                self.controller,
                title="Error",
                message="User created successfully",
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
                message="Phone already exists",
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
                message="Failed to create user",
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
        height = 590
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
