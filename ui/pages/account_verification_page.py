import customtkinter as ctk
from PIL import Image
from tkcalendar import Calendar
from constants.seeds import (
    BACKGROUND,
    ACCOUNT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    PRIMARY,
    SECONDARY,
    CALENDAR,
)
from ..components.square import Square
from CTkMessagebox import CTkMessagebox as mb
from datetime import datetime


class AccountVerificationPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color=BACKGROUND,
        )
        self.controller = controller
        self.db = controller.db

        # ICONS
        self.account_icon = ctk.CTkImage(Image.open(ACCOUNT), size=(70, 70))
        self.calendar_icon = ctk.CTkImage(Image.open(CALENDAR), size=(35, 35))

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
            image=self.account_icon,
            size=100,
            fg_color=PRIMARY,
        ).place(x=40, y=40)
        ctk.CTkLabel(
            self.container, text="Account Verification", font=("Inter", 32, "bold")
        ).place(x=160, y=70)

        ctk.CTkLabel(
            self.container,
            text="Please confirm your account details to continue",
            text_color=TEXT_SECONDARY,
            font=("Poppins", 21.5),
        ).place(x=40, y=160)

        ctk.CTkLabel(
            self.container,
            text="In what city or municipality were you born?",
            font=("Poppins", 20),
            text_color=TEXT_PRIMARY,
        ).place(x=40, y=210)

        self.city_entry = ctk.CTkEntry(
            self.container,
            width=530,
            height=60,
            corner_radius=9,
            font=("Poppins", 20),
            text_color=TEXT_PRIMARY,
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.city_entry.place(x=40, y=250)

        ctk.CTkLabel(
            self.container,
            text="What is your mother’s first name?",
            font=("Poppins", 20),
            text_color=TEXT_PRIMARY,
        ).place(x=40, y=325)

        self.mothers_name_entry = ctk.CTkEntry(
            self.container,
            width=530,
            height=60,
            corner_radius=9,
            font=("Poppins", 20),
            text_color=TEXT_PRIMARY,
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.mothers_name_entry.place(x=40, y=365)

        ctk.CTkLabel(
            self.container,
            text="When is your birthday?",
            font=("Poppins", 20),
            text_color=TEXT_PRIMARY,
        ).place(x=40, y=440)

        self.birthday_entry = ctk.CTkEntry(
            self.container,
            width=530,
            height=60,
            corner_radius=9,
            font=("Poppins", 20),
            text_color=TEXT_PRIMARY,
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.birthday_entry.place(x=40, y=480)

        self.calendar_btn = ctk.CTkButton(
            self.container,
            width=43,
            height=47,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            hover=False,
            # cursor="hand2",
            image=self.calendar_icon,
            text="",
            command=self.show_calendar,
        )
        self.calendar_btn.place(x=514, y=487)

        self.confirm_btn = ctk.CTkButton(
            self.container,
            text="Verify",
            width=530,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            font=("Inter", 22, "bold"),
            height=60,
            corner_radius=9,
            text_color="#FFFFFF",
            cursor="hand2",
            command=self.save_data,
        ).place(x=40, y=580)

    def show_calendar(self):

        if hasattr(self, "cal_window") and self.cal_window.winfo_exists():
            self.cal_window.focus()
            return

        self.cal_window = ctk.CTkToplevel(self)
        self.cal_window.title("Calendar")
        self.cal_window.resizable(False, False)

        self.update_idletasks()

        # GET ENTRY POSITIO
        entry_x = self.city_entry.winfo_rootx()
        entry_y = self.city_entry.winfo_rooty()
        entry_w = self.city_entry.winfo_width()

        # popup size
        width = 450
        height = 450

        # POSITION (RIGHT SIDE OF ENTRY
        x = entry_x + entry_w + 30
        y = entry_y - 70

        self.cal_window.geometry(f"{width}x{height}+{x}+{y}")

        self.cal_window.transient(self)
        self.cal_window.grab_set()
        self.cal_window.focus()

        # CALENDA

        self.calendar = Calendar(
            self.cal_window,
            selectmode="day",
            date_pattern="mm/dd/yyyy",
            background="#FFFFFF",
            foreground="#0F172A",
            headersbackground="#F1F5F9",
            headersforeground="#334155",
            selectbackground=PRIMARY,
            selectforeground="white",
            weekendbackground="#F8FAFC",
            weekendforeground="#EF4444",
            bordercolor="#E2E8F0",
            font=("Inter", 17),
        )
        self.calendar.pack(pady=20, padx=20, fill="both", expand=True)

        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)

    def on_date_selected(self, event=None):
        selected_date = self.calendar.get_date()
        self.birthday_entry.configure(state="normal")
        self.birthday_entry.delete(0, "end")
        self.birthday_entry.insert(0, selected_date)
        self.birthday_entry.configure(state="readonly")
        self.cal_window.destroy()

    from datetime import datetime

    def validate_data(self):
        city = self.city_entry.get().strip()
        mother = self.mothers_name_entry.get().strip()
        birthday = self.birthday_entry.get().strip()

        if not city or not mother or not birthday:
            return "All fields are required."

        if len(city) < 2:
            return "City is too short."

        if len(mother) < 2:
            return "Mother's name is too short."

        try:
            parsed_date = datetime.strptime(birthday, "%m/%d/%Y")
            self.formatted_birthday = parsed_date.strftime("%Y-%m-%d")  # ✅ convert
        except ValueError:
            return "Invalid birthday format. Use MM/DD/YYYY."

        return None

    def save_data(self):
        error = self.validate_data()
        if error:
            # mb.showerror("Account Verification", error)
            mb(
                self,
                title="Account Verification",
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

        user = self.controller.current_user

        if not user:
            # mb.showerror("Session Error", "Session expired.")
            mb(
                self,
                title="Session Error",
                message="Session expired.",
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
            self.controller.change_window("SignInPage")
            return

        email = user[2]

        result = self.db.save_recovery_questions(
            email=email,
            city=self.city_entry.get().strip().lower(),
            mother_name=self.mothers_name_entry.get().strip().lower(),
            birthday=self.formatted_birthday,
        )

        if result == "RECOVERY_SAVED":
            # mb.showinfo("Success", "Account setup complete.")
            mb(
                title="Success",
                message="Account setup complete.",
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

            self.clear_fields()
            self.controller.change_window("SignInPage")
        else:
            # mb.showerror("Error", "Failed to save recovery details.")
            mb(
                title="Error",
                message="Failed to save recovery details.",
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

    def on_show(self):
        pass

    def clear_fields(self):
        self.city_entry.delete(0, ctk.END)
        self.mothers_name_entry.delete(0, ctk.END)
        self.birthday_entry.configure(state="normal")
        self.birthday_entry.delete(0, ctk.END)
