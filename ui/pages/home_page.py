import customtkinter as ctk
from PIL import Image
from ..components.avatar import Avatar
from ..components.animated_line_chart import AnimatedLineChart
from ..components.animated_bar_chart import AnimatedBarChart
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
    BLUE,
    PINK,
    YELLOW,
    RED,
)


class HomePage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color="transparent",
        )
        self.controller = controller
        self.db = controller.db

        # ICONS
        self.bell_icon = ctk.CTkImage(Image.open(BELL), size=(30, 30))
        self.plus_icon = ctk.CTkImage(Image.open(PLUS), size=(26, 26))
        self.track_icon = ctk.CTkImage(Image.open(TRACK_ACTIVITY), size=(30, 30))
        self.test_icon = ctk.CTkImage(Image.open(CHECK_TEST), size=(45, 45))
        self.report_icon = ctk.CTkImage(Image.open(RECEIPT), size=(45, 45))
        self.calendar_icon = ctk.CTkImage(Image.open(CALENDAR), size=(45, 45))

        self.welcome_frame = ctk.CTkFrame(
            self,
            height=170,
            width=1050,
            fg_color="#E2E8F0",
            corner_radius=20,
        )
        self.welcome_frame.place(x=0, y=0)

        self.icons = [self.test_icon, self.report_icon, self.calendar_icon]
        self.colors = [BLUE, VIOLET, PINK]

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
            text="Early leptospirosis detection through AI eye analysis and structured questionnaires",
            font=("Poppins", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=110, y=70)

        ctk.CTkButton(
            self.welcome_frame,
            text="Start Test",
            font=("Arial", 21, "bold"),
            image=self.plus_icon,
            compound="left",
            height=50,
            width=250,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            text_color="#FFFFFF",
            corner_radius=9,
            command=lambda: self.controller.change_window("StartTestPage"),
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
            fg_color=RED,
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
        self.line_chart = AnimatedLineChart(
            self.line_inner,
            title="Historic Progress",
            lines_config=[
                {"key": "test", "label": "Test Confidence", "color": PINK},
                {"key": "eye", "label": "Eye Scan Confidence", "color": VIOLET},
                {"key": "temp", "label": "Body Temp", "color": YELLOW},
            ],
        )
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
            title="Risk History",
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
        user = self.controller.current_user
        # user = [None, None]

        if not user:
            return

        user_id = user[0]
        user_name = user[1]
        self.welcome_label.configure(text=f"Welcome, {user_name}!")

        stats = self.db.fetch_patient_diagnosis_stats(user_id)

        if not stats:
            stats = {
                "total_tests": 0,
                "total_reports": 0,
                "last_test_date": "N/A",
                "last_activity": "No activity",
            }

        self.home_cards_data = [
            {"title": "Total Test Taken", "value": stats["total_tests"]},
            {"title": "Reports Generated", "value": stats["total_reports"]},
            {"title": "Last Test Date", "value": stats["last_test_date"]},
        ]

        self.build_home_cards()

        self.last_activity_label.configure(text=stats["last_activity"])

        line_chart_data = self.db.get_line_chart_data(user_id)
        if not line_chart_data:
            line_chart_data = [
                {
                    "session": "Session 1",
                    "temp": 0.00,
                    "test": 0.00,
                    "eye": 0.00,
                }
            ]
        self.after(500, lambda: self.line_chart.update_chart(line_chart_data))

        bar_chart_data = self.db.get_bar_chart_data(user_id)

        if not bar_chart_data:
            bar_chart_data = {
                "Safe": 0,
                "Mild": 0,
                "Moderate": 0,
                "Severe": 0,
            }

        self.after(500, lambda: self.bar_chart.update_chart(bar_chart_data))
