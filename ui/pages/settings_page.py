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
    AVATAR_USER,
    PINK,
)
from ..components.avatar import Avatar
from ..components.avatar_profile import AvatarProfile


class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            # fg_color="#F8FAFC",
            # border_width=1,
            # border_color="#E2E8F0",
            fg_color="transparent",
        )
        self.controller = controller
        self.admin_db = controller.admin_db

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
            width=130,
            height=130,
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
        self.name_container.place(x=190, y=70)

        # Name
        self.name = ctk.CTkLabel(
            self.name_container,
            text_color=TEXT_PRIMARY,
            font=("Arial", 32, "bold"),
            text="Raven Magbanua",
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
        self.badge.pack()
        self.email = ctk.CTkLabel(
            self.profile_frame,
            text_color=TEXT_PRIMARY,
            font=("Poppins", 20),
            text="magbanua@email.com",
        )

        self.email.place(x=190, y=110)

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
            fg_color=BLUE,
        ).place(x=30, y=20)

        ctk.CTkLabel(
            self.personal_info_frame,
            text_color="#1E293B",
            font=("Poppins", 24, "bold"),
            text="Account Details",
        ).place(x=105, y=30)

        ctk.CTkLabel(
            self.personal_info_frame,
            font=("Poppins", 19),
            text_color="#1E293B",
            text="Full Name",
        ).place(x=41, y=110)

        self.full_name_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=500,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#EEF2F7",
            border_color="#CBD5E1",
            text_color=TEXT_SECONDARY,
        )
        self.full_name_entry.place(x=40, y=150)

        ctk.CTkLabel(
            self.personal_info_frame,
            font=("Poppins", 19),
            text_color="#1E293B",
            text="Phone",
        ).place(x=911, y=120)

        self.phone_number_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=500,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#EEF2F7",
            border_color="#CBD5E1",
            text_color=TEXT_SECONDARY,
        )
        self.phone_number_entry.place(x=910, y=150)

        ctk.CTkLabel(
            self.personal_info_frame,
            font=("Poppins", 19),
            text_color="#1E293B",
            text="Email",
        ).place(x=41, y=225)

        self.email_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=500,
            height=60,
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
        ).place(x=911, y=225)

        self.status_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=500,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#EEF2F7",
            border_color="#CBD5E1",
            text_color=TEXT_SECONDARY,
        )
        self.status_entry.place(x=910, y=265)

        ctk.CTkLabel(
            self.personal_info_frame,
            font=("Poppins", 19),
            text_color="#1E293B",
            text="Joined At",
        ).place(x=41, y=340)

        self.created_at_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=500,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#EEF2F7",
            border_color="#CBD5E1",
            text_color=TEXT_SECONDARY,
        )
        self.created_at_entry.place(x=40, y=380)

        ctk.CTkLabel(
            self.personal_info_frame,
            font=("Poppins", 19),
            text_color="#1E293B",
            text="Last Login",
        ).place(x=911, y=340)

        self.last_login_entry = ctk.CTkEntry(
            self.personal_info_frame,
            width=500,
            height=60,
            corner_radius=9,
            font=("Roboto", 20),
            fg_color="#EEF2F7",
            border_color="#CBD5E1",
            text_color=TEXT_SECONDARY,
        )
        self.last_login_entry.place(x=910, y=380)
