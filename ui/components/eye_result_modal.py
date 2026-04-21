import customtkinter as ctk
from PIL import Image


from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    EYE,
    PRIMARY,
    SECONDARY,
    PERCENT,
    PINK,
    VIOLET,
    LOGO,
)
from ..components.avatar import Avatar
from ..components.square import Square
from CTkMessagebox import CTkMessagebox as mb
from models.eye_classification_model import EyeClassificationModel


class EyeResultModal(ctk.CTkToplevel):
    def __init__(self, master, controller, x=100, y=100, *args, **kwargs):
        super().__init__(master, fg_color="#FFFFFF", *args, **kwargs)

        self.controller = controller

        self.eye_icon = ctk.CTkImage(Image.open(EYE), size=(35, 35))
        self.percent_icon = ctk.CTkImage(Image.open(PERCENT), size=(35, 35))

        # SYSTEM LOGO
        self.logo_img = ctk.CTkImage(
            light_image=Image.open(LOGO),
            size=(51, 51),
        )

        self.container = ctk.CTkFrame(
            self,
            width=1100,
            height=810,
            # fg_color="#E2E8F0",
            fg_color="transparent",
        )
        self.container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        Square(
            self.container,
            size=60,
            image=self.logo_img,
            fg_color=PRIMARY,
        ).place(x=10, y=0)
        ctk.CTkLabel(
            self.container,
            text="LeptoSight",
            font=("Inter", 22, "bold"),
            text_color=TEXT_PRIMARY,
        ).place(x=90, y=5)

        ctk.CTkLabel(
            self.container,
            text="An AI-Powered for Early Detection of Leptospirosis",
            font=("Inter", 16),
            wraplength=670,
            justify="left",
            text_color=TEXT_SECONDARY,
        ).place(x=90, y=30)

        ctk.CTkLabel(
            self,
            text="Eye Scan Results",
            font=("Inter", 22, "bold"),
        ).place(x=30, y=90)

        ctk.CTkLabel(
            self.container,
            text="Raw Eye Image",
            font=("Inter", 17, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(x=15, y=120)

        ctk.CTkLabel(
            self.container,
            text="Scan Eye Image",
            font=("Inter", 17, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(x=565, y=120)

        self.raw_image_container = ctk.CTkFrame(
            self.container,
            width=530,
            height=400,
            corner_radius=9,
            fg_color="#E2E8F0",
        )
        self.raw_image_container.place(x=10, y=160)

        self.raw_image = ctk.CTkFrame(
            self.raw_image_container,
            height=380,
            width=510,
            fg_color="transparent",
        )
        self.raw_image.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.raw_image_label = ctk.CTkLabel(self.raw_image, text="")
        self.raw_image_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.scan_image_container = ctk.CTkFrame(
            self.container,
            width=530,
            height=400,
            corner_radius=9,
            fg_color="#E2E8F0",
        )
        self.scan_image_container.place(x=560, y=160)

        self.scan_image = ctk.CTkFrame(
            self.scan_image_container,
            height=380,
            width=510,
            fg_color="transparent",
        )
        self.scan_image.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.scan_image_label = ctk.CTkLabel(self.scan_image, text="")
        self.scan_image_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self.container,
            text="Results",
            font=("Inter", 19, "bold"),
            text_color="#1E293B",
        ).place(x=10, y=570)

        self.eye_class_container = ctk.CTkFrame(
            self.container,
            width=530,
            height=100,
            corner_radius=9,
            fg_color="#E2E8F0",
        )
        self.eye_class_container.place(x=10, y=610)

        Avatar(
            self.eye_class_container,
            width=60,
            height=60,
            image=self.eye_icon,
            fg_color=PINK,
        ).place(x=450, y=20)

        ctk.CTkLabel(
            self.eye_class_container,
            text="Eye Classification",
            font=("Inter", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=20, y=10)

        # VALUE
        self.eye_class_value = ctk.CTkLabel(
            self.eye_class_container,
            text="--",
            font=("Poppins", 35),
            text_color=TEXT_PRIMARY,
        )
        self.eye_class_value.place(x=20, y=40)

        self.eye_conf_container = ctk.CTkFrame(
            self.container,
            width=530,
            height=100,
            corner_radius=9,
            fg_color="#E2E8F0",
        )
        self.eye_conf_container.place(x=560, y=610)

        Avatar(
            self.eye_conf_container,
            width=60,
            height=60,
            image=self.percent_icon,
            fg_color=VIOLET,
        ).place(x=450, y=20)

        ctk.CTkLabel(
            self.eye_conf_container,
            text="Eye Confidence",
            font=("Inter", 17),
            text_color=TEXT_SECONDARY,
        ).place(x=20, y=10)

        # VALUE
        self.eye_conf_value = ctk.CTkLabel(
            self.eye_conf_container,
            text="--",
            font=("Poppins", 35),
            text_color=TEXT_PRIMARY,
        )
        self.eye_conf_value.place(x=20, y=40)

        ctk.CTkButton(
            self.container,
            text="View Results",
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            font=("Inter", 20, "bold"),
            text_color="#FFFFFF",
            height=55,
            width=180,
            corner_radius=10,
            command=lambda: self.proceed_results(),
        ).place(x=910, y=740)

    def populate_data(self):

        question_id = self.controller.current_question_id
        data = self.controller.db.load_eye_results(question_id)

        if not data:
            print("No eye results found")
            return

        # ✅ Load images
        self.load_ctk_image(data.get("eye_image"), self.raw_image_label)
        self.load_ctk_image(data.get("eye_scan"), self.scan_image_label)

        # ✅ Safe extraction
        eye_class = data.get("classification", "Unknown")
        eye_conf = data.get("confidence", 0)

        # ✅ Display
        self.eye_class_value.configure(text=eye_class)

        percent = f"{round(float(eye_conf), 2)}%"
        self.eye_conf_value.configure(text=percent)

    def load_ctk_image(self, path, label, size=(510, 380)):
        from PIL import Image

        if not path:
            return

        try:
            # Load from file path
            img = Image.open(path)

            # Resize
            img = img.resize(size)

            # Convert to CTkImage
            ctk_img = ctk.CTkImage(light_image=img, size=size)

            # ⚠️ IMPORTANT: store reference
            label.image = ctk_img

            # Display

            label.configure(image=ctk_img, text="")

        except Exception as e:
            print("IMAGE LOAD ERROR:", e)

    def proceed_results(self):
        self.close()
        self.controller.change_window("ResultsPage")

    def close(self):
        try:
            self.grab_release()
        except:
            pass
        self.destroy()
