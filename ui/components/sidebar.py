import customtkinter as ctk
from PIL import Image
from .account_modal import AccountModal
from constants.seeds import (
    PRIMARY,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    DIVIDER,
    LOGO,
    HOME,
    PROFILE,
    TEST,
    SETTINGS,
    RECORDS,
    CHEVRON,
    DASHBOARD,
    PATIENT_RECORDS,
    USERS,
    SIDEBAR_ACTIVE,
    SIDEBAR_HOVER,
)


class AppSideBar(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color="#F8FAFC",
            border_width=2,
            border_color="#E2E8F0",
            width=400,
            corner_radius=10,
        )

        self.pack_propagate(False)
        self.controller = controller
        self.toplevel_window = None

        # IMAGES AND ICONS
        self.logo_img = ctk.CTkImage(Image.open(LOGO), size=(71, 71))
        self.home_icon = ctk.CTkImage(Image.open(HOME), size=(22, 22))
        self.test_icon = ctk.CTkImage(Image.open(TEST), size=(24, 24))
        self.records_icon = ctk.CTkImage(Image.open(RECORDS), size=(24, 24))
        self.profile_icon = ctk.CTkImage(Image.open(PROFILE), size=(24, 24))
        self.settings_icon = ctk.CTkImage(Image.open(SETTINGS), size=(24, 24))
        self.chevron_icon = ctk.CTkImage(Image.open(CHEVRON), size=(24, 24))
        self.dashboard_icon = ctk.CTkImage(Image.open(DASHBOARD), size=(24, 24))
        self.patient_records_icon = ctk.CTkImage(
            Image.open(PATIENT_RECORDS), size=(24, 24)
        )
        self.users_icon = ctk.CTkImage(Image.open(USERS), size=(24, 24))

        # LOGO
        self.logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.logo_frame.pack(fill="x", padx=10, pady=(10, 5))

        self.logo_label = ctk.CTkLabel(
            self.logo_frame,
            text="LeptoSight",
            image=self.logo_img,
            compound="left",
            text_color=TEXT_PRIMARY,
            font=("Inter", 25, "bold"),
        )
        self.logo_label.pack(anchor="w", padx=10, pady=5)

        # DIVIDER
        self.divider = ctk.CTkFrame(
            self.logo_frame, height=5, fg_color=SIDEBAR_ACTIVE, width=350
        )
        self.divider.place(x=15, y=120)

        # NAVIGATION
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent", height=500)
        self.nav_frame.pack(fill="x", padx=10, pady=5)
        self.nav_frame.pack_propagate(False)

        self.account_frame = ctk.CTkFrame(
            self, fg_color="transparent", corner_radius=8, height=100
        )

        self.account_frame.pack(side="bottom", fill="x", padx=10, pady=15)
        self.account_frame.pack_propagate(False)

        self.account_frame.bind("<Button-1>", lambda e: self.open_modal())
        self.account_frame.bind(
            "<Enter>", lambda e: self.account_frame.configure(fg_color=SIDEBAR_ACTIVE)
        )
        self.account_frame.bind(
            "<Leave>", lambda e: self.account_frame.configure(fg_color="transparent")
        )

        self.account_row = ctk.CTkFrame(self.account_frame, fg_color="transparent")
        self.account_row.pack(fill="x", padx=5)

        self.avatar_label = ctk.CTkLabel(
            self.account_row, image=self.profile_icon, text=""
        )
        self.avatar_label.pack(side="left", padx=(5, 10), pady=5)

        self.user_info = ctk.CTkFrame(self.account_row, fg_color="transparent")
        self.user_info.pack(side="left", fill="x", expand=True)

        self.user_name = ctk.CTkLabel(
            self.user_info,
            text="",
            text_color=TEXT_PRIMARY,
            font=("Poppins", 18),
        )
        self.user_name.pack(anchor="w", pady=(15, 0))

        self.user_email = ctk.CTkLabel(
            self.user_info,
            text="",
            text_color=TEXT_SECONDARY,
            font=("Poppins", 16),
        )
        self.user_email.pack(anchor="w", pady=(0, 5), padx=5)

        self.chevron_label = ctk.CTkLabel(
            self.account_row, image=self.chevron_icon, text=""
        )
        self.chevron_label.pack(side="right", padx=(10, 5))

        for widget in [
            self.account_frame,
            self.avatar_label,
            self.user_info,
            self.user_name,
            self.user_email,
            self.chevron_label,
        ]:
            widget.bind(
                "<Enter>",
                lambda e: self.account_frame.configure(fg_color=SIDEBAR_ACTIVE),
            )
            widget.bind(
                "<Leave>",
                lambda e: self.account_frame.configure(fg_color="transparent"),
            )
            widget.bind("<Button-1>", lambda e: self.open_modal())

        # BUILD MENU
        self.build_menu()

    # NAVIGATION LOGIC
    def navigate(self, page_name):
        self.controller.change_window(page_name)

        mapping = {
            "HomePage": getattr(self, "home_btn", None),
            "StartTestPage": getattr(self, "test_btn", None),
            "RecordsPage": getattr(self, "records_btn", None),
            "ProfilePage": getattr(self, "profile_btn", None),
            "DashboardPage": getattr(self, "dashboard_btn", None),
            "UsersPage": getattr(self, "users_btn", None),
            "PatientRecordsPage": getattr(self, "patient_records_btn", None),
            "SettingsPage": getattr(self, "settings_btn", None),
        }

        btn = mapping.get(page_name)

        if btn:
            self.set_active(btn)

    def set_active(self, active_btn):
        for btn in self.nav_buttons:
            if btn == active_btn:
                # btn.configure(fg_color="#D1F5F2")
                btn.configure(fg_color=SIDEBAR_ACTIVE)

            else:
                btn.configure(fg_color="transparent")

    def clear_menu_buttons(self):
        for widget in self.nav_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()

    def get_role(self):
        return "patient"

    # def get_role(self):
    #     user = self.controller.current_user

    #     if not user:
    #         return "patient"

    #     print("Printing Role:", user[5])
    #     return user[5]

    def build_menu(self):
        self.clear_menu_buttons()
        role = self.get_role()

        if role in ("admin", "personnel"):
            self.build_admin_menu()
            self.set_active(self.dashboard_btn)
        else:
            self.build_patient_menu()
            self.set_active(self.home_btn)

    # ADMIN MENU
    def build_admin_menu(self):
        self.dashboard_btn = self.button_builder(
            "Dashboard",
            self.dashboard_icon,
            lambda: self.navigate("DashboardPage"),
        )

        self.users_btn = self.button_builder(
            "Users",
            self.users_icon,
            lambda: self.navigate("UsersPage"),
        )

        self.patient_records_btn = self.button_builder(
            "Patient Records",
            self.patient_records_icon,
            lambda: self.navigate("PatientRecordsPage"),
        )

        self.settings_btn = self.button_builder(
            "Settings",
            self.settings_icon,
            lambda: self.navigate("SettingsPage"),
        )

        self.nav_buttons = [
            self.dashboard_btn,
            self.users_btn,
            self.patient_records_btn,
            self.settings_btn,
        ]

    # PATIENT MENU
    def build_patient_menu(self):
        self.home_btn = self.button_builder(
            "Home", self.home_icon, lambda: self.navigate("HomePage")
        )

        self.test_btn = self.button_builder(
            "Start Test",
            self.test_icon,
            lambda: self.navigate("StartTestPage"),
        )

        self.records_btn = self.button_builder(
            "Records",
            self.records_icon,
            lambda: self.navigate("RecordsPage"),
        )

        self.profile_btn = self.button_builder(
            "Profile",
            self.settings_icon,
            lambda: self.navigate("ProfilePage"),
        )

        self.nav_buttons = [
            self.home_btn,
            self.test_btn,
            self.records_btn,
            self.profile_btn,
        ]

    # BUTTON FACTORY
    def button_builder(self, text, icon, command):
        btn = ctk.CTkButton(
            self.nav_frame,
            text=text,
            image=icon,
            compound="left",
            fg_color="transparent",
            hover=SIDEBAR_HOVER,
            text_color=TEXT_PRIMARY,
            font=("Poppins", 20),
            anchor="w",
            height=60,
            corner_radius=10,
            command=command,
        )
        btn.pack(fill="x", pady=5, padx=5)
        return btn

    def get_user(self):
        user = self.controller.current_user
        if user:
            self.user_name.configure(text=user[1])
            self.user_email.configure(text=user[2])

        else:
            self.user_name.configure(text="")
            self.user_email.configure(text="")

    # MODAL
    def open_modal(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            x = self.account_frame.winfo_rootx()
            y = self.account_frame.winfo_rooty()
            self.toplevel_window = AccountModal(
                self.winfo_toplevel(),
                self.controller,
                role=self.get_role(),
            )
            self.toplevel_window.geometry(f"+{x+285}+{y-110}")
