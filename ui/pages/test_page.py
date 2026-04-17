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
    EVAL,
    SHIELD,
    LOGO,
    YELLOW,
    PERCENT,
    FLASH,
)
from ..components.avatar import Avatar
from ..components.rectangle import Rectangle
from ..components.square import Square
from ..components.messagebox import MessageBox as mb


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
        self.eval_icon = ctk.CTkImage(Image.open(EVAL), size=(38, 38))
        self.skip_icon = ctk.CTkImage(Image.open(SKIP), size=(38, 38))
        self.warning_icon = ctk.CTkImage(Image.open(SHIELD), size=(34, 34))

        self.icons = [
            self.read_icon,
            self.recall_icon,
            self.select_icon,
            self.eval_icon,
            self.skip_icon,
            self.heart_icon,
        ]

        ctk.CTkLabel(
            self, text="Start Test", font=("Arial", 33, "bold"), text_color=TEXT_PRIMARY
        ).place(x=40, y=10)
        ctk.CTkLabel(
            self,
            text="Ready to begin the LeptoSight screening?",
            font=("Poppins", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=40, y=60)
        ctk.CTkLabel(
            self,
            text="Follow the general instruction below to successfully complete the test.",
            font=("Poppins", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=40, y=100)

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
            font=("Inter", 22, "bold"),
            width=450,
            height=65,
            corner_radius=9,
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

        self.top = Modal(self, controller=self.controller, x=x, y=y)

        self.top.title("LeptoSight")
        self.top.geometry(f"700x700+{x+310}+{y+50}")
        self.top.transient(self)
        self.top.after(10, self.top.grab_set)

        # self.top = EyeResultModal(self, controller=self.controller, x=x, y=y)

        # self.top.title("LeptoSight")
        # self.top.geometry(f"1130x840+{x+180}+{y}")
        # self.top.transient(self)
        # self.top.after(10, self.top.grab_set)


class Modal(ctk.CTkToplevel):
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
            width=670,
            height=690,
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
            text="The system analyzes your responses together with body temperature to estimate your potential risk level for leptospirosis. Providing incorrect or incomplete information may affect the accuracy of the results and recommendations. This tool is designed to support early detection and should not replace professional medical evaluation.",
            font=("Poppins", 17),
            wraplength=670,
            justify="left",
            text_color=TEXT_SECONDARY,
        ).place(x=0, y=90)

        self.description_frame = ctk.CTkFrame(
            self.container,
            width=670,
            height=275,
            fg_color="#E2E8F0",
            corner_radius=10,
            # fg_color="transparent",
        )
        self.description_frame.place(x=0, y=200)

        ctk.CTkLabel(
            self.description_frame,
            text="Instructions",
            font=("Inter", 17, "bold"),
        ).place(x=20, y=15)

        # Starting Y position
        start_y = 50
        spacing = 35  # space between each instruction

        # Loop through instructions
        for i, item in enumerate(TEST_INSTRUCTION):
            ctk.CTkLabel(
                self.description_frame,
                text=f"• {item['sub_title']}",
                font=("Poppins", 16),
                text_color=TEXT_SECONDARY,
                wraplength=630,
                justify="left",
            ).place(x=30, y=start_y + (i * spacing))

        Rectangle(
            self.container,
            width=670,
            height=70,
            # fg_color="#F6E7C1",
            fg_color=YELLOW,
            text="To ensure accurate assessment results, please answer all questions honestly and carefully.",
            text_color="#FFFFFF",
            font=("Poppins", 17),
            corner_radius=10,
        ).place(x=0, y=490)

        self.agree_checkbox_var = ctk.StringVar(value="off")
        self.agree_checkbox = ctk.CTkCheckBox(
            self,
            text="I have read and agree to answer honestly",
            font=("Poppins", 17),
            text_color=TEXT_PRIMARY,
            variable=self.agree_checkbox_var,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            border_color=TEXT_PRIMARY,
            onvalue="on",
            offvalue="off",
        )
        self.agree_checkbox.place(x=20, y=580)

        ctk.CTkButton(
            self,
            text="Okay, Got it",
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            font=("Inter", 20, "bold"),
            text_color="#FFFFFF",
            height=55,
            width=180,
            corner_radius=10,
            command=lambda: self.proceed_test(),
        ).place(x=500, y=620)

        ctk.CTkButton(
            self,
            text="Cancel",
            fg_color="#E2E8F0",
            hover_color="#CDD5DB",
            font=("Inter", 20, "bold"),
            height=55,
            width=130,
            text_color=TEXT_SECONDARY,
            corner_radius=10,
            command=lambda: self.close(),
        ).place(x=350, y=620)

    def validate(self):
        if self.agree_checkbox_var.get() == "off":
            return "You must read and agree to the instructions before continuing."
        return None

    def proceed_test(self):
        error = self.validate()
        if error:
            mb(
                title="Error",
                message=error,
                options=("Okay",),
                icon="cancel",
            ).show()
            return

        self.controller.change_window("ScanTemperaturePage")
        self.close()

    def close(self):
        try:
            self.grab_release()
        except:
            pass
        self.destroy()


# class EyeResultModal(ctk.CTkToplevel):
#     def __init__(self, master, controller, x=100, y=100, *args, **kwargs):
#         super().__init__(master, fg_color="#FFFFFF", *args, **kwargs)

#         self.controller = controller

#         self.eye_icon = ctk.CTkImage(Image.open(EYE), size=(35, 35))
#         self.percent_icon = ctk.CTkImage(Image.open(PERCENT), size=(35, 35))

#         # SYSTEM LOGO
#         self.logo_img = ctk.CTkImage(
#             light_image=Image.open(LOGO),
#             size=(51, 51),
#         )

#         self.container = ctk.CTkFrame(
#             self,
#             width=1100,
#             height=810,
#             # fg_color="#E2E8F0",
#             fg_color="transparent",
#         )
#         self.container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

#         Square(
#             self.container,
#             size=60,
#             image=self.logo_img,
#             fg_color=PRIMARY,
#         ).place(x=10, y=0)
#         ctk.CTkLabel(
#             self.container,
#             text="LeptoSight",
#             font=("Inter", 22, "bold"),
#             text_color=TEXT_PRIMARY,
#         ).place(x=90, y=5)

#         ctk.CTkLabel(
#             self.container,
#             text="An AI-Powered for Early Detection of Leptospirosis",
#             font=("Inter", 16),
#             wraplength=670,
#             justify="left",
#             text_color=TEXT_SECONDARY,
#         ).place(x=90, y=30)

#         ctk.CTkLabel(
#             self,
#             text="Eye Scan Results",
#             font=("Inter", 22, "bold"),
#         ).place(x=30, y=90)

#         ctk.CTkLabel(
#             self.container,
#             text="Raw Eye Image",
#             font=("Inter", 17, "bold"),
#             text_color=TEXT_SECONDARY,
#         ).place(x=15, y=120)

#         ctk.CTkLabel(
#             self.container,
#             text="Scan Eye Image",
#             font=("Inter", 17, "bold"),
#             text_color=TEXT_SECONDARY,
#         ).place(x=565, y=120)

#         self.raw_image_container = ctk.CTkFrame(
#             self.container,
#             width=530,
#             height=400,
#             corner_radius=9,
#             fg_color="#E2E8F0",
#         )
#         self.raw_image_container.place(x=10, y=160)

#         self.raw_image = ctk.CTkFrame(
#             self.raw_image_container,
#             height=510,
#             width=380,
#             fg_color="transparent",
#         )
#         self.raw_image.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
#         self.raw_image_label = ctk.CTkLabel(self.raw_image, text="")
#         self.raw_image_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

#         self.scan_image_container = ctk.CTkFrame(
#             self.container,
#             width=530,
#             height=400,
#             corner_radius=9,
#             fg_color="#E2E8F0",
#         )
#         self.scan_image_container.place(x=560, y=160)

#         self.scan_image = ctk.CTkFrame(
#             self.scan_image_container,
#             height=510,
#             width=380,
#             fg_color="transparent",
#         )
#         self.scan_image.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
#         self.scan_image_label = ctk.CTkLabel(self.scan_image, text="")
#         self.scan_image_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

#         ctk.CTkLabel(
#             self.container,
#             text="Results",
#             font=("Inter", 19, "bold"),
#             text_color="#1E293B",
#         ).place(x=10, y=570)

#         self.eye_class_container = ctk.CTkFrame(
#             self.container,
#             width=530,
#             height=100,
#             corner_radius=9,
#             fg_color="#E2E8F0",
#         )
#         self.eye_class_container.place(x=10, y=610)

#         Avatar(
#             self.eye_class_container,
#             width=60,
#             height=60,
#             image=self.eye_icon,
#             fg_color=PINK,
#         ).place(x=450, y=20)

#         ctk.CTkLabel(
#             self.eye_class_container,
#             text="Eye Classification",
#             font=("Inter", 17),
#             text_color=TEXT_SECONDARY,
#         ).place(x=20, y=10)

#         # VALUE
#         ctk.CTkLabel(
#             self.eye_class_container,
#             text="SAFE",
#             font=("Poppins", 35),
#             text_color=TEXT_PRIMARY,
#         ).place(x=20, y=40)

#         self.eye_conf_container = ctk.CTkFrame(
#             self.container,
#             width=530,
#             height=100,
#             corner_radius=9,
#             fg_color="#E2E8F0",
#         )
#         self.eye_conf_container.place(x=560, y=610)

#         Avatar(
#             self.eye_conf_container,
#             width=60,
#             height=60,
#             image=self.percent_icon,
#             fg_color=VIOLET,
#         ).place(x=450, y=20)

#         ctk.CTkLabel(
#             self.eye_conf_container,
#             text="Eye Confidence",
#             font=("Inter", 17),
#             text_color=TEXT_SECONDARY,
#         ).place(x=20, y=10)

#         # VALUE
#         ctk.CTkLabel(
#             self.eye_conf_container,
#             text="99%",
#             font=("Poppins", 35),
#             text_color=TEXT_PRIMARY,
#         ).place(x=20, y=40)

#         ctk.CTkButton(
#             self.container,
#             text="View Results",
#             fg_color=PRIMARY,
#             hover_color=SECONDARY,
#             font=("Inter", 20, "bold"),
#             text_color="#FFFFFF",
#             height=55,
#             width=180,
#             corner_radius=10,
#             command=lambda: self.proceed_test(),
#         ).place(x=910, y=740)
