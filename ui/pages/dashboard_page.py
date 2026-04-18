import customtkinter as ctk
from PIL import Image

from constants.seeds import (
    BELL,
    TRACK_ACTIVITY,
    PLUS,
    CHECK_TEST,
    RECEIPT,
    CALENDAR,
    VIOLET,
    GREEN,
    TEXT_SECONDARY,
    TEXT_PRIMARY,
    PRIMARY,
    SECONDARY,
    USER,
    BLUE,
    RISK,
    PINK,
    YELLOW,
    RECORDS,
    LIB,
    RED,
)
from ..components.avatar import Avatar
from ..components.animated_bar_chart import AnimatedBarChart
from ..components.animated_admin_line_chart import AnimatedAdminLineChart


class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            # fg_color="#F8FAFC",
            # border_width=1,
            # border_color="#E2E8F0",
            fg_color="transparent",
        )
        self.controller = controller
        self.admin_db = controller.admin_db

        # ICONS
        self.bell_icon = ctk.CTkImage(Image.open(BELL), size=(30, 30))
        self.records_icon = ctk.CTkImage(Image.open(LIB), size=(26, 26))
        self.track_icon = ctk.CTkImage(Image.open(TRACK_ACTIVITY), size=(30, 30))
        self.test_icon = ctk.CTkImage(Image.open(CHECK_TEST), size=(45, 45))
        self.users_icon = ctk.CTkImage(Image.open(USER), size=(45, 45))
        self.risk_icon = ctk.CTkImage(Image.open(RISK), size=(45, 45))

        self.welcome_frame = ctk.CTkFrame(
            self,
            height=170,
            width=1050,
            fg_color="#E2E8F0",
            corner_radius=20,
        )
        self.welcome_frame.place(x=0, y=0)

        self.icons = [self.users_icon, self.test_icon, self.risk_icon]
        self.colors = [PINK, VIOLET, RED]

        self.bell_container = Avatar(
            self.welcome_frame,
            width=60,
            height=60,
            image=self.bell_icon,
            fg_color=YELLOW,
        )
        self.bell_container.place(x=30, y=20)
        self.welcome_label = ctk.CTkLabel(
            self.welcome_frame, text="", font=("Inter", 25)
        )
        self.welcome_label.place(x=110, y=30)

        ctk.CTkLabel(
            self.welcome_frame,
            text="Centralized dashboard for managing users, tests, and leptospirosis risk data.",
            font=("Poppins", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=110, y=70)

        ctk.CTkButton(
            self.welcome_frame,
            text="View Records",
            font=("Arial", 21, "bold"),
            image=self.records_icon,
            compound="left",
            height=50,
            width=210,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            text_color="#FFFFFF",
            corner_radius=9,
            command=lambda: self.controller.change_window("PatientRecordsPage"),
        ).place(x=110, y=105)

        self.last_activity_frame = ctk.CTkFrame(
            self,
            height=120,
            width=390,
            fg_color="#E2E8F0",
            corner_radius=20,
        )
        self.last_activity_frame.place(x=1070, y=0)

        self.track_container = Avatar(
            self.last_activity_frame,
            width=60,
            height=60,
            image=self.track_icon,
            fg_color=BLUE,
        )
        self.track_container.place(x=30, y=20)

        ctk.CTkLabel(
            self.last_activity_frame,
            text="Last Activity",
            font=("Inter", 23),
        ).place(x=110, y=30)

        self.last_activity_label = ctk.CTkLabel(
            self.last_activity_frame,
            text="",
            font=("Poppins", 19),
            text_color=TEXT_SECONDARY,
        )
        self.last_activity_label.place(x=110, y=60)

        ctk.CTkLabel(
            self,
            text="Overview",
            font=("Inter", 22),
        ).place(x=20, y=190)
        self.home_card_positions = [0, 495, 985]

        self.graphs_container = ctk.CTkFrame(self, fg_color="transparent")
        self.graphs_container.place(x=0, y=410)

        self.line_graph_frame = ctk.CTkFrame(
            self.graphs_container,
            fg_color="#E2E8F0",
            width=720,
            corner_radius=20,
            height=510,
        )

        self.line_graph_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.line_graph_frame.pack_propagate(False)  # VERY IMPORTANT

        self.line_inner = ctk.CTkFrame(self.line_graph_frame, fg_color="transparent")
        self.line_inner.pack(fill="both", expand=True, padx=10, pady=10)

        # CHART
        self.line_chart = AnimatedAdminLineChart(self.line_inner)

        self.line_chart.pack(fill="both", expand=True)

        self.bar_graph_frame = ctk.CTkFrame(
            self.graphs_container,
            fg_color="#E2E8F0",
            corner_radius=20,
            height=510,
            width=720,
        )

        self.bar_graph_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))

        self.bar_graph_frame.pack_propagate(False)

        self.bar_chart = AnimatedBarChart(
            self.bar_graph_frame,
            title="Patient Risk History",
            lines_config=[
                {"key": "safe", "label": "Safe", "color": BLUE},
                {"key": "mild", "label": "Mild", "color": VIOLET},
                {"key": "moderate", "label": "Moderate", "color": YELLOW},
                {"key": "severe", "label": "Severe", "color": RED},
            ],
        )

        self.bar_chart.pack(fill="both", expand=True, padx=10, pady=10)

    def build_home_cards(self):
        START_Y = 240
        WIDTH = 475
        HEIGHT = 150

        for i, item in enumerate(self.home_cards_data):
            x_position = self.home_card_positions[i]

            card = ctk.CTkFrame(
                self,
                width=WIDTH,
                height=HEIGHT,
                fg_color="#E2E8F0",
                corner_radius=20,
            )
            card.place(x=x_position, y=START_Y)

            # ICON + COLOR (same logic)
            icon = self.icons[i] if i < len(self.icons) else self.test_icon
            color = self.colors[i] if i < len(self.colors) else PRIMARY

            Avatar(
                card,
                width=80,
                height=80,
                image=icon,
                fg_color=color,
            ).place(x=360, y=30)

            # TITLE
            ctk.CTkLabel(
                card,
                text=item["title"],
                font=("Inter", 20),
                text_color=TEXT_SECONDARY,
            ).place(x=40, y=20)

            # VALUE
            ctk.CTkLabel(
                card,
                text=item["value"],
                font=("Poppins", 53),
                text_color=TEXT_PRIMARY,
            ).place(x=40, y=50)

    def on_show(self):
        # user = self.controller.current_user

        # if not user:
        #     return

        # user_name = user[1]
        # self.welcome_label.configure(text=f"Welcome, {user_name}!")

        stats = self.admin_db.fetch_admin_stats()

        if not stats:
            stats = {
                "total_users": 0,
                "total_test": 0,
                "severe_cases": 0,
                "last_activity": "No activity",
            }

        self.home_cards_data = [
            {"title": "Total Users", "value": stats["total_users"]},
            {"title": "Total Test Conducted", "value": stats["total_test"]},
            {"title": "Severe Risk Cases", "value": stats["severe_cases"]},
        ]

        self.last_activity_label.configure(text=stats["last_activity"])

        self.build_home_cards()

        line_chart_data = self.admin_db.fetch_weekly_users()

        if not line_chart_data:
            line_chart_data = [
                {"day": "Mon", "users": 0},
                {"day": "Tue", "users": 0},
                {"day": "Wed", "users": 0},
                {"day": "Thu", "users": 0},
                {"day": "Fri", "users": 0},
                {"day": "Sat", "users": 0},
                {"day": "Sun", "users": 0},
            ]

        self.after(500, lambda: self.line_chart.update_chart(line_chart_data))

        bar_chart_data = self.admin_db.fetch_risk_level()

        if not bar_chart_data:
            bar_chart_data = [
                {"classification": "Safe", "value": 0},
                {"classification": "Mild", "value": 0},
                {"classification": "Moderate", "value": 0},
                {"classification": "Severe", "value": 0},
            ]

        self.after(500, lambda: self.bar_chart.update_chart(bar_chart_data))
