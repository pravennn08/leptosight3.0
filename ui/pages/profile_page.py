import customtkinter as ctk
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
    VERIFIED,
)
from ..components.avatar import Avatar
from ..components.avatar_profile import AvatarProfile
from ..components.messagebox import MessageBox as mb
from ..components.data_table import DataTable
from ..components.rectangle import Rectangle


class ProfilePage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            # fg_color="#F8FAFC",
            # border_width=1,
            # border_color="#E2E8F0",
            fg_color="transparent",
        )
        self.controller = controller

        self.verified_icon = ctk.CTkImage(Image.open(VERIFIED), size=(20, 20))

        ctk.CTkLabel(
            self, text="Profile", font=("Arial", 33, "bold"), text_color=TEXT_PRIMARY
        ).place(x=40, y=10)

        self.container = ctk.CTkFrame(
            self,
            width=1400,
            height=660,
            # fg_color="#F8FAFC",
            # border_width=2,
            # border_color="#E2E8F0",
            # corner_radius=20,
            fg_color="transparent",
        )
        self.container.place(x=40, y=80)

        self.avatar = AvatarProfile(
            self.container,
            width=160,
            height=160,
            fg_color=GREEN,
            text_color="#FFFFFF",
            text="XX",
            font=("Inter", 55, "bold"),
        )
        self.avatar.place(x=60, y=50)

        # self.name = ctk.CTkLabel(
        #     self.container,
        #     text_color=TEXT_PRIMARY,
        #     font=("Arial", 32, "bold"),
        #     text="",
        # )

        # self.name.place(x=300, y=50)

        # self.badge = Avatar(
        #     self.container,
        #     width=34,
        #     height=34,
        #     image=self.verified_icon,
        #     fg_color=BLUE,
        # )

        # Wrapper frame
        self.name_container = ctk.CTkFrame(self.container, fg_color="transparent")
        self.name_container.place(x=300, y=50)

        # Name
        self.name = ctk.CTkLabel(
            self.name_container,
            text_color=TEXT_PRIMARY,
            font=("Arial", 32, "bold"),
            text="",
        )
        self.name.pack(side="left")

        # Badge
        self.badge = Avatar(
            self.name_container,
            width=34,
            height=34,
            image=self.verified_icon,
            fg_color=BLUE,
        )

        self.email = ctk.CTkLabel(
            self.container,
            text_color=TEXT_PRIMARY,
            font=("Poppins", 20),
            text="",
        )

        self.email.place(x=300, y=95)

        ctk.CTkButton(
            self.container,
            width=170,
            height=55,
            fg_color=GREEN,
            text="Edit Profile",
            text_color="#FFFFFF",
            font=("Arial", 22, "bold"),
        ).place(x=300, y=140)

        self.divider = ctk.CTkFrame(
            self.container, height=5, fg_color="#E2E8F0", width=1030
        )
        self.divider.place(x=300, y=230)

        ctk.CTkLabel(
            self.container,
            text_color=TEXT_PRIMARY,
            font=("Arial", 26, "bold"),
            text="Account Details",
        ).place(x=300, y=270)

        ctk.CTkLabel(
            self.container,
            text_color=TEXT_SECONDARY,
            font=("Roboto", 20),
            text="Full Name",
        ).place(x=300, y=350)

        self.full_name_entry = ctk.CTkEntry(
            self.container,
            width=370,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            text_color=TEXT_SECONDARY,
        )
        self.full_name_entry.place(x=410, y=340)

        ctk.CTkLabel(
            self.container,
            text_color=TEXT_SECONDARY,
            font=("Roboto", 20),
            text="Phone",
        ).place(x=880, y=350)

        self.phone_number_entry = ctk.CTkEntry(
            self.container,
            width=370,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            text_color=TEXT_SECONDARY,
        )
        self.phone_number_entry.place(x=960, y=340)

        ctk.CTkLabel(
            self.container,
            text_color=TEXT_SECONDARY,
            font=("Roboto", 20),
            text="Email",
        ).place(x=300, y=450)

        self.email_entry = ctk.CTkEntry(
            self.container,
            width=370,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            text_color=TEXT_SECONDARY,
        )
        self.email_entry.place(x=410, y=440)

        ctk.CTkLabel(
            self.container,
            text_color=TEXT_SECONDARY,
            font=("Roboto", 20),
            text="Status",
        ).place(x=880, y=450)

        self.status_entry = ctk.CTkEntry(
            self.container,
            width=370,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            text_color=TEXT_SECONDARY,
        )
        self.status_entry.place(x=960, y=440)

        ctk.CTkLabel(
            self.container,
            text_color=TEXT_SECONDARY,
            font=("Roboto", 20),
            text="Joined At",
        ).place(x=300, y=550)

        self.created_at_entry = ctk.CTkEntry(
            self.container,
            width=370,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            text_color=TEXT_SECONDARY,
        )
        self.created_at_entry.place(x=410, y=540)

        ctk.CTkLabel(
            self.container,
            text_color=TEXT_SECONDARY,
            font=("Roboto", 20),
            text="Last Login",
        ).place(x=845, y=550)

        self.last_login_entry = ctk.CTkEntry(
            self.container,
            width=370,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
            text_color=TEXT_SECONDARY,
        )
        self.last_login_entry.place(x=960, y=540)

    def get_avatar_initials(self, full_name: str):
        if not full_name:
            return "?"
        parts = full_name.strip().split()
        if len(parts) == 1:
            return parts[0][0].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    def format_date(self, value):
        from datetime import datetime

        if not value:
            return "N/A"

        try:
            # If it's already a datetime object
            if isinstance(value, datetime):
                return value.strftime("%B %d, %Y")

            # If it's a string, try parsing
            parsed = datetime.fromisoformat(str(value))
            return parsed.strftime("%B %d, %Y")

        except Exception:
            return str(value)

    def load_profile(self):

        user = self.controller.current_user
        print(f"User: {user}")
        if not user:
            return

        name = user[1]
        email = user[2]
        phone_number = user[3]
        verified = user[7]
        date_create = user[6]
        last_login = user[8]

        if verified:
            if not self.badge.winfo_ismapped():
                self.badge.pack(side="left", padx=(8, 0))
            status = "Verified"
        else:
            self.badge.pack_forget()
            status = "Not Verified"

        initials = self.get_avatar_initials(name)
        self.avatar.set_text(initials)
        self.name.configure(text=name)
        self.email.configure(text=email)

        self.full_name_entry.insert(0, name)
        self.full_name_entry.configure(state=ctk.DISABLED)
        self.email_entry.insert(0, email)
        self.email_entry.configure(state=ctk.DISABLED)

        self.phone_number_entry.insert(0, phone_number)
        self.phone_number_entry.configure(state=ctk.DISABLED)

        self.status_entry.insert(0, status)
        self.status_entry.configure(state=ctk.DISABLED)

        self.created_at_entry.insert(0, self.format_date(date_create))
        self.created_at_entry.configure(state=ctk.DISABLED)

        self.last_login_entry.insert(0, self.format_date(last_login))
        self.last_login_entry.configure(state=ctk.DISABLED)

    def on_show(self):
        self.load_profile()
