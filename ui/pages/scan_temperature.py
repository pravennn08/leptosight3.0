import customtkinter as ctk
import time
import subprocess
from PIL import Image
from hardware.mlx90164 import send_temperature
from constants.seeds import (
    BEEP,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    CAMERA,
    FLASH,
    SAVE,
    CHECK,
    BLUE,
    RED,
    DISTANCE,
    EYE,
    CAMERA_TIPS,
    CAMERA_PROMPT,
    RETRY,
    GREEN,
    TEMP,
    YELLOW,
    ORANGE,
)
from ..components.avatar import Avatar
from CTkMessagebox import CTkMessagebox as mb


class ScanTemperaturePage(ctk.CTkFrame):
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
        self.timer_running = False

        # IMAGE
        self.camera_prompt_img = ctk.CTkImage(
            Image.open(CAMERA_PROMPT), size=(360, 260)
        )

        # ICONS
        self.scan_icon = ctk.CTkImage(Image.open(TEMP), size=(70, 70))
        self.retry_icon = ctk.CTkImage(Image.open(RETRY), size=(50, 50))
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
            self,
            text="Scan Temperature",
            font=("Arial", 33, "bold"),
            text_color=TEXT_PRIMARY,
        ).place(x=40, y=10)
        ctk.CTkLabel(
            self,
            text="Position your forehead from IR temperature sensor.",
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

        self.curr_progress = 0.0
        self.temp_bar = ctk.CTkProgressBar(
            self.container,
            orientation="horizontal",
            width=500,
            height=20,
            corner_radius=15,
            fg_color="#FFFFFF",
            progress_color="#14B8A6",
        )
        self.temp_bar.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)
        self.temp_bar.set(self.curr_progress)

        self.temp_label = ctk.CTkLabel(
            self.container,
            text="--.- °C",
            font=("Inter", 100, "bold"),
            text_color=TEXT_PRIMARY,
        )
        self.temp_label.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

        self.status_label = ctk.CTkLabel(
            self.container,
            text="--",
            font=("Inter", 50, "bold"),
            text_color=TEXT_SECONDARY,
        )
        self.status_label.place(relx=0.5, rely=0.60, anchor=ctk.CENTER)

        self.actions_container = ctk.CTkFrame(
            self,
            height=160,
            width=1000,
            fg_color="transparent",
        )
        self.actions_container.place(x=40, y=750)

        self.countdown = 6

        self.scan_temp_btn = ctk.CTkButton(
            self.actions_container,
            image=self.scan_icon,
            width=150,
            height=100,
            text="",
            # fg_color=BLUE,
            # hover_color="#0284C7",
            fg_color=RED,
            corner_radius=10,
            # compound="center",
            text_color="#FFFFFF",
            font=("Inter", 55, "bold"),
            command=self.start_timer,
        )
        self.scan_temp_btn.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        ctk.CTkLabel(
            self.actions_container,
            text="SCAN",
            font=("Inter", 16, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

        # self.retry_temp_btn = ctk.CTkButton(
        #     self.actions_container,
        #     image=self.retry_icon,
        #     width=100,
        #     height=90,
        #     text="",
        #     fg_color=BLUE,
        #     corner_radius=10,
        #     # compound="center",
        #     command=self.retry_scan,
        # )
        # self.retry_temp_btn.place(relx=0.35, rely=0.42, anchor=ctk.CENTER)

        # ctk.CTkLabel(
        #     self.actions_container,
        #     text="RETRY",
        #     font=("Inter", 16, "bold"),
        #     text_color=TEXT_SECONDARY,
        # ).place(relx=0.35, rely=0.85, anchor=ctk.CENTER)

        self.save_temp_btn = ctk.CTkButton(
            self.actions_container,
            image=self.save_icon,
            width=100,
            height=90,
            text="",
            fg_color="#14B8A6",
            corner_radius=10,
            # compound="center",
            command=self.save_temperature,
        )
        self.save_temp_btn.place(relx=0.65, rely=0.42, anchor=ctk.CENTER)

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
            border_width=2,
            border_color="#E2E8F0",
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
            text="IDEAL POSITION",
            font=("Inter", 16, "bold"),
            text_color=TEXT_SECONDARY,
        ).place(x=1075, y=560)

        self.prompt_container = ctk.CTkFrame(
            self,
            height=270,
            width=380,
            fg_color="#E2E8F0",
            border_width=2,
            border_color="#E2E8F0",
            corner_radius=15,
        )
        self.prompt_container.place(x=1070, y=595)

        self.camera_prompt = ctk.CTkFrame(
            self.prompt_container,
            height=260,
            width=370,
            fg_color="transparent",
        )
        self.camera_prompt.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.camera_prompt_label = ctk.CTkLabel(
            self.camera_prompt,
            text="",
            image=self.camera_prompt_img,
        ).pack()

    # def start_timer(self):
    #     if self.countdown > 0:
    #         self.countdown -= 1
    #         self.scan_temp_btn.configure(
    #             text=self.countdown, image=None, state="disabled"
    #         )

    #         self.after(1000, self.start_timer)

    #     else:
    #         self.scan_temperature()
    #         self.scan_temp_btn.configure(
    #             text="", image=self.scan_icon, state="disabled"
    #         )

    def start_timer(self):
        if self.timer_running:
            return

        self.timer_running = True
        self.countdown = 6
        self._run_timer()

    def _run_timer(self):
        if not self.timer_running:
            return

        if self.countdown > 0:
            self.countdown -= 1
            self.scan_temp_btn.configure(
                text=self.countdown, image=None, state="disabled"
            )
            self.after(1000, self._run_timer)
        else:
            if self.timer_running:  # extra safety
                self.scan_temperature()

            self.scan_temp_btn.configure(
                text="", image=self.scan_icon, state="disabled"
            )
            self.timer_running = False

    def beep(self):
        try:
            subprocess.Popen(["paplay", BEEP])
        except Exception as e:
            print("Beep error:", e)

    def temp_to_progress(self, temp):
        min_temp = 34.0
        max_temp = 42.0
        temp = max(min(temp, max_temp), min_temp)
        return (temp - min_temp) / (max_temp - min_temp)

    def animate_progress(self, target, color):
        step = 0.005

        def step_animation():
            if abs(self.curr_progress - target) > step:
                if self.curr_progress < target:
                    self.curr_progress += step
                else:
                    self.curr_progress -= step

                self.temp_bar.set(self.curr_progress)
                self.temp_bar.configure(progress_color=color)

                self.after(10, step_animation)
            else:
                self.curr_progress = target
                self.temp_bar.set(target)

        step_animation()

    def get_temp_status(self, temp):
        if temp < 36.0:
            return ORANGE, "HYPOTHERMIA"
        elif temp <= 37.0:
            return GREEN, "NORMAL"
        elif temp <= 38.0:
            return YELLOW, "SUBFEBRILE"
        else:
            return RED, "FEVER"

    def scan_temperature(self):
        temp = send_temperature()
        target = self.temp_to_progress(temp)

        if self.last_temp is None:
            self.last_temp = temp
        smooth_temp = (self.last_temp * 0.7) + (temp * 0.3)
        self.last_temp = smooth_temp

        self.rounded_temp = round(smooth_temp, 1)
        color, status = self.get_temp_status(self.rounded_temp)
        self.animate_progress(target, color)
        self.beep()

        self.temp_label.configure(text=f"{self.rounded_temp:.1f} °C")
        self.status_label.configure(text=status, text_color=color)

        print(f"{self.rounded_temp:.1f} °C")

    def validate_data(self):
        temp = getattr(self, "rounded_temp", None)

        if temp is None:
            return "Please scan your temperature first"

        if temp < 30:
            return "Invalid temperature reading. Please scan again."

        return None

    def save_temperature(self):
        error = self.validate_data()
        if error:
            mb(
                self,
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

        try:
            patient_id = self.controller.current_user[0]
            temp = self.rounded_temp

            question_id = self.db.save_temperature(patient_id, temp)

            if question_id:
                self.controller.current_question_id = question_id
                mb(
                    self,
                    title="Saved Temperature",
                    message="Temperature save successful",
                    options=("Thanks",),
                    icon="check",
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
                self.stop_timer()
                self.controller.change_window("QuestionsPage")
            else:
                mb(
                    self,
                    title="Error",
                    message="Failed to save responses",
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

        except Exception as error:
            mb(
                self,
                title="Error",
                message=error,
                options=("Okay"),
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
                corner_radius=12,
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

    def stop_timer(self):
        self.timer_running = False

    def clear_fields(self):
        # 🔥 RESET STATE
        self.rounded_temp = None
        self.last_temp = None
        self.countdown = 6
        self.curr_progress = 0.0

        # 🔥 RESET UI
        self.temp_bar.set(0)
        self.temp_label.configure(text="--.- °C")
        self.status_label.configure(text="--", text_color=TEXT_SECONDARY)

        # 🔥 RESET BUTTON
        self.scan_temp_btn.configure(text="", image=self.scan_icon, state="normal")

    def on_show(self):
        self.beep()
        self.card_builder()
