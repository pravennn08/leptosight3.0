import customtkinter as ctk
from PIL import Image
from constants.seeds import (
    BACKGROUND,
    PHONE,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    PRIMARY,
    SECONDARY,
    LOGO,
    BLUE,
)
from ..components.square import Square
from ..components.messagebox import MessageBox as mb


class VerifyOTPPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color=BACKGROUND,
        )
        self.controller = controller
        self.db = controller.db

        # ICONS
        self.phone_icon = ctk.CTkImage(Image.open(PHONE), size=(70, 70))

        # CARD CONTAINER
        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent",
            # fg_color="gray",
            # border_width=1,
            # border_color="#E2E8F0",
            # corner_radius=12,
            width=650,
            height=750,
        )
        self.container.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        Square(
            self.container,
            image=self.phone_icon,
            size=100,
            fg_color=PRIMARY,
        ).place(relx=0.5, rely=0.1, anchor=ctk.N)
        ctk.CTkLabel(
            self.container, text="OTP Verification", font=("Inter", 35, "bold")
        ).place(relx=0.5, rely=0.27, anchor=ctk.N)

        self.phone_number = ctk.CTkLabel(
            self.container,
            text="We sent a code to +64747474422",
            text_color=TEXT_SECONDARY,
            font=("Phone", 20),
        )
        self.phone_number.place(relx=0.5, rely=0.34, anchor=ctk.N)

        self.otp_frame = ctk.CTkFrame(
            self.container, fg_color="transparent", width=600, height=100
        )
        self.otp_frame.place(relx=0.5, rely=0.45, anchor=ctk.N)
        self.create_boxes()
        self.resend_label = ctk.CTkLabel(
            self.container,
            text="Resend code in 60s",
            text_color=TEXT_SECONDARY,
            font=("Poppins", 18),
        )
        self.resend_label.place(relx=0.84, rely=0.6, anchor=ctk.N)

        self.verify_otp_btn = ctk.CTkButton(
            self.container,
            text="Verify",
            width=580,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            font=("Inter", 22, "bold"),
            height=60,
            corner_radius=12,
            text_color="#FFFFFF",
            cursor="hand2",
            command=self.verify_otp,
        ).place(relx=0.5, rely=0.7, anchor=ctk.N)

    def load_phone_number(self):
        user = self.controller.current_user
        print(user)

        if user:
            phone_number = user[3]
            self.phone_number.configure(text=f"We sent a code to {phone_number}")

    def create_boxes(self):
        self.otp_entries = []

        vcmd = (self.register(self.only_numbers), "%P")

        for i in range(6):
            entry = ctk.CTkEntry(
                self.otp_frame,
                width=90,
                height=90,
                justify="center",
                font=("Poppins", 35),
                validate="key",
                validatecommand=vcmd,
                fg_color="#F3F4F6",
                border_color="#E5E7EB",
                border_width=3,
            )

            # spacing for dash
            col = i if i < 3 else i + 1
            entry.grid(row=0, column=col, padx=5)

            entry.bind("<KeyRelease>", lambda e, idx=i: self.handle_key(e, idx))
            self.otp_entries.append(entry)

        ctk.CTkLabel(self.otp_frame, text="-", font=("Poppins", 35, "bold")).grid(
            row=0, column=3, padx=5
        )

    def handle_key(self, event, index):
        value = self.otp_entries[index].get()

        # enforce single digit
        if len(value) > 1:
            self.otp_entries[index].delete(1, "end")
            return

        # move forward
        if value and index < 5:
            self.otp_entries[index + 1].focus()

        # move backward
        if event.keysym == "BackSpace" and index > 0 and not value:
            self.otp_entries[index - 1].focus()

    def only_numbers(self, value):
        return value.isdigit() or value == ""

    def verify_otp(self):
        otp = "".join(entry.get() for entry in self.otp_entries)

        if len(otp) != 6:
            # mb.showerror("Invalid OTP", "Please enter the 6-digit code.")
            mb(
                title="Invalid OTP",
                message="Please enter the 6-digit code.",
                options=("Okay",),
                icon="cancel",
            ).show()
            return

        user = self.controller.current_user
        if not user:
            # mb.showerror("Session Error", "Verification session expired.")
            mb(
                title="Session Error",
                message="Verification session expired.",
                options=("Okay",),
                icon="cancel",
            ).show()
            self.controller.change_window("SignInPage")
            return

        phone = user[3]
        result = self.controller.db.verify_otp(phone, otp)

        if isinstance(result, dict) and result["status"] == "RATE_LIMITED":
            seconds = result["remaining"]
            minutes = seconds // 60

            # mb.showerror(
            #     "Too Many Attempts",
            #     f"Too many OTP attempts.\nTry again in {minutes} minute(s).",
            # )
            mb(
                title="Too Many Attempts",
                message=f"Too many OTP attempts.\nTry again in {minutes} minute(s).",
                options=("Okay",),
                icon="cancel",
            ).show()
            return

        if result == "SETUP_RECOVERY_REQUIRED":
            # mb.showinfo(
            #     "OTP",
            #     "Verification successful. Please complete account verification.",
            # )
            mb(
                title="OTP Verification",
                message="Verification successful. Please complete account verification.",
                options=("Got It",),
                icon="check",
            ).show()

            self.controller.change_window("AccountVerificationPage")

        elif result == "VERIFIED":
            # mb.showinfo("OTP", "Verification successful. Please login.")
            mb(
                title="OTP Verification",
                message="Verification successful. Please login your account.",
                options=("Got It",),
                icon="check",
            ).show()

            self.controller.change_window("SignInPage")

        elif result == "INVALID_OTP":
            # mb.showerror("OTP", "Incorrect OTP.")
            mb(
                title="OTP Invalid",
                message="Incorrect OTP.",
                options=("Okay",),
                icon="cancel",
            ).show()
            self.clear_fields()
        elif result == "OTP_EXPIRED":
            self.clear_fields()
            # mb.showerror("OTP", "OTP expired.")
            mb(
                title="OTP Expired",
                message="OTP expired.",
                options=("Okay",),
                icon="cancel",
            ).show()
        else:
            self.clear_fields()
            # mb.showerror("OTP", "Verification failed.")
            mb(
                title="OTP Failed",
                message="Verification failed.",
                options=("Okay",),
                icon="cancel",
            ).show()

    def start_timer(self):
        if self.countdown > 0:
            self.resend_label.configure(text=f"Resend code in {self.countdown}s")
            self.countdown -= 1
            self.after(1000, self.start_timer)
        else:
            self.resend_label.configure(text="Resend Code", text_color=PRIMARY)
            self.resend_label.bind("<Button-1>", self.resend_code)

    def resend_code(self, event=None):
        phone = self.controller.current_user[3]

        if self.controller.db.resend_otp(phone):
            # mb.showinfo("OTP", "New OTP sent.")
            mb(
                title="Resend OTP",
                message="New OTP sent.",
                options=("Thanks",),
                icon="info",
            ).show()

        # reset timer
        self.countdown = 60
        self.resend_label.unbind("<Button-1>")
        self.resend_label.configure(text_color="gray")

        self.start_timer()

    def on_show(self):
        self.load_phone_number()
        self.countdown = 180
        self.start_timer()
        self.after(100, lambda: self.otp_entries[0].focus())

    def clear_fields(self):
        for entry in self.otp_entries:
            entry.delete(0, "end")

        self.otp_entries[0].focus()
