import customtkinter as ctk
from PIL import Image


class PatientRecordsPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color="#F8FAFC",
            border_width=1,
            border_color="#E2E8F0",
        )
        self.controller = controller

        ctk.CTkLabel(self, text="PATIENT RECORDS").pack(expand=True)
