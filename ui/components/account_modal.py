import customtkinter as ctk
from PIL import Image
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    DIVIDER,
    PROFILE,
    SETTINGS,
    DANGER,
    LOGOUT,
)


class AccountModal(ctk.CTkToplevel):
    def __init__(self, master, controller, role="patient"):
        super().__init__(master, fg_color="#FFFFFF")
        self.controller = controller

        self.geometry("260x180")
        self.overrideredirect(True)
        self.after(200, lambda: self.bind("<FocusOut>", lambda e: self.destroy()))

        # IMAGES
        self.avatar_img = ctk.CTkImage(Image.open(PROFILE), size=(24, 24))
        self.settings_icon = ctk.CTkImage(Image.open(SETTINGS), size=(18, 18))
        self.logout_icon = ctk.CTkImage(Image.open(LOGOUT), size=(18, 18))

        # CONTAINER (CARD)
        self.container = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E5E7EB",
        )
        self.container.place(relwidth=1, relheight=1, x=0, y=0)

        # HEADER (AVATAR + INFO)
        self.avatar = ctk.CTkLabel(self.container, image=self.avatar_img, text="")
        self.avatar.place(x=15, y=20)

        self.user_name = ctk.CTkLabel(
            self.container,
            text="Raven Magbanua",
            font=("Poppins", 14),
            text_color=TEXT_PRIMARY,
        )
        self.user_name.place(x=55, y=12)

        self.user_email = ctk.CTkLabel(
            self.container,
            text="m@example.com",
            font=("Poppins", 11),
            text_color=TEXT_SECONDARY,
        )
        self.user_email.place(x=55, y=32)

        # DIVIDER
        self.div1 = ctk.CTkFrame(self.container, height=5, fg_color=DIVIDER, width=230)
        self.div1.place(x=15, y=60)

        # ROLE-BASED BUTTON CONFIG
        if role in ("admin", "personnel"):
            btn_text = "Settings"
            btn_command = lambda: self.controller.sidebar.navigate("SettingsPage")
        else:
            btn_text = "Profile"
            btn_command = lambda: self.controller.sidebar.navigate("ProfilePage")

        self.settings_btn = ctk.CTkButton(
            self.container,
            text=btn_text,
            image=self.settings_icon,
            compound="left",
            fg_color="transparent",
            hover_color="#E2E8F0",
            text_color=TEXT_PRIMARY,
            font=("Poppins", 14),
            anchor="w",
            height=40,
            width=235,
            corner_radius=8,
            command=lambda: self.handle_action(btn_command),
        )
        self.settings_btn.place(x=10, y=75)
        self.settings_btn.place(x=10, y=75)

        self.logout_btn = ctk.CTkButton(
            self.container,
            text="Logout",
            image=self.logout_icon,
            compound="left",
            fg_color="transparent",
            hover_color=DANGER,
            text_color=TEXT_PRIMARY,
            font=("Poppins", 15),
            anchor="w",
            height=40,
            width=235,
            corner_radius=8,
            command=self.handle_logout,
        )
        self.logout_btn.place(x=10, y=120)

    def handle_logout(self):
        self.destroy()
        self.controller.db.logout()
        self.controller.current_user = None
        self.controller.change_window("SignInPage")

    def handle_action(self, action):
        self.destroy()
        action()
