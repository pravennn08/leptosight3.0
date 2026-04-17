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
)
from CTkMessagebox import CTkMessagebox as mb
from ..components.square import Square


class SignInPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color=BACKGROUND,
        )
        self.controller = controller
        self.db = controller.db
        self.toplevel_window = None

        # SYSTEM LOGO
        self.logo_img = ctk.CTkImage(
            Image.open(LOGO),
            size=(82, 82),
        )

        # CARD CONTAINER
        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent",
            # fg_color="gray",
            # border_width=1,
            # border_color="#E2E8F0",SS
            # corner_radius=12,
            width=600,
            height=790,
        )
        self.container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # # SYSTEM LOGO
        # ctk.CTkLabel(
        #     self.container,
        #     # text="LeptoSight",
        #     image=self.logo_img,
        #     text="",
        #     # compound="left",
        #     # font=("Roboto", 35),
        # ).place(
        #     relx=0.5,
        #     y=0,
        #     anchor=ctk.N,
        # )
        Square(
            self.container,
            size=90,
            image=self.logo_img,
            fg_color=PRIMARY,
        ).place(relx=0.36, y=0, anchor=ctk.N)
        ctk.CTkLabel(
            self.container, text="LeptoSight", font=("Inter", 30, "bold")
        ).place(relx=0.62, y=30, anchor=ctk.N)

        # HEADER
        ctk.CTkLabel(
            self.container,
            text="Login to your account",
            font=("Roboto", 24),
            text_color=TEXT_PRIMARY,
        ).place(x=30, y=140)

        # SUB HEADER
        ctk.CTkLabel(
            self.container,
            text="Enter your email below to login to your account",
            font=("Roboto", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=30, y=180)

        # EMAIL
        ctk.CTkLabel(
            self.container,
            text="Email",
            font=("Roboto", 20),
            text_color=TEXT_PRIMARY,
        ).place(x=30, y=250)

        # EMAIL ENTRY
        self.email_entry = ctk.CTkEntry(
            self.container,
            width=540,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#E2E8F0",
            text_color=TEXT_SECONDARY,
            border_width=0,
        )
        self.email_entry.place(x=30, y=290)

        # PASSWORD
        ctk.CTkLabel(
            self.container,
            text="Password",
            font=("Roboto", 20),
            text_color=TEXT_PRIMARY,
        ).place(x=30, y=365)

        # PASSWORD ENTRY
        self.password_entry = ctk.CTkEntry(
            self.container,
            width=540,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#E2E8F0",
            text_color=TEXT_SECONDARY,
            border_width=0,
        )
        self.password_entry.place(x=30, y=405)

        # FORGOT PASSWORD
        self.forgot_password_btn = ctk.CTkButton(
            self.container,
            text="Forgot password?",
            font=("Roboto", 20),
            width=0,
            fg_color="transparent",
            hover=False,
            text_color=TEXT_SECONDARY,
            cursor="hand2",
            command=lambda: self.open_modal(),
        )
        self.forgot_password_btn.place(x=400, y=480)

        # SIGN IN
        self.sign_in_btn = ctk.CTkButton(
            self.container,
            text="Login",
            text_color=BACKGROUND,
            width=540,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            font=("Inter", 20, "bold"),
            height=60,
            corner_radius=9,
            cursor="hand2",
            command=self.login,
        )
        self.sign_in_btn.place(x=30, y=540)

        # TO SIGN UP
        ctk.CTkLabel(
            self.container,
            text="Don't have an account?",
            text_color=TEXT_SECONDARY,
            font=("Roboto", 20),
        ).place(x=260, y=620, anchor=ctk.N)

        ctk.CTkButton(
            self.container,
            text="Sign up",
            width=0,
            fg_color="transparent",
            hover=False,
            text_color=PRIMARY,
            font=("Roboto", 20, "underline"),
            cursor="hand2",
            command=lambda: self.controller.change_window("SignUpPage"),
        ).place(x=405, y=618, anchor=ctk.N)

        # TERMS AND CONDITIONS
        self.terms_label = ctk.CTkLabel(
            self.container,
            text="By signing in, you agree to our Terms and Condition and \nPrivacy Policy.",
            text_color=TEXT_SECONDARY,
            justify="center",
            font=("Roboto", 20),
            cursor="hand2",
        )
        self.terms_label.place(x=50, y=660)
        self.terms_label.bind("<Button-1>")

    def show_terms_and_condtion(self, event=None):
        pass

    def validate(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            return "Email and password are required."

        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            return "Please enter a valid email address."

        if len(password) < 8:
            return "Password must be at least 8 characters long."

        return None

    def login(self):

        error = self.validate()
        if error:
            # mb.showerror("Login", error)
            mb(
                self,
                title="Error",
                message=error,
                options=("Okay",),
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

        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        result = self.db.login(email, password)

        # RATE LIMIT
        if isinstance(result, dict) and result["status"] == "RATE_LIMITED":
            minutes = result["remaining"] // 60
            # mb.showerror(
            #     "Too Many Attempts",
            #     f"Login temporarily locked.\nTry again in {minutes} minute(s).",
            # )
            mb(
                self,
                title="Too Many Attempts",
                message=f"Login temporarily locked.\nTry again in {minutes} minute(s).",
                options=("Okay",),
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

        # LOGIN SUCCESS
        if result == "LOGIN_SUCCESS":

            self.controller.current_user = self.db.current_user

            # ⭐ VERY IMPORTANT
            self.controller.sidebar.build_menu()
            self.controller.sidebar.get_user()
            role = self.controller.current_user[5]

            # mb.showinfo("Success", "Login successful")
            mb(
                self,
                title="Success",
                message="Login successful.",
                options=("Thanks",),
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

            # ROLE BASED NAVIGATION
            if role in ("admin", "personnel"):
                self.controller.change_window("DashboardPage")
            else:
                self.controller.change_window("HomePage")

        # NOT VERIFIED
        elif result == "NOT_VERIFIED":
            self.controller.current_user = self.db.current_user
            # mb.showwarning("Verify", "Please verify your OTP first.")
            mb(
                self,
                title="Verify",
                message="Please verify your OTP first.",
                options=("Okay",),
                icon="warning",
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

            self.controller.change_window("VerifyOTPPage")

        # RECOVERY SETUP REQUIRED
        elif result == "RECOVERY_SETUP_REQUIRED":
            self.controller.current_user = self.db.current_user
            # mb.showinfo("Setup Required", "Please complete account verification.")
            mb(
                self,
                title="Setup Required",
                message="Please complete account verification.",
                options=("Okay",),
                icon="info",
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
            self.controller.change_window("AccountVerificationPage")

        elif result == "INVALID_PASSWORD":
            # mb.showerror("Login", "Incorrect password")
            mb(
                self,
                title="Error",
                message="Incorrect password",
                options=("Okay",),
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
            # mb.showerror("Login", "User not found")
            mb(
                self,
                title="Error",
                message="User not found",
                options=("Okay",),
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
            # mb.showerror("Error", "Login failed")
            mb(
                self,
                title="Error",
                message="Login failed",
                options=("Okay",),
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

    def toggle_password(self):
        if self.password_visible:
            self.password_entry.configure(show="*")
            self.eye_btn.configure(image=self.eye_icon)
            self.password_visible = False
        else:
            self.password_entry.configure(show="")
            self.eye_btn.configure(image=self.eyeoff_icon)
            self.password_visible = True

    def clear_fields(self):
        self.email_entry.delete(0, ctk.END)
        self.password_entry.delete(0, ctk.END)
        self.email_entry.configure(placeholder_text="Email")
        self.password_entry.configure(placeholder_text="Password")


#     def open_modal(self):
#         if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
#             x = self.container.winfo_rootx()
#             y = self.container.winfo_rooty()
#             self.toplevel_window = ToplevelWindow(self.winfo_toplevel())
#             self.toplevel_window.geometry(f"+{x-80}+{y-80}")

#         # # Base text

#         # ctk.CTkLabel(
#         #     self.container,
#         #     text="By signing in, you agree to our",
#         #     text_color=TEXT_SECONDARY,
#         #     font=("Roboto", 14),
#         # ).place(relx=0.3, y=530, anchor="center")

#         # # Terms and Condition (teal clickable)
#         # terms = ctk.CTkLabel(
#         #     self.container,
#         #     text="Terms and Conditions",
#         #     text_color=PRIMARY,  # TEAL
#         #     font=("Roboto", 14, "underline"),
#         #     cursor="hand2",
#         # )
#         # terms.place(relx=0.70, y=530, anchor="center")

#         # # "and"
#         # ctk.CTkLabel(
#         #     self.container,
#         #     text="and",
#         #     text_color=TEXT_SECONDARY,
#         #     font=("Roboto", 14),
#         # ).place(relx=0.5, y=550, anchor="center")

#         # # Privacy Policy (teal clickable)
#         # privacy = ctk.CTkLabel(
#         #     self.container,
#         #     text="Privacy Policy",
#         #     text_color=PRIMARY,  # TEAL
#         #     font=("Roboto", 14, "underline"),
#         #     cursor="hand2",
#         # )
#         # privacy.place(relx=0.65, y=550, anchor="center")


# class ToplevelWindow(ctk.CTkToplevel):
#     def __init__(self, *args, **kwargs):
#         super().__init__(
#             *args,
#             **kwargs,
#             fg_color=BACKGROUND,
#         )
#         self.geometry("600x600")
#         self.grab_set()
#         self.title("Forgot Password")

#         self.container = ctk.CTkFrame(
#             self,
#             width=550,
#             height=550,
#             corner_radius=15,
#             fg_color="#F8FAFC",
#             border_width=1,
#             border_color="#E2E8F0",
#         )
#         self.container.pack(pady=25, padx=20)

#         ctk.CTkLabel(
#             self.container,
#             text="Forgot Password",
#             font=("Poppins", 25),
#         ).place(relx=0.5, rely=0.1, anchor=ctk.N)
