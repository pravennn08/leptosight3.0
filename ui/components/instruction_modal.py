import customtkinter as ctk
from PIL import Image
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    PRIMARY,
    SECONDARY,
    TEST_INSTRUCTION,
    LOGO,
    YELLOW,
)
from ..components.avatar import Avatar
from ..components.rectangle import Rectangle
from ..components.square import Square
from CTkMessagebox import CTkMessagebox as mb


class InstructionModal(ctk.CTkToplevel):
    def __init__(self, master, controller, x=100, y=100, *args, **kwargs):
        super().__init__(master, fg_color="#FFFFFF", *args, **kwargs)

        self.controller = controller

        # SYSTEM LOGO
        self.logo_img = ctk.CTkImage(
            light_image=Image.open(LOGO),
            size=(51, 51),
        )

        self.container = ctk.CTkFrame(
            self,
            width=770,
            height=740,
            # fg_color="#E2E8F0",
            fg_color="transparent",
        )
        self.container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        Square(
            self.container,
            size=60,
            image=self.logo_img,
            fg_color=PRIMARY,
        ).place(x=0, y=0)
        ctk.CTkLabel(
            self.container,
            text="LeptoSight",
            font=("Inter", 22, "bold"),
            text_color=TEXT_PRIMARY,
        ).place(x=70, y=5)

        ctk.CTkLabel(
            self.container,
            text="An AI-Powered for Early Detection of Leptospirosis",
            font=("Inter", 16),
            wraplength=670,
            justify="left",
            text_color=TEXT_SECONDARY,
        ).place(x=70, y=30)

        ctk.CTkLabel(
            self.container,
            # text="The system analyzes your responses together with body temperature to estimate your potential risk level for leptospirosis. Providing incorrect or incomplete information may affect the accuracy of the results and recommendations. This tool is designed to support early detection and should not replace professional medical evaluation.",
            text="The system analyzes your responses, body temperature, and eye scan to detect \nconjunctival suffusion in order to estimate your potential risk level for leptospirosis. Providing incorrect or incomplete information may affect the accuracy of the results and recommendations. This tool is designed to support early detection and should not replace professional medical evaluation.",
            font=("Poppins", 17),
            wraplength=790,
            justify="left",
            text_color=TEXT_SECONDARY,
        ).place(x=0, y=90)

        self.description_frame = ctk.CTkFrame(
            self.container,
            width=770,
            height=300,
            fg_color="#E2E8F0",
            corner_radius=10,
            # fg_color="transparent",
        )
        self.description_frame.place(x=0, y=210)

        ctk.CTkLabel(
            self.description_frame,
            text="Instructions",
            font=("Inter", 19, "bold"),
        ).place(x=20, y=15)

        # Starting Y position
        start_y = 60
        spacing = 35  # space between each instruction

        # Loop through instructions
        for i, item in enumerate(TEST_INSTRUCTION):
            ctk.CTkLabel(
                self.description_frame,
                text=f"• {item['sub_title']}",
                font=("Poppins", 18),
                text_color=TEXT_SECONDARY,
                wraplength=790,
                justify="left",
            ).place(x=30, y=start_y + (i * spacing))

        # Rectangle(
        #     self.container,
        #     width=770,
        #     height=70,
        #     # fg_color="#F6E7C1",
        #     fg_color=YELLOW,
        #     text="To ensure accurate assessment results, please answer all questions honestly and carefully.",
        #     text_color="#FFFFFF",
        #     font=("Poppins", 18),
        #     corner_radius=10,
        # ).place(x=0, y=530)

        self.notice_frame = ctk.CTkFrame(
            self.container,
            width=770,
            height=70,
            # fg_color="#F6E7C1",
            corner_radius=10,
            fg_color=YELLOW,
        )

        self.notice_frame.place(x=0, y=530)

        ctk.CTkLabel(
            self.notice_frame,
            text="To ensure accurate assessment results, please answer all questions honestly and carefully.",
            text_color="#FFFFFF",
            wraplength=770,
            font=("Poppins", 18),
            justify="left",
        ).place(x=20, y=12)

        self.agree_checkbox_var = ctk.StringVar(value="off")
        self.agree_checkbox = ctk.CTkCheckBox(
            self,
            text="I have read and agree to answer honestly",
            font=("Poppins", 18),
            text_color=TEXT_PRIMARY,
            variable=self.agree_checkbox_var,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            border_color=TEXT_PRIMARY,
            onvalue="on",
            offvalue="off",
        )
        self.agree_checkbox.place(x=20, y=625)

        ctk.CTkButton(
            self.container,
            text="Okay, Got it",
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            font=("Inter", 20, "bold"),
            text_color="#FFFFFF",
            height=55,
            width=180,
            corner_radius=10,
            command=lambda: self.proceed_test(),
        ).place(x=590, y=670)

        ctk.CTkButton(
            self.container,
            text="Cancel",
            fg_color="#E2E8F0",
            hover_color="#CDD5DB",
            font=("Inter", 20, "bold"),
            height=55,
            width=130,
            text_color=TEXT_SECONDARY,
            corner_radius=10,
            command=lambda: self.close(),
        ).place(x=430, y=670)

    def validate(self):
        if self.agree_checkbox_var.get() == "off":
            return "You must read and agree to the instructions before continuing."
        return None

    def proceed_test(self):
        error = self.validate()
        if error:
            # mb(
            #     title="Error",
            #     message=error,
            #     options=("Okay",),
            #     icon="cancel",
            # ).show()
            mb(
                self.controller,
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

        self.controller.change_window("ScanTemperaturePage")
        self.close()

    def close(self):
        try:
            self.grab_release()
        except:
            pass
        self.destroy()
