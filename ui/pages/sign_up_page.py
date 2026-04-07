import customtkinter as ctk
import re
from PIL import Image
from constants.seeds import (
    BACKGROUND,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    PRIMARY,
    SECONDARY,
    LOGO,
    DIVIDER,
)

from service.models.user_model import User
from ..components.messagebox import MessageBox as mb
from ..components.square import Square


class SignUpPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color=BACKGROUND,
        )
        self.controller = controller
        self.db = controller.db

        # SYSTEM LOGO
        self.logo_img = ctk.CTkImage(
            light_image=Image.open(LOGO),
            size=(71, 71),
        )

        # CARD CONTAINER
        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent",
            # fg_color="gray",
            # border_width=1,
            # border_color="#E2E8F0",
            # corner_radius=12,
            width=600,
            height=900,
        )
        self.container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # SYSTEM LOGO
        # ctk.CTkLabel(self.container, text="", image=self.logo_img).place(
        #     relx=0.5,
        #     y=0,
        #     anchor=ctk.N,
        # )
        Square(
            self.container,
            size=85,
            image=self.logo_img,
            fg_color=PRIMARY,
        ).place(relx=0.36, y=0, anchor=ctk.N)

        ctk.CTkLabel(
            self.container, text="LeptoSight", font=("Arial", 30, "bold")
        ).place(relx=0.62, y=30, anchor=ctk.N)

        # HEADER
        ctk.CTkLabel(
            self.container,
            text="Create an account",
            font=("Roboto", 22),
            text_color=TEXT_PRIMARY,
        ).place(x=30, y=120)

        # SUB HEADER
        ctk.CTkLabel(
            self.container,
            text="Enter your information below to create your account",
            font=("Roboto", 17.5),
            text_color=TEXT_SECONDARY,
        ).place(x=30, y=155)

        # NAME
        ctk.CTkLabel(
            self.container,
            text="Full Name",
            font=("Roboto", 18),
            text_color=TEXT_PRIMARY,
        ).place(x=30, y=200)

        # NAME ENTRY

        self.name_entry = ctk.CTkEntry(
            self.container,
            width=540,
            height=55,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            border_width=2,
        )
        self.name_entry.place(x=30, y=235)

        # EMAIL
        ctk.CTkLabel(
            self.container,
            text="Email",
            font=("Roboto", 18),
            text_color=TEXT_PRIMARY,
        ).place(x=30, y=300)

        # EMAIL ENTRY
        self.email_entry = ctk.CTkEntry(
            self.container,
            width=540,
            height=55,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            border_width=2,
        )
        self.email_entry.place(x=30, y=335)

        # PHONE NUMBER
        ctk.CTkLabel(
            self.container,
            text="Phone Number",
            font=("Roboto", 18),
            text_color=TEXT_PRIMARY,
        ).place(x=30, y=400)

        # # PHONE NUMBER ENTRY
        self.phone_number_entry = ctk.CTkEntry(
            self.container,
            width=540,
            height=55,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            border_width=2,
        )
        self.phone_number_entry.place(x=30, y=435)

        # ROLE
        ctk.CTkLabel(
            self.container,
            text="Role",
            font=("Roboto", 18),
            text_color=TEXT_PRIMARY,
        ).place(x=30, y=500)

        self.roles = ctk.StringVar(value="Patient")

        self.role_option = ctk.CTkOptionMenu(
            self.container,
            values=[
                "Patient",
                "Personnel",
                "Admin",
            ],
            variable=self.roles,
            font=("Roboto", 18),
            fg_color="#EEEFF0",
            text_color=TEXT_SECONDARY,
            button_color=PRIMARY,
            button_hover_color=SECONDARY,
            dropdown_text_color=TEXT_PRIMARY,
            dropdown_font=("Roboto", 18),
            corner_radius=9,
            dynamic_resizing=False,
            width=540,
            height=55,
        )
        self.role_option.place(x=30, y=535)

        # PASSWORD
        ctk.CTkLabel(
            self.container,
            text="Password",
            font=("Roboto", 18),
            text_color=TEXT_PRIMARY,
        ).place(x=30, y=600)

        # PASSWORD ENTRY
        self.password_entry = ctk.CTkEntry(
            self.container,
            width=260,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            border_width=2,
        )
        self.password_entry.place(x=30, y=635)

        # PASSWORD REQUIREMENT
        ctk.CTkLabel(
            self.container,
            text="Must be at least 8 characters long.",
            font=("Roboto", 16.5),
            text_color=TEXT_SECONDARY,
        ).place(x=35, y=690)

        # CONFIRM PASSWORD
        ctk.CTkLabel(
            self.container,
            text="Confirm Password",
            font=("Roboto", 18),
            text_color=TEXT_PRIMARY,
        ).place(x=311, y=600)

        # CONFIRM PASSWORD ENTRY
        self.confirm_password_entry = ctk.CTkEntry(
            self.container,
            width=260,
            height=55,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            border_width=2,
        )
        self.confirm_password_entry.place(x=310, y=635)

        self.signup_btn = ctk.CTkButton(
            self.container,
            text="Create Account",
            text_color=BACKGROUND,
            width=540,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            font=("Inter", 20, "bold"),
            height=60,
            corner_radius=10,
            cursor="hand2",
            border_color="#E5E7EB",
            command=self.sign_up,
        )
        self.signup_btn.place(x=30, y=750)

        # TO SIGN UP
        ctk.CTkLabel(
            self.container,
            text="Don't have an account?",
            text_color=TEXT_SECONDARY,
            font=("Roboto", 18),
        ).place(x=265, y=820, anchor=ctk.N)

        ctk.CTkButton(
            self.container,
            text="Sign in",
            width=0,
            fg_color="transparent",
            hover=False,
            text_color=PRIMARY,
            font=("Roboto", 18, "underline"),
            cursor="hand2",
            command=lambda: self.controller.change_window("SignInPage"),
        ).place(x=395, y=819, anchor=ctk.N)

        # TERMS AND CONDITIONS
        self.terms_label = ctk.CTkLabel(
            self.container,
            text="By signing in, you agree to our Terms and Condition and \nPrivacy Policy.",
            text_color=TEXT_SECONDARY,
            justify="center",
            font=("Roboto", 18),
            cursor="hand2",
        )
        self.terms_label.place(x=50, y=860)
        self.terms_label.bind("<Button-1>")

    def show_terms_and_condtion(self, event=None):
        pass

    def validate_data(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone_number = self.phone_number_entry.get().strip()
        role = self.role_option.get()
        valid_roles = ["Patient", "Personnel", "Admin"]
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not name or not email or not phone_number or not password:
            return "All fields are required."

        if len(name) < 2:
            return "Full name is too short."

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            return "Please enter a valid email address."

        if not phone_number.isdigit() or len(phone_number) != 11:
            return "Phoine number must be 11 digits (ex: 09123456789)."

        if not role or role not in valid_roles:
            return "Please select a valid role."

        if len(password) < 8:
            return "Password must be at least 8 characters long."

        if password != confirm_password:
            return "Passwords do not match."

        return None

    def sign_up(self):
        error = self.validate_data()

        if error:
            # mb.showerror("Register", error)
            mb(
                title="Error",
                message=error,
                options=("Okay",),
                icon="cancel",
            ).show()
            return

        user = User(
            name=self.name_entry.get().strip(),
            email=self.email_entry.get().strip(),
            phone_number=self.phone_number_entry.get().strip(),
            role=self.role_option.get(),
            password=self.password_entry.get(),
        )

        user_id = self.db.register(user)

        # RATE LIMIT CHECK
        if isinstance(user_id, dict) and user_id["status"] == "RATE_LIMITED":

            seconds = user_id["remaining"]
            minutes = seconds // 60

            # mb.showerror(
            #     "Too Many Attempts",
            #     f"Please wait {minutes} minute(s) before trying again.",
            # )
            mb(
                title="Too Many Attempts",
                message=f"Please wait {minutes} minute(s) before trying again.",
                options=("Okay",),
                icon="cancel",
            ).show()
            return

        if user_id == "USER_EXISTS":
            # mb.showerror("Register", "Email or phone number already exists")
            mb(
                title=" Error",
                message="Email or phone number already exists",
                options=("Okay",),
                icon="cancel",
            ).show()
        elif user_id:
            # mb.showinfo("Register", "Account created. Verify your OTP.")
            mb(
                title="Account Created",
                message="Account created. Verify your OTP.",
                options=("Thanks",),
                icon="check",
            ).show()
            self.controller.current_user = user_id
            self.controller.change_window("VerifyOTPPage")
        else:
            # mb.showerror("Register", "Registration failed")
            mb(
                title="Error",
                message="Registration failed",
                options=("Okay",),
                icon="cancel",
            ).show()

    def toggle_password(self):
        if self.password_visible:
            self.password_entry.configure(show="*")
            self.eye_btn.configure(image=self.eye_icon)
            self.password_visible = False
        else:
            self.password_entry.configure(show="")
            self.eye_btn.configure(image=self.eyeoff_icon)
            self.password_visible = True

    def toggle_confirm_password(self):
        if self.confirm_password_visible:
            self.confirm_password_entry.configure(show="*")
            self.eye_btn2.configure(image=self.eye_icon)
            self.confirm_password_visible = False
        else:
            self.confirm_password_entry.configure(show="")
            self.eye_btn2.configure(image=self.eyeoff_icon)
            self.confirm_password_visible = True

    def on_show(self):
        self.password_visible = False
        self.confirm_password_visible = False
        self.password_entry.configure(show="*")
        self.confirm_password_entry.configure(show="*")
        # self.eye_btn.configure(image=self.eye_icon)
        # self.eye_btn2.configure(image=self.eye_icon)

    def clear_fields(self):
        self.name_entry.delete(0, ctk.END)
        self.email_entry.delete(0, ctk.END)
        self.phone_number_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)
        self.confirm_password_entry.delete(0, ctk.END)
        self.email_entry.configure(placeholder_text="Email")
        self.name_entry.configure(placeholder_text="Full Name")
        self.phone_number_entry.configure(placeholder_text="Phone Number")
        self.password_entry.configure(placeholder_text="Password")
        self.confirm_password_entry.configure(placeholder_text="Confirm Password")

    # def select_role(self, idx, selected_card):
    #     self.selected_role.set(str(idx))
    #     for card in self.cards:
    #         card.configure(fg_color="#F8FAFC", border_color="#E2E8F0")
    #     selected_card.configure(fg_color="#EFF6FF", border_color=PRIMARY)

    #     # # TERMS AND CONDITIONS
    #     # self.terms_label = ctk.CTkLabel(
    #     #     self.container,
    #     #     text="By signing in, you agree to our Terms and Condition and \nPrivacy Policy.",
    #     #     text_color=TEXT_SECONDARY,
    #     #     justify="center",
    #     #     font=("Roboto", 15),
    #     #     cursor="hand2",
    #     # )
    #     # self.terms_label.place(x=35, y=530)
    #     # self.terms_label.bind("<Button-1>")

    #     # # Base text

    #     # ctk.CTkLabel(
    #     #     self.container,
    #     #     text="By signing in, you agree to our",
    #     #     text_color=TEXT_SECONDARY,
    #     #     font=("Roboto", 14),
    #     # ).place(relx=0.3, y=530, anchor="center")

    #     # # Terms and Condition (teal clickable)
    #     # terms = ctk.CTkLabel(
    #     #     self.container,
    #     #     text="Terms and Conditions",
    #     #     text_color=PRIMARY,  # TEAL
    #     #     font=("Roboto", 14, "underline"),
    #     #     cursor="hand2",
    #     # )
    #     # terms.place(relx=0.70, y=530, anchor="center")

    #     # # "and"
    #     # ctk.CTkLabel(
    #     #     self.container,
    #     #     text="and",
    #     #     text_color=TEXT_SECONDARY,
    #     #     font=("Roboto", 14),
    #     # ).place(relx=0.5, y=550, anchor="center")

    #     # # Privacy Policy (teal clickable)
    #     # privacy = ctk.CTkLabel(
    #     #     self.container,
    #     #     text="Privacy Policy",
    #     #     text_color=PRIMARY,  # TEAL
    #     #     font=("Roboto", 14, "underline"),
    #     #     cursor="hand2",
    #     # )
    #     # privacy.place(relx=0.65, y=550, anchor="center")
