import customtkinter as ctk
from PIL import Image
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    PRIMARY,
    SECONDARY,
    BELL,
    PROFILE,
    RECORDS,
    DASHBOARD,
    QUESTIONS,
    DISTANCE,
    INSTRUCTIONS,
    CAMERA,
    PLUS,
    FLASH,
)
from ..components.avatar import Avatar


class StartTestPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller

        # ICONS
        self.question_icon = ctk.CTkImage(Image.open(QUESTIONS), size=(28, 28))
        self.camera_icon = ctk.CTkImage(Image.open(CAMERA), size=(28, 28))
        self.user_icon = ctk.CTkImage(Image.open(DISTANCE), size=(28, 28))
        self.scan_icon = ctk.CTkImage(Image.open(FLASH), size=(28, 28))
        self.plus_icon = ctk.CTkImage(Image.open(PLUS), size=(30, 30))

        self.icons = [
            self.camera_icon,
            self.user_icon,
            self.scan_icon,
            self.question_icon,
        ]
        # CONTAINER
        self.container = ctk.CTkFrame(
            self,
            fg_color="#F8FAFC",
            border_width=2,
            border_color="#E2E8F0",
            corner_radius=20,
            width=800,
            height=770,
        )
        self.container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self.container,
            text="Start Test",
            font=("Inter", 30, "bold"),
            text_color=TEXT_PRIMARY,
        ).place(x=40, y=40)

        ctk.CTkLabel(
            self.container,
            text="Ready to begin the LeptoSight screening?",
            font=("Poppins", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=40, y=90)
        ctk.CTkLabel(
            self.container,
            text="Follow the general instruction below to successfully complete the test.",
            font=("Poppins", 18),
            text_color=TEXT_SECONDARY,
        ).place(x=40, y=125)

        self.card_builder()

        ctk.CTkButton(
            self.container,
            text="START TEST",
            text_color="#FFFFFF",
            image=self.plus_icon,
            compound="left",
            width=500,
            height=70,
            font=("Arial", 26, "bold"),
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            corner_radius=15,
            command=lambda: self.controller.change_window("ScanTemperaturePage"),
        ).place(x=150, y=650)

    def card_builder(self):
        START_Y = 180
        GAP = 115

        for i, item in enumerate(INSTRUCTIONS):
            y_position = START_Y + (i * GAP)

            card = ctk.CTkFrame(
                self.container,
                width=720,
                height=100,
                fg_color="#FFFFFF",
                corner_radius=15,
                border_width=2,
                border_color="#E2E8F0",
            )
            card.place(x=40, y=y_position)

            icon_image = self.icons[i] if i < len(self.icons) else self.bell_icon

            Avatar(
                card,
                image=icon_image,
                width=60,
                height=60,
                fg_color=PRIMARY,
            ).place(x=20, y=20)

            # TITLE
            ctk.CTkLabel(
                card,
                text=item.get("title", "No Title"),
                font=("Inter", 20, "bold"),
                text_color=TEXT_PRIMARY,
            ).place(x=100, y=20)

            # SUBTITLE
            ctk.CTkLabel(
                card,
                text=item.get("sub_title", ""),
                font=("Poppins", 18),
                text_color=TEXT_SECONDARY,
            ).place(x=100, y=48)

    def on_show(self):
        print("User:", self.controller.current_user[1])
