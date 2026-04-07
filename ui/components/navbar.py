import customtkinter as ctk
from PIL import Image
from constants.seeds import BACKGROUND, TEXT_PRIMARY, NEXT


class AppNavBar(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            height=60,
            fg_color=BACKGROUND,
        )
        self.pack_propagate(False)

        # ICONS
        self.next_icon = ctk.CTkImage(light_image=Image.open(NEXT), size=(30, 30))

        self.nav_title = ctk.CTkLabel(
            self,
            text="",
            font=("Inter", 20),
            text_color=TEXT_PRIMARY,
            compound="left",
            image=self.next_icon,
        )
        self.nav_title.place(x=5, y=20)

    def set_title(self, text):
        self.nav_title.configure(text=f"  {text}")
