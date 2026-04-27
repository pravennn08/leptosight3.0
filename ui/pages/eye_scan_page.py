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
    VIOLET_HOVER,
    YELLOW_HOVER,
    BLUE_HOVER,
    LOGO,
    ZOOM_IN,
)
from ..components.avatar import Avatar
from ..components.square import Square
from ..components.eye_result_modal import EyeResultModal
from CTkMessagebox import CTkMessagebox as mb


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
        self.eye_model = controller.eye_model

        self.current_frame = None
        self.preview_mode = False
        self.is_on = False
        self.flash_on = send_relay_on
        self.flash_off = send_relay_off
        self.clean_up = cleanup

        self.zoom_level = 1.0  # 1.0 = no zoom
        self.max_zoom = 4.0
        self.zoom_step = 0.5

        # IMAGE
        self.camera_prompt_img = ctk.CTkImage(
            Image.open(CAMERA_PROMPT), size=(360, 260)
        )

        # ICONS
        self.camera_icon = ctk.CTkImage(Image.open(CAMERA), size=(60, 60))
        self.flash_icon = ctk.CTkImage(Image.open(FLASH), size=(60, 60))
        self.save_icon = ctk.CTkImage(Image.open(SAVE), size=(60, 60))
        self.zoom_icon = ctk.CTkImage(Image.open(ZOOM_IN), size=(60, 60))

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
        ).place(x=20, y=10)
        ctk.CTkLabel(
            self,
            text="Please center your eye in the frame and hold steady while the scan is in progress.",
            font=("Poppins", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=20, y=60)

        self.container = ctk.CTkFrame(
            self,
            height=700,
            width=1000,
            fg_color="#E2E8F0",
            border_width=2,
            border_color="#E2E8F0",
            corner_radius=15,
        )
        self.container.place(x=20, y=100)

        self.camera_container = ctk.CTkFrame(
            self.container,
            height=650,
            width=950,
        )
        self.camera_container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.camera_label = tk.Label(self.camera_container, text="")
        self.camera_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # self.actions_container = ctk.CTkFrame(
        #     self,
        #     height=170,
        #     width=1000,
        #     fg_color="transparent",
        # )
        # self.actions_container.place(x=40, y=750)
        self.instruction_container = ctk.CTkFrame(
            self,
            height=650,
            width=380,
            # fg_color="#E2E8F0",
            fg_color="transparent",
            corner_radius=15,
        )
        self.instruction_container.place(x=1070, y=100)

        self.capture_btn = ctk.CTkButton(
            self.instruction_container,
            image=self.camera_icon,
            width=120,
            height=100,
            text="",
            fg_color=BLUE,
            hover=False,
            corner_radius=10,
            command=self.capture_eye,
            # compound="center",
        )
        self.capture_btn.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self.instruction_container,
            text="CAPTURE",
            font=("Inter", 16, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(relx=0.5, rely=0.60, anchor=ctk.CENTER)

        self.open_flash = ctk.CTkButton(
            self.instruction_container,
            image=self.flash_icon,
            width=120,
            height=100,
            text="",
            fg_color=YELLOW,
            hover=False,
            corner_radius=10,
            command=self.toggle_flash,
            # compound="center",
        )
        self.open_flash.place(relx=0.5, rely=0.29, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self.instruction_container,
            text="FLASH",
            font=("Inter", 16, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(relx=0.5, rely=0.39, anchor=ctk.CENTER)

        self.save_eye = ctk.CTkButton(
            self.instruction_container,
            image=self.save_icon,
            width=120,
            height=100,
            fg_color=PRIMARY,
            hover=False,
            text="",
            corner_radius=10,
            # compound="center",
            command=self.save_eye_scan,
        )
        self.save_eye.place(relx=0.5, rely=0.71, anchor=ctk.CENTER)
        ctk.CTkLabel(
            self.instruction_container,
            text="SAVE",
            font=("Inter", 16, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(relx=0.5, rely=0.81, anchor=ctk.CENTER)

        self.zoom_eye_btn = ctk.CTkButton(
            self.instruction_container,
            image=self.zoom_icon,
            width=120,
            height=100,
            text="",
            fg_color=VIOLET,
            hover=False,
            corner_radius=10,
            command=self.zoom_eye,
        )
        self.zoom_eye_btn.place(relx=0.5, rely=0.08, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self.instruction_container,
            text="ZOOM",
            font=("Inter", 16, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(relx=0.5, rely=0.18, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self,
            text="PREVIEW",
            font=("Inter", 16, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(x=1225, y=800)

        self.preview_container = ctk.CTkFrame(
            self,
            height=150,
            width=170,
            fg_color="#E2E8F0",
            corner_radius=15,
        )
        self.preview_container.place(x=1180, y=650)

        self.preview_frame = ctk.CTkFrame(
            self.preview_container,
            height=120,
            width=150,
            fg_color="transparent",
        )
        self.preview_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="",
        )
        self.preview_label.pack(expand=True)

    def zoom_eye(self):
        if not hasattr(self, "picam2"):
            return

        if self.zoom_level == 1.0:
            self.zoom_level = 4.0
        else:
            self.zoom_level = 1.0

        sensor_width, sensor_height = self.picam2.camera_properties["PixelArraySize"]

        crop_width = int(sensor_width / self.zoom_level)
        crop_height = int(sensor_height / self.zoom_level)

        crop_x = (sensor_width - crop_width) // 2
        crop_y = (sensor_height - crop_height) // 2

        self.picam2.set_controls(
            {"ScalerCrop": (crop_x, crop_y, crop_width, crop_height)}
        )

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
        self.zoom_level = 1.0

        config = self.picam2.create_preview_configuration(
            main={"size": (1000, 650), "format": "RGB888"}
        )

        self.picam2.configure(config)
        self.picam2.start()

        self.camera_running = True
        self.update_camera()

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

        self.after(10, self.update_camera)

    def stop_camera(self):
        if hasattr(self, "camera_running") and self.camera_running:
            self.camera_running = False

            try:
                self.picam2.stop()
                self.picam2.close()
            except:
                pass

    def show_preview(self):
        if self.current_frame is None:
            return

        # Convert numpy → PIL
        img = Image.fromarray(self.current_frame)

        # Resize to fit preview container
        img = img.resize((150, 120))

        # Convert to CTkImage (correct for CTkLabel)
        ctk_img = ctk.CTkImage(light_image=img, size=(140, 110))

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
                self.stop_camera()

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

        # Convert confidence to 0–1
        test_conf = test_conf / 100
        eye_conf = eye_conf / 100

        # Handle unknowns
        if test_class == "Unknown":
            return eye_class
        if eye_class == "Unknown":
            return test_class

        test_score = RISK_ORDER[test_class]
        eye_score = RISK_ORDER[eye_class]

        # 🔥 HARD RULE (VERY GOOD - KEEP THIS)
        if test_score == 3 or eye_score == 3:
            return "Severe"

        if test_score > eye_score:
            return test_class

        # 🔥 NORMALIZED WEIGHTED SCORE
        weighted_score = (test_score * test_conf * 0.65) + (eye_score * eye_conf * 0.35)

        # 🔥 NORMALIZE by total weight contribution
        total_weight = (test_conf * 0.65) + (eye_conf * 0.35)

        if total_weight == 0:
            final_score = 0
        else:
            final_score = weighted_score / total_weight

        # 🔥 SMART THRESHOLDS (BETTER THAN ROUND)
        if final_score < 0.75:
            return "Safe"
        elif final_score < 1.5:
            return "Mild"
        elif final_score < 2.5:
            return "Moderate"
        else:
            return "Severe"

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

    def clear_fields(self):
        # 🔥 RESET STATE
        self.current_frame = None
        self.preview_ctk_img = None
        self.eye_classification = None
        self.eye_confidence = None

        # 🔥 RESET PREVIEW
        # self.preview_label.configure(image="", text="")

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
        pass
        # self.stop_camera()
        # self.start_camera()
        # self.card_builder()
        # send_relay_on()
