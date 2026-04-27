import customtkinter as ctk
from PIL import Image
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    GREEN,
    BLUE,
    PINK,
    AVATAR_USER,
    VERIFIED,
)
from ..components.avatar import Avatar
from ..components.avatar_profile import AvatarProfile


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
        self.avatar_user = ctk.CTkImage(Image.open(AVATAR_USER), size=(30, 30))

        self.profile_frame = ctk.CTkFrame(
            self,
            height=230,
            width=1450,
            fg_color="#E2E8F0",
            corner_radius=20,
        )
        self.profile_frame.place(x=0, y=10)

        self.avatar = AvatarProfile(
            self.profile_frame,
            width=115,
            height=115,
            fg_color=GREEN,
            text_color="#FFFFFF",
            text="XX",
            font=("Inter", 45, "bold"),
        )
        self.avatar.place(x=30, y=40)

        self.name_container = ctk.CTkFrame(
            self.profile_frame,
            fg_color="transparent",
        )
        self.name_container.place(x=170, y=70)

        # Name
        self.name = ctk.CTkLabel(
            self.name_container,
            text_color=TEXT_PRIMARY,
            font=("Arial", 30, "bold"),
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
            self.profile_frame,
            text_color=TEXT_PRIMARY,
            font=("Poppins", 20),
            text="",
        )

        self.email.place(x=170, y=110)

        self.personal_info_frame = ctk.CTkFrame(
            self,
            height=500,
            width=1450,
            fg_color="#E2E8F0",
            corner_radius=20,
        )
        self.personal_info_frame.place(x=0, y=270)

        Avatar(
            self.personal_info_frame,
            width=60,
            height=60,
            image=self.avatar_user,
            fg_color=PINK,
        ).place(x=30, y=30)

        ctk.CTkLabel(
            self.personal_info_frame,
            text_color="#1E293B",
            font=("Arial", 24, "bold"),
            text="Personal Information",
        ).place(x=105, y=40)

        self.divider = ctk.CTkFrame(
            self.personal_info_frame, height=5, fg_color="#D4D6DA", width=1370
        )
        self.divider.place(x=40, y=105)

        ctk.CTkLabel(
            self.personal_info_frame,
            font=("Poppins", 19),
            text_color="#1E293B",
            text="Full Name",
        ).place(x=41, y=130)

        self.full_name_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=450,
            height=55,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#EEF2F7",
            border_color="#CBD5E1",
            text_color=TEXT_SECONDARY,
        )
        self.full_name_entry.place(x=40, y=170)

        ctk.CTkLabel(
            self.personal_info_frame,
            font=("Poppins", 19),
            text_color="#1E293B",
            text="Phone",
        ).place(x=961, y=130)

        self.phone_number_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=450,
            height=55,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#EEF2F7",
            border_color="#CBD5E1",
            text_color=TEXT_SECONDARY,
        )
        self.phone_number_entry.place(x=960, y=170)

        ctk.CTkLabel(
            self.personal_info_frame,
            font=("Poppins", 19),
            text_color="#1E293B",
            text="Email",
        ).place(x=41, y=235)

        self.email_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=450,
            height=55,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#EEF2F7",
            border_color="#CBD5E1",
            text_color=TEXT_SECONDARY,
        )
        self.email_entry.place(x=40, y=265)

        ctk.CTkLabel(
            self.personal_info_frame,
            font=("Poppins", 19),
            text_color="#1E293B",
            text="Status",
        ).place(x=961, y=235)

        self.status_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=450,
            height=55,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#EEF2F7",
            border_color="#CBD5E1",
            text_color=TEXT_SECONDARY,
        )
        self.status_entry.place(x=960, y=265)

        ctk.CTkLabel(
            self.personal_info_frame,
            font=("Poppins", 19),
            text_color="#1E293B",
            text="Joined At",
        ).place(x=41, y=330)

        self.created_at_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=450,
            height=55,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#EEF2F7",
            border_color="#CBD5E1",
            text_color=TEXT_SECONDARY,
        )
        self.created_at_entry.place(x=40, y=360)

        ctk.CTkLabel(
            self.personal_info_frame,
            font=("Poppins", 19),
            text_color="#1E293B",
            text="Last Login",
        ).place(x=961, y=330)

        self.last_login_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=450,
            height=55,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#EEF2F7",
            border_color="#CBD5E1",
            text_color=TEXT_SECONDARY,
        )
        self.last_login_entry.place(x=960, y=360)

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
        last_login = user[9]

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
