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
    FILTER,
    VIOLET,
    FUNNEL,
    PLUS,
)
from ..components.avatar import Avatar


class UsersPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            # fg_color="#F8FAFC",
            # border_width=1,
            # border_color="#E2E8F0",
            fg_color="transparent",
        )
        self.controller = controller

        self.filter_icon = ctk.CTkImage(Image.open(FUNNEL), size=(30, 30))
        self.plus_icon = ctk.CTkImage(Image.open(PLUS), size=(26, 26))

        ctk.CTkLabel(
            self, text="Users", font=("Arial", 33, "bold"), text_color=TEXT_PRIMARY
        ).place(x=40, y=10)
        # ctk.CTkLabel(
        #     self,
        #     text="Manage user accounts, roles, and account status efficiently.",
        #     font=("Poppins", 20),
        #     text_color=TEXT_SECONDARY,
        # ).place(x=40, y=60)

        self.user_filter_frame = ctk.CTkFrame(
            self,
            height=230,
            width=1400,
            fg_color="#E2E8F0",
            corner_radius=20,
        )
        self.user_filter_frame.place(x=40, y=70)
        Avatar(
            self.user_filter_frame,
            width=60,
            height=60,
            image=self.filter_icon,
            fg_color=VIOLET,
        ).place(x=30, y=20)
        ctk.CTkLabel(
            self.user_filter_frame,
            text=" User Filters",
            font=("Poppins", 22),
            text_color=TEXT_PRIMARY,
        ).place(x=100, y=30)

        ctk.CTkButton(
            self.user_filter_frame,
            text="Add User",
            font=("Inter", 19, "bold"),
            image=self.plus_icon,
            compound="left",
            height=50,
            width=180,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            text_color="#FFFFFF",
            corner_radius=9,
        ).place(x=1190, y=20)

        ctk.CTkLabel(
            self.user_filter_frame,
            text="Search",
            font=("Poppins", 18),
            text_color=TEXT_SECONDARY,
        ).place(x=31, y=110)

        self.search_entry = ctk.CTkEntry(
            self.user_filter_frame,
            width=500,
            height=45,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#D3D9E2",
            text_color="#1E293B",
            placeholder_text="Search users...",
            placeholder_text_color="#64748B",
            border_width=0,
        )

        self.search_entry.place(x=30, y=140)

        ctk.CTkLabel(
            self.user_filter_frame,
            text="Role",
            font=("Poppins", 18),
            text_color=TEXT_SECONDARY,
        ).place(x=721, y=110)

        self.filter_role_var = ctk.StringVar(value="All")

        self.filter_role_menu = ctk.CTkOptionMenu(
            self.user_filter_frame,
            values=["All", "Patient", "Personnel", "Admin"],
            variable=self.filter_role_var,
            width=230,
            height=45,
            font=("Inter", 18),
            fg_color="#D3D9E2",  # match search bar
            button_color="#CBD5E1",  # subtle gray-blue
            button_hover_color="#94A3B8",  # darker on hover
            text_color="#1E293B",  # dark readable text
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Inter", 20),
            corner_radius=9,
        )

        self.filter_role_menu.place(x=720, y=140)
        ctk.CTkLabel(
            self.user_filter_frame,
            text="Status",
            font=("Poppins", 18),
            text_color=TEXT_SECONDARY,
        ).place(x=1141, y=110)
        self.filter_status_var = ctk.StringVar(value="All")

        self.filter_status_menu = ctk.CTkOptionMenu(
            self.user_filter_frame,
            values=["All", "Verified", "Not Verified"],
            variable=self.filter_status_var,
            width=230,
            height=45,
            font=("Inter", 18),
            fg_color="#D3D9E2",  # match search bar
            button_color="#CBD5E1",  # subtle gray-blue
            button_hover_color="#94A3B8",  # darker on hover
            text_color="#1E293B",  # dark readable text
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#D4D6DA",
            dropdown_font=("Inter", 20),
            corner_radius=9,
        )
        self.filter_status_menu.place(x=1140, y=140)

        self.table_container = ctk.CTkFrame(
            self,
            width=1400,
            height=590,
            corner_radius=20,
            fg_color="#E2E8F0",
        )
        self.table_container.place(x=40, y=325)
        self.users_table = ctk.CTkFrame(
            self.table_container,
            fg_color="red",
            width=1380,
            height=560,
        )

        self.users_table.pack(fill="both", expand=True)
        self.users_table.pack_propagate(False)
