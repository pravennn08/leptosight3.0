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
    TEST_INSTRUCTION,
    CAMERA,
    PLUS,
    HEART,
    READ,
    RECALL,
    SKIP,
    PINK,
    VIOLET,
    SELECT,
    EYE,
    WARNING,
    NAV,
    SHIELD,
    LOGO,
    YELLOW,
    PLUS,
)
from ..components.avatar import Avatar
from ..components.rectangle import Rectangle
from ..components.square import Square
from ..components.instruction_modal import InstructionModal


class StartTestPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller

        # SYSTEM LOGO
        self.logo_img = ctk.CTkImage(
            light_image=Image.open(LOGO),
            size=(45, 45),
        )

        # ICONS
        self.read_icon = ctk.CTkImage(Image.open(READ), size=(38, 38))
        self.recall_icon = ctk.CTkImage(Image.open(RECALL), size=(38, 38))
        self.select_icon = ctk.CTkImage(Image.open(SELECT), size=(38, 38))
        self.heart_icon = ctk.CTkImage(Image.open(HEART), size=(38, 38))
        self.nav_icon = ctk.CTkImage(Image.open(NAV), size=(38, 38))
        self.skip_icon = ctk.CTkImage(Image.open(SKIP), size=(38, 38))
        self.warning_icon = ctk.CTkImage(Image.open(SHIELD), size=(34, 34))
        self.plus_icon = ctk.CTkImage(Image.open(PLUS), size=(35, 35))

        self.icons = [
            self.read_icon,
            self.recall_icon,
            self.select_icon,
            self.nav_icon,
            self.skip_icon,
            self.heart_icon,
        ]

        ctk.CTkLabel(
            self, text="Start Test", font=("Arial", 33, "bold"), text_color=TEXT_PRIMARY
        ).place(x=20, y=10)
        ctk.CTkLabel(
            self,
            text="Ready to begin the LeptoSight screening?",
            font=("Poppins", 20),
            text_color=TEXT_PRIMARY,
        ).place(x=20, y=60)
        ctk.CTkLabel(
            self,
            text="Follow the general instruction below to successfully complete the test.",
            font=("Poppins", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=20, y=100)

        # self.notice_container = ctk.CTkFrame(
        #     self,
        #     height=80,
        #     width=1390,
        #     fg_color="transparent",
        # )
        # self.notice_container.place(x=40, y=560)

        # self.notice_frame = ctk.CTkFrame(
        #     self.notice_container,
        #     height=80,
        #     width=1000,
        #     fg_color="#E2E8F0",
        #     corner_radius=15,
        # )
        # self.notice_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # ctk.CTkLabel(
        #     self.notice_frame,
        #     text=" This test is NOT a medical diagnosis. Consult a doctor for confirmation.",
        #     font=("Poppins", 20, "bold"),
        #     text_color=TEXT_SECONDARY,
        # ).place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        Rectangle(
            self,
            height=90,
            width=960,
            fg_color="#E2E8F0",
            corner_radius=15,
        ).place(x=260, y=560)

        Avatar(
            self,
            height=60,
            width=60,
            image=self.warning_icon,
            fg_color=YELLOW,
            bg_color="#E2E8F0",
        ).place(x=290, y=575)

        ctk.CTkLabel(
            self,
            text=" This test is NOT a medical diagnosis. Consult a doctor for confirmation.",
            font=("Poppins", 20, "bold"),
            text_color=TEXT_SECONDARY,
            bg_color="#E2E8F0",
        ).place(x=360, y=590)

        ctk.CTkButton(
            self,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            text_color="#FFFFFF",
            text="Start Test",
            font=("Inter", 24, "bold"),
            width=400,
            height=70,
            corner_radius=9,
            image=self.plus_icon,
            command=lambda: self.modal(),
        ).place(x=510, y=680)

    def card_builder(self):
        START_X = 40
        START_Y = 170

        CARD_WIDTH = 450
        CARD_HEIGHT = 160

        GAP_X = 470  # horizontal spacing
        GAP_Y = 180  # vertical spacing

        COLUMNS = 3  # 3 cards per row

        for i, item in enumerate(TEST_INSTRUCTION):
            row = i // COLUMNS
            col = i % COLUMNS

            x_position = START_X + (col * GAP_X)
            y_position = START_Y + (row * GAP_Y)

            card = ctk.CTkFrame(
                self,
                width=CARD_WIDTH,
                height=CARD_HEIGHT,
                fg_color="#E2E8F0",
                corner_radius=15,
                border_width=2,
                border_color="#E2E8F0",
            )
            card.place(x=x_position, y=y_position)

            icon_image = self.icons[i] if i < len(self.icons) else self.icons[0]

            Avatar(
                card,
                image=icon_image,
                width=75,
                height=75,
                fg_color=PRIMARY,
            ).place(x=30, y=30)

            # TITLE
            ctk.CTkLabel(
                card,
                text=item.get("title", "No Title"),
                font=("Inter", 22, "bold"),
                text_color=TEXT_PRIMARY,
            ).place(x=130, y=30)

            # SUBTITLE
            ctk.CTkLabel(
                card,
                text=item.get("sub_title", ""),
                wraplength=280,
                font=("Poppins", 18),
                justify="left",
                text_color=TEXT_SECONDARY,
            ).place(x=130, y=60)

    def on_show(self):
        # print("User:", self.controller.current_user[1])
        self.card_builder()

    def modal(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty()

        self.top = InstructionModal(self, controller=self.controller, x=x, y=y)

        self.top.title("LeptoSight")
        self.top.geometry(f"800x750+{x+310}+{y+50}")
        self.top.transient(self)
        self.top.after(10, self.top.grab_set)
