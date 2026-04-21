import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from picamera2 import Picamera2
import cv2
from hardware.relay import send_relay_on, send_relay_off, cleanup
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
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
    PERCENT,
    PINK,
    VIOLET,
    LOGO,
)
from ..components.avatar import Avatar
from ..components.square import Square
from CTkMessagebox import CTkMessagebox as mb
from models.eye_classification_model import EyeClassificationModel


class EyeScanPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color="transparent",
            # fg_color="#F8FAFC",
            # border_width=2,
            # border_color="#E2E8F0",
            # corner_radius=15,
        )
        self.controller = controller
        self.db = controller.db
        self.eye_model = EyeClassificationModel()

        self.current_frame = None
        self.preview_mode = False
        self.is_on = False
        self.flash_on = send_relay_on
        self.flash_off = send_relay_off
        self.clean_up = cleanup

        # IMAGE
        self.camera_prompt_img = ctk.CTkImage(
            Image.open(CAMERA_PROMPT), size=(360, 260)
        )

        # ICONS
        self.camera_icon = ctk.CTkImage(Image.open(CAMERA), size=(70, 70))
        self.flash_icon = ctk.CTkImage(Image.open(FLASH), size=(50, 50))
        self.save_icon = ctk.CTkImage(Image.open(SAVE), size=(50, 50))
        self.check_icon = ctk.CTkImage(Image.open(CHECK), size=(24, 24))

        self.camera_tips_icon = ctk.CTkImage(Image.open(CAMERA), size=(24, 24))
        self.eye_tips_icon = ctk.CTkImage(Image.open(EYE), size=(24, 24))
        self.flash_tips_icon = ctk.CTkImage(Image.open(FLASH), size=(24, 24))
        self.distance_tips_icon = ctk.CTkImage(Image.open(DISTANCE), size=(24, 24))

        self.tips_icons = [
            self.camera_tips_icon,
            self.eye_tips_icon,
            self.flash_tips_icon,
            self.distance_tips_icon,
        ]

        ctk.CTkLabel(
            self, text="Eye Scan", font=("Arial", 33, "bold"), text_color=TEXT_PRIMARY
        ).place(x=40, y=10)
        ctk.CTkLabel(
            self,
            text="Please center your eye in the frame and hold steady while the scan is in progress.",
            font=("Poppins", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=40, y=60)

        self.container = ctk.CTkFrame(
            self,
            height=650,
            width=1000,
            fg_color="#E2E8F0",
            border_width=2,
            border_color="#E2E8F0",
            corner_radius=15,
        )
        self.container.place(x=40, y=100)

        self.camera_container = ctk.CTkFrame(
            self.container,
            height=600,
            width=950,
        )
        self.camera_container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.camera_label = tk.Label(self.camera_container, text="")
        self.camera_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.actions_container = ctk.CTkFrame(
            self,
            height=170,
            width=1000,
            fg_color="transparent",
        )
        self.actions_container.place(x=40, y=750)

        self.capture_btn = ctk.CTkButton(
            self.actions_container,
            image=self.camera_icon,
            width=150,
            height=130,
            text="",
            fg_color=BLUE,
            hover_color="#0284C7",
            corner_radius=10,
            command=self.capture_eye,
            # compound="center",
        )
        self.capture_btn.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self.actions_container,
            text="CAPTURE",
            font=("Inter", 16, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(relx=0.5, rely=0.97, anchor=ctk.CENTER)

        self.open_flash = ctk.CTkButton(
            self.actions_container,
            image=self.flash_icon,
            width=100,
            height=90,
            text="",
            fg_color=YELLOW,
            corner_radius=10,
            command=self.toggle_flash,
            # compound="center",
        )
        self.open_flash.place(relx=0.35, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self.actions_container,
            text="FLASH",
            font=("Inter", 16, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(relx=0.35, rely=0.85, anchor=ctk.CENTER)

        self.save_eye = ctk.CTkButton(
            self.actions_container,
            image=self.save_icon,
            width=100,
            height=90,
            text="",
            fg_color="#14B8A6",
            corner_radius=10,
            # compound="center",
            command=self.save_eye_scan,
        )
        self.save_eye.place(relx=0.65, rely=0.5, anchor=ctk.CENTER)
        ctk.CTkLabel(
            self.actions_container,
            text="SAVE",
            font=("Inter", 16, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(relx=0.65, rely=0.85, anchor=ctk.CENTER)

        self.instruction_container = ctk.CTkFrame(
            self,
            height=430,
            width=380,
            fg_color="#E2E8F0",
            corner_radius=15,
        )
        self.instruction_container.place(x=1070, y=100)

        Avatar(
            self.instruction_container,
            image=self.check_icon,
            width=40,
            height=40,
            fg_color="#14B8A6",
        ).place(x=30, y=30)

        ctk.CTkLabel(
            self.instruction_container,
            text="Best Position Guide",
            text_color=TEXT_PRIMARY,
            font=("Inter", 20),
        ).place(x=80, y=35)

        ctk.CTkLabel(
            self,
            text="PREVIEW",
            font=("Inter", 16, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(x=1075, y=560)

        self.preview_container = ctk.CTkFrame(
            self,
            height=270,
            width=380,
            fg_color="#E2E8F0",
            corner_radius=15,
        )
        self.preview_container.place(x=1070, y=595)

        self.preview_frame = ctk.CTkFrame(
            self.preview_container,
            height=260,
            width=370,
            fg_color="transparent",
        )
        self.preview_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="",
        )
        self.preview_label.pack(expand=True)

    def toggle_flash(self):
        self.is_on = not self.is_on

        if self.is_on:
            self.flash_on()
        else:
            self.flash_off()

    def start_camera(self):
        if hasattr(self, "camera_running") and self.camera_running:
            return

        self.picam2 = Picamera2()

        config = self.picam2.create_preview_configuration(
            main={"size": (950, 600), "format": "RGB888"}
        )

        self.picam2.configure(config)
        self.picam2.start()

        self.camera_running = True
        self.update_camera()

    # def update_camera(self):
    #     frame = self.picam2.capture_array()

    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #     self.current_frame = frame.copy()

    #     img = Image.fromarray(frame)
    #     imgtk = ImageTk.PhotoImage(image=img)

    #     self.camera_label.imgtk = imgtk
    #     self.camera_label.configure(image=imgtk)

    #     self.after(10, self.update_camera)

    # def update_camera(self):
    #     if not hasattr(self, "camera_running") or not self.camera_running:
    #         return

    #     frame = self.picam2.capture_array()

    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     self.current_frame = frame.copy()

    #     img = Image.fromarray(frame)
    #     imgtk = ImageTk.PhotoImage(image=img)

    #     self.camera_label.imgtk = imgtk
    #     self.camera_label.configure(image=imgtk)

    #     self.after(10, self.update_camera)
    def update_camera(self):
        if not hasattr(self, "camera_running") or not self.camera_running:
            return

        frame = self.picam2.capture_array()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.current_frame = frame.copy()

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        self.camera_label.imgtk = imgtk
        self.camera_label.configure(image=imgtk)

        # 🔥 store after ID
        # self.after_id = self.after(10, self.update_camera)
        self.after(10, self.update_camera)

    def stop_camera(self):
        if hasattr(self, "camera_running") and self.camera_running:
            self.camera_running = False

            try:
                self.picam2.stop()
                self.picam2.close()
            except:
                pass

    # def stop_camera(self):
    #     if hasattr(self, "camera_running") and self.camera_running:
    #         self.camera_running = False

    #         # 🔥 cancel loop
    #         if hasattr(self, "after_id"):
    #             self.after_cancel(self.after_id)

    #         try:
    #             self.picam2.stop()
    #             self.picam2.close()
    #         except Exception as e:
    #             print("Stop camera error:", e)

    def show_preview(self):
        if self.current_frame is None:
            return

        # Convert numpy → PIL
        img = Image.fromarray(self.current_frame)

        # Resize to fit preview container
        img = img.resize((370, 260))

        # Convert to CTkImage (correct for CTkLabel)
        ctk_img = ctk.CTkImage(light_image=img, size=(350, 240))

        # Store reference (IMPORTANT to avoid garbage collection)
        self.preview_ctk_img = ctk_img

        # Display
        self.preview_label.configure(image=ctk_img)

    def capture_eye(self):
        if self.current_frame is None:
            print("No frame available")

        self.show_preview()

    def save_eye_scan(self):
        import os
        from datetime import datetime

        if self.current_frame is None:
            return

        patient_id = self.controller.current_user[0]
        question_id = self.controller.current_question_id

        if not question_id:
            mb(
                self,
                title="Error",
                message="No active test session.",
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

        upload_dir = "assets/uploads"
        predicted_dir = "assets/predictions"

        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(predicted_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # ✅ RAW IMAGE SAVE
        filename = f"eye_{patient_id}_{question_id}_{timestamp}.jpg"
        filepath = os.path.join(upload_dir, filename)

        # 🔥 IMPORTANT FIX (RGB → BGR)
        frame_bgr = cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite(filepath, frame_bgr)

        try:
            # ✅ RUN YOLO ON SAVED IMAGE
            result = self.eye_model.predict(
                filepath,
                predicted_dir,
                conf=0.40,
            )
            print("YOLO RESULT:", result)

            eye_classification = result["classification"]
            eye_confidence = result["confidence"]
            eye_scan_path = result["eye_scan_path"]

            # ✅ FIX HERE
            self.eye_classification = eye_classification
            self.eye_confidence = eye_confidence

            # 🚫 VALIDATION (VERY IMPORTANT)
            if eye_classification == "Unknown" or eye_confidence == 0.0:
                mb(
                    self,
                    title="Detection Failed",
                    message="No eye condition detected. Please try again with a clearer image.",
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

            # ✅ ONLY runs if valid detection
            saved = self.controller.db.save_eye_image(
                question_id,
                filepath,
                eye_scan_path,
                eye_classification,
                eye_confidence,
            )

            if saved:
                # mb(
                #     self,
                #     title="Saved Predictions",
                #     message="Eye scan saved successfully.",
                #     options=("Okay",),
                #     icon="check",
                #     fg_color="#FFFFFF",
                #     border_width=1,
                #     border_color="#E2E8F0",
                #     text_color="#0F172A",
                #     title_color="#0F172A",
                #     font=("Inter", 16),
                #     height=260,
                #     button_color="#14B8A6",
                #     button_hover_color="#0D9488",
                #     button_text_color="#FFFFFF",
                #     button_width=100,
                #     button_height=55,
                # )
                # Handle Risk Level and Recommendation
                self.load_patient_test_results()

                self.clean_up()
                self.result_modal()

                # self.controller.change_window("ResultsPage")
            else:
                mb(
                    self,
                    title="Save Error",
                    message="Failed to save eye scan.",
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

        except Exception as e:
            # mb.showerror("Model Error", str(e))
            mb(
                self,
                title="Model Error",
                message=f"Error {str(e)}",
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

    def compute_risk(self, test_class, test_conf, eye_class, eye_conf):
        RISK_ORDER = {
            "Safe": 0,
            "Mild": 1,
            "Moderate": 2,
            "Severe": 3,
        }

        # Handle unknowns
        if test_class == "Unknown":
            return eye_class
        if eye_class == "Unknown":
            return test_class

        test_score = RISK_ORDER[test_class]
        eye_score = RISK_ORDER[eye_class]

        # 🔥 HARD SAFETY RULE
        if test_score == 3 or eye_score == 3:
            return "Severe"

        # 🔥 WEIGHTED WITH CONFIDENCE
        weighted_test = test_score * test_conf * 0.65
        weighted_eye = eye_score * eye_conf * 0.35

        final_score = weighted_test + weighted_eye

        final_index = round(final_score)

        # Clamp just in case
        final_index = max(0, min(3, final_index))

        for key, value in RISK_ORDER.items():
            if value == final_index:
                return key

    def load_patient_test_results(self):

        question_id = self.controller.current_question_id

        test_result = self.controller.db.load_test_results(question_id)

        if not test_result:
            mb(
                self,
                title="Error",
                message="Test results not found.",
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

        test_class = test_result["classification"]
        test_conf = test_result["confidence"]

        eye_class = self.eye_classification
        eye_conf = self.eye_confidence

        # 🔥 Compute
        final_risk = self.compute_risk(test_class, test_conf, eye_class, eye_conf)
        recommendation = self.get_recommendation(final_risk)

        # # ✅ Save to controller
        # self.controller.final_risk = final_risk
        # self.controller.recommendation = recommendation

        print("FINAL RISK:", final_risk)
        print("RECOMMENDATION:", recommendation)

        # ✅ Save to DB
        saved = self.controller.db.save_risk_and_recommendation(
            question_id,
            final_risk,
            recommendation,
        )

        if not saved:
            # print("Failed to save risk and recommendation")
            mb(
                self,
                title="Error",
                message="Failed to save risk and recommendation",
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

    def get_recommendation(self, risk_level):
        for r in RECOMMENDATIONS:
            if r["classification"] == risk_level:
                return r["recommendation"]
        return "No recommendation available."

    def result_modal(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        self.top = EyeResultModal(self, controller=self.controller, x=x, y=y)

        self.top.title("LeptoSight")
        self.top.geometry(f"1130x840+{x+180}+{y}")
        self.top.transient(self)
        self.top.grab_set()
        self.top.populate_data()

    def card_builder(self):
        start_y = 90
        gap = 80

        for i, item in enumerate(CAMERA_TIPS):
            y_position = start_y + (i * gap)

            card = ctk.CTkFrame(
                self.instruction_container,
                width=340,
                height=70,
                fg_color="#EEF2F7",
                corner_radius=10,
            )
            card.place(x=20, y=y_position)

            # ICON
            icon_image = (
                self.tips_icons[i] if i < len(self.tips_icons) else self.bell_icon
            )

            Avatar(
                card,
                image=icon_image,
                width=50,
                height=50,
                fg_color="#14B8A6",
            ).place(x=12, y=10)

            # TITLE
            ctk.CTkLabel(
                card,
                text=item.get("title", ""),
                font=("Inter", 17),
                text_color=TEXT_PRIMARY,
            ).place(x=70, y=7)

            # SUBTITLE
            ctk.CTkLabel(
                card,
                text=item.get("sub_title", ""),
                font=("Poppins", 14),
                text_color=TEXT_SECONDARY,
            ).place(x=70, y=30)

    def clear_fields(self):
        # 🔥 RESET STATE
        self.current_frame = None
        self.preview_ctk_img = None
        self.eye_classification = None
        self.eye_confidence = None

        # 🔥 RESET PREVIEW
        self.preview_label.configure(image="", text="")

        # 🔥 RESET FLASH
        self.is_on = False
        try:
            self.flash_off()
        except:
            pass

        # 🔥 RESET BUTTONS (optional but good UX)
        self.capture_btn.configure(state="normal")
        self.save_eye.configure(state="normal")

    def on_show(self):
        # self.stop_camera()
        # self.start_camera()
        self.card_builder()
        # send_relay_on()


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
