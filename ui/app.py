import customtkinter as ctk
import re
from service.service import DatabaseService
from constants.seeds import BACKGROUND
from .components.sidebar import AppSideBar
from .components.navbar import AppNavBar
from .pages.sign_in_page import SignInPage
from .pages.sign_up_page import SignUpPage
from .pages.verify_otp_page import VerifyOTPPage
from .pages.account_verification_page import AccountVerificationPage
from .pages.home_page import HomePage
from .pages.test_page import StartTestPage
from .pages.scan_temperature import ScanTemperaturePage
from .pages.questions_page import QuestionsPage
from .pages.eye_scan_page import EyeScanPage
from .pages.result_page import ResultsPage
from .pages.records_page import RecordsPage
from .pages.settings_page import SettingsPage
from .pages.profile_page import ProfilePage
from .pages.dashboard_page import DashboardPage
from .pages.patient_records_page import PatientRecordsPage
from .pages.users_page import UsersPage


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LeptoSight")
        self.geometry("1200x700")
        self.configure(fg_color=BACKGROUND)

        # PAGES
        self.frames = {}

        # DB SERVICE
        self.db = DatabaseService()

        # AUTH SESSION
        self.current_user = None
        self.recovery_user = None
        self.current_question_id = None

        # SIDEBAR (LEFT)
        self.sidebar = AppSideBar(self, self)
        self.sidebar.pack(side="left", fill="y", pady=10, padx=10)

        # RIGHT SIDE CONTAINER
        self.container = ctk.CTkFrame(self, fg_color=BACKGROUND)
        self.container.pack(side="left", fill="both", expand=True)

        # NAVBAR (TOP)
        self.navbar = AppNavBar(self.container, self)
        self.navbar.pack(
            side="top",
            fill="x",
            pady=(0, 10),
            padx=(5, 20),
        )

        # CONTENT
        self.content = ctk.CTkFrame(self.container, fg_color="transparent")
        self.content.pack(
            fill="both",
            expand=True,
            padx=(10, 20),
            pady=(0, 10),
        )

        # AUTH PAGES
        self.frames["SignInPage"] = SignInPage(self, self)
        self.frames["SignUpPage"] = SignUpPage(self, self)
        self.frames["VerifyOTPPage"] = VerifyOTPPage(self, self)
        self.frames["AccountVerificationPage"] = AccountVerificationPage(self, self)

        # PATIENT-SIDE PAGES
        self.frames["HomePage"] = HomePage(self.content, self)
        self.frames["StartTestPage"] = StartTestPage(self.content, self)
        self.frames["ScanTemperaturePage"] = ScanTemperaturePage(self.content, self)
        self.frames["QuestionsPage"] = QuestionsPage(self.content, self)
        self.frames["EyeScanPage"] = EyeScanPage(self.content, self)
        self.frames["ResultsPage"] = ResultsPage(self.content, self)
        self.frames["RecordsPage"] = RecordsPage(self.content, self)
        self.frames["ProfilePage"] = ProfilePage(self.content, self)

        # ADMIN/PERSONNEL-SIDE PAGES
        self.frames["DashboardPage"] = DashboardPage(self.content, self)
        self.frames["PatientRecordsPage"] = PatientRecordsPage(self.content, self)
        self.frames["UsersPage"] = UsersPage(self.content, self)
        self.frames["SettingsPage"] = SettingsPage(self.content, self)

        self.change_window("SignInPage")

    # CHANGE WINDOW
    def change_window(self, name):
        for frame in self.frames.values():
            frame.pack_forget()

        page = self.frames[name]

        if hasattr(page, "clear_fields"):
            page.clear_fields()

        # AUTH PAGE (FULL SCREEN)
        if name in [
            "SignInPage",
            "SignUpPage",
            "VerifyOTPPage",
            "AccountVerificationPage",
        ]:
            self.sidebar.pack_forget()
            self.container.pack_forget()

            page.pack(fill=ctk.BOTH, expand=True)

        else:
            self.sidebar.pack(
                side="left",
                fill="y",
                pady=10,
                padx=10,
            )

            self.container.pack(side="left", fill="both", expand=True)

            self.navbar.pack(
                side="top",
                fill="x",
                pady=(0, 10),
                padx=(5, 20),
            )

            page.pack(fill=ctk.BOTH, expand=True)
            self.navbar.set_title(
                re.sub(r"(?<!^)(?=[A-Z])", " ", name.replace("Page", ""))
            )

        if hasattr(page, "on_show"):
            page.on_show()
