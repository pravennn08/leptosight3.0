import customtkinter as ctk

ctk.set_appearance_mode("light")  # medical apps are usually light
ctk.set_default_color_theme("blue")


class Rectangle(ctk.CTkFrame):
    def __init__(
        self,
        master,
        width=120,
        height=60,
        corner_radius=12,
        text="",
        font=("Arial", 14),
        text_color="black",
        image=None,
        fg_color="#F1F5F9",
        **kwargs,
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=corner_radius,
            fg_color=fg_color,
            **kwargs,
        )

        # Prevent resizing based on content
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.image = image

        # Center label (text + optional image)
        self.label = ctk.CTkLabel(
            self,
            text=text,
            font=font,
            text_color=text_color,
            image=self.image,
            compound="left" if image else None,  # image + text layout
        )

        self.label.place(relx=0.5, rely=0.5, anchor="center")


class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"1400x700")
        self.configure(fg_color="#f5f7fa")

        self.after(10, self.grab_set)

        self.build_ui()

    def build_ui(self):

        ctk.CTkLabel(self, text="Record Details", font=("Inter", 22, "bold")).place(
            x=30, y=20
        )
        Rectangle(
            self,
            width=170,
            height=50,
            corner_radius=8,
            text="Diagnostic Id: 11",
            fg_color="#14B8A6",
            text_color="#FFFFFF",
            font=("Inter", 15, "bold"),
        ).place(x=1200, y=20)

        ctk.CTkLabel(
            self,
            text="Date Created",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=30, y=70)

        self.date_created_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.date_created_entry.place(x=30, y=110)

        ctk.CTkLabel(
            self,
            text="Temperature",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=360, y=70)

        self.temperature_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.temperature_entry.place(x=360, y=110)

        ctk.CTkLabel(
            self,
            text="Test Classification",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=30, y=170)

        self.test_class_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.test_class_entry.place(x=30, y=210)

        ctk.CTkLabel(
            self,
            text="Test Confidence",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=360, y=170)

        self.test_conf_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.test_conf_entry.place(x=360, y=210)

        ctk.CTkLabel(
            self,
            text="Eye Classification",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=30, y=270)

        self.eye_class_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.eye_class_entry.place(x=30, y=310)

        ctk.CTkLabel(
            self,
            text="Eye Confidence",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=360, y=270)

        self.eye_conf_entry = ctk.CTkEntry(
            self,
            width=300,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.eye_conf_entry.place(x=360, y=310)

        ctk.CTkLabel(
            self,
            text="Test Contributing Factors",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=30, y=370)

        self.test_factors_text_box = ctk.CTkTextbox(
            self,
            width=300,
            height=200,
            corner_radius=9,
            fg_color="#E2E8F0",
            border_spacing=5,
            font=("Roboto", 18),
            text_color="#111827",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        self.test_factors_text_box.place(x=30, y=410)

        ctk.CTkLabel(
            self,
            text="Test Answers",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=360, y=370)

        self.test_answers_text_box = ctk.CTkTextbox(
            self,
            width=300,
            height=200,
            corner_radius=9,
            fg_color="#E2E8F0",
            border_spacing=5,
            font=("Roboto", 18),
            text_color="#111827",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        self.test_answers_text_box.place(x=360, y=410)

        ctk.CTkLabel(
            self,
            text="Eye Image",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=700, y=70)

        self.eye_image_container = ctk.CTkFrame(
            self,
            width=320,
            height=230,
            corner_radius=9,
            # fg_color="#F8FAFC",
            # border_color="#E2E8F0",
        )
        self.eye_image_container.place(x=700, y=110)

        ctk.CTkLabel(
            self,
            text="Eye Scan",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=1050, y=70)

        self.eye_scan_container = ctk.CTkFrame(
            self,
            width=320,
            height=230,
            corner_radius=9,
            # fg_color="#F8FAFC",
            # border_color="#E2E8F0",
        )
        self.eye_scan_container.place(x=1050, y=110)

        ctk.CTkLabel(
            self,
            text="Risk Level",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=700, y=350)

        self.risk_level_entry = ctk.CTkEntry(
            self,
            width=320,
            height=50,
            corner_radius=9,
            font=("Roboto", 18),
            fg_color="#F8FAFC",
            border_color="#E2E8F0",
        )
        self.risk_level_entry.place(x=700, y=390)

        ctk.CTkLabel(
            self,
            text="Recommendation",
            font=("Poppins", 17),
            text_color="#111827",
        ).place(x=700, y=450)

        self.recommendation_text_box = ctk.CTkTextbox(
            self,
            width=670,
            height=120,
            corner_radius=9,
            fg_color="#E2E8F0",
            border_spacing=5,
            font=("Roboto", 18),
            text_color="#111827",
            scrollbar_button_color="#6B7280",
            scrollbar_button_hover_color="#4B5563",
        )
        self.recommendation_text_box.place(x=700, y=490)

        ctk.CTkButton(
            self,
            width=170,
            height=50,
            text="Close",
            fg_color="#EF4444",
            font=("Inter", 18, "bold"),
        ).place(x=1200, y=630)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        self.button = ctk.CTkButton(
            self, text="Open Monitor", command=self.open_toplevel
        )
        self.button.pack(pady=50)

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)
        else:
            self.toplevel_window.focus()


app = App()
app.mainloop()
