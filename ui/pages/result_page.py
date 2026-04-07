import customtkinter as ctk
from PIL import Image
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    EYE,
    TEMP,
    CHECK_TEST,
    RISK,
    PRIMARY,
    GREEN,
    VIOLET,
    YELLOW,
    RED,
    BLUE,
    RECEIPT,
    PINK,
    PLUS,
    PRINTER,
)
from datetime import datetime
from ..components.avatar import Avatar
from ..components.animated_horizontal_bar_chart import AnimatedHorizontalBarChart
from receipts.automate_receipt import AutomateReceipt
from receipts.thermal_receipt import ThermalPrinter


class ResultsPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color="#F8FAFC",
            border_width=2,
            border_color="#E2E8F0",
            corner_radius=15,
        )
        self.controller = controller

        # ICONS
        self.temp_icon = ctk.CTkImage(Image.open(TEMP), size=(35, 35))
        self.test_icon = ctk.CTkImage(Image.open(CHECK_TEST), size=(35, 35))
        self.eye_icon = ctk.CTkImage(Image.open(EYE), size=(35, 35))
        self.risk_icon = ctk.CTkImage(Image.open(RISK), size=(35, 35))
        self.recommendation_icon = ctk.CTkImage(Image.open(CHECK_TEST), size=(24, 24))
        self.receipt_icon = ctk.CTkImage(Image.open(RECEIPT), size=(24, 24))
        self.plus_icon = ctk.CTkImage(Image.open(PLUS), size=(30, 30))
        self.printer_icon = ctk.CTkImage(Image.open(PRINTER), size=(26, 26))

        self.icons = [
            self.temp_icon,
            self.test_icon,
            self.eye_icon,
            self.risk_icon,
        ]

        self.avatar_colors = [RED, VIOLET, PINK, BLUE]

        ctk.CTkLabel(
            self,
            text="Pre-Diagnostic Results",
            font=("Inter", 35),
            text_color=TEXT_PRIMARY,
        ).place(x=40, y=40)
        ctk.CTkLabel(
            self,
            text="Overview of your screening results and health insights",
            font=("Poppins", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=40, y=90)

        self.results_data = [
            {
                "title": "Temperature",
                "value": "36.2 °C",
                "status": "NORMAL",
            },
            {
                "title": "Test Result",
                "value": "99%",
                "status": "SAFE",
            },
            {
                "title": "Eye Scan",
                "value": "80%",
                "status": "MILD",
            },
            {
                "title": "Risk Level",
                "value": "MILD",
                "status": None,
            },
        ]

        self.card_positions = [40, 290, 540, 790]
        self.build_result_cards()

        self.graphs_container = ctk.CTkFrame(self, fg_color="transparent")
        self.graphs_container.place(x=40, y=310)

        self.bar_container = ctk.CTkFrame(
            self.graphs_container,
            width=985,
            height=410,
            fg_color="#F8FAFC",
            border_width=2,
            border_color="#E2E8F0",
            corner_radius=20,
        )

        self.bar_container.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10),
        )
        self.bar_container.pack_propagate(False)

        # self.patient_chart = AnimatedHorizontalBarChart(
        #     self.bar_container,
        #     title="Top Contributing Factors",
        #     lines_config=[
        #         {"label": "temperature", "color": RED},
        #         {"label": "calf_pain", "color": VIOLET},
        #         {"label": "wounds", "color": YELLOW},
        #         {"label": "environment", "color": PINK},
        #         {"label": "headache_freq", "color": BLUE},
        #     ],
        # )

        # self.patient_chart.pack(fill="both", expand=True, padx=10, pady=10)
        # data = [
        #     {"score": 13.27, "feature": "temperature"},
        #     {"score": 2, "feature": "calf_pain"},
        #     {"score": 0.09, "feature": "wounds"},
        #     {"score": 0.4, "feature": "environment"},
        #     {"score": 50, "feature": "headache_freq"},
        # ]

        # self.patient_chart.update_chart(data)

        self.recommendation_container = ctk.CTkFrame(
            self,
            width=980,
            height=160,
            fg_color="#F8FAFC",
            border_width=2,
            border_color="#E2E8F0",
            corner_radius=20,
        )

        self.recommendation_container.place(x=40, y=740)
        Avatar(
            self.recommendation_container,
            image=self.recommendation_icon,
            width=50,
            height=50,
            fg_color=GREEN,
        ).place(x=20, y=20)

        ctk.CTkLabel(
            self.recommendation_container,
            text="Recommendation",
            text_color=TEXT_PRIMARY,
            font=("Inter", 20),
        ).place(x=80, y=30)

        Avatar(
            self.recommendation_container,
            # image=self.check_icon,
            image="",
            width=15,
            height=15,
            fg_color=GREEN,
        ).place(x=55, y=90)

        self.recommendation_label = ctk.CTkLabel(
            self.recommendation_container,
            text_color="#0F172A",
            wraplength=880,
            font=("Poppins", 17.5),
            text="",
            anchor="w",
            justify="left",
        )

        self.recommendation_label.place(x=80, y=85)

        self.receipt_container = ctk.CTkFrame(
            self,
            width=405,
            height=550,
            fg_color="#F8FAFC",
            border_width=2,
            border_color="#E2E8F0",
            corner_radius=20,
        )

        self.receipt_container.place(x=1045, y=140)

        Avatar(
            self.receipt_container,
            image=self.receipt_icon,
            width=50,
            height=50,
            fg_color=GREEN,
        ).place(x=20, y=20)

        ctk.CTkLabel(
            self.receipt_container,
            text="Receipt Preview",
            text_color=TEXT_PRIMARY,
            font=("Inter", 20),
        ).place(x=80, y=30)

        self.pdf_preview = ctk.CTkFrame(
            self.receipt_container,
            width=380,
            height=445,
            fg_color="transparent",
        )
        self.pdf_preview.place(x=10, y=85)
        self.reciept_preview()

        self.actions_container = ctk.CTkFrame(
            self,
            width=405,
            height=190,
            fg_color="#F8FAFC",
            border_width=2,
            border_color="#E2E8F0",
            corner_radius=20,
        )

        self.actions_container.place(x=1045, y=710)
        ctk.CTkButton(
            self.actions_container,
            text="Print",
            fg_color=VIOLET,
            text_color="#FFFFFF",
            width=360,
            height=60,
            font=("Inter", 20, "bold"),
            image=self.printer_icon,
            compound="left",
        ).place(x=23, y=25)

        ctk.CTkButton(
            self.actions_container,
            text="Test Again",
            fg_color=GREEN,
            text_color="#FFFFFF",
            width=360,
            height=60,
            font=("Inter", 20, "bold"),
            image=self.plus_icon,
            compound="left",
        ).place(x=23, y=100)

    def build_receipt_filename(self, patient_id, question_id):
        import os

        os.makedirs("assets/pdf", exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"assets/pdf/receipt_{patient_id}_{question_id}_{ts}.pdf"

    def reciept_preview(self):
        try:
            import fitz
            from PIL import Image
            import os

            # # ✔ Correct path
            # base_dir = os.path.dirname(os.path.abspath(__file__))
            # pdf_path = os.path.join(base_dir, "..", "..", "assets", "pdfs", "test.pdf")
            # pdf_path = os.path.abspath(pdf_path)

            pdf_path = getattr(self, "latest_receipt_path", None)

            if not pdf_path or not os.path.exists(pdf_path):
                return

            # CLEAR OLD CONTENT (IMPORTANT)
            for widget in self.pdf_preview.winfo_children():
                widget.destroy()

            # SCROLLABLE FRAME
            scroll = ctk.CTkScrollableFrame(
                self.pdf_preview,
                fg_color="transparent",
                corner_radius=0,
                scrollbar_button_color="#CBD5E1",
                scrollbar_button_hover_color="#94A3B8",
                # fg_color="red",
                width=365,
                height=440,
            )
            scroll.pack(fill="both", expand=True)

            # OPEN PDF
            doc = fitz.open(pdf_path)

            for i in range(len(doc)):
                page = doc.load_page(i)

                mat = fitz.Matrix(2, 2)
                pix = page.get_pixmap(matrix=mat)

                img = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples,
                )

                img.thumbnail((340, 2000))  # fit container nicely

                ctk_img = ctk.CTkImage(light_image=img, size=img.size)

                lbl = ctk.CTkLabel(scroll, image=ctk_img, text="")
                lbl.pack(pady=10)

                lbl.image = ctk_img  # prevent garbage collection

            doc.close()

        except Exception as e:
            print("PDF Preview Error:", e)  # 🔥 DON'T USE PASS

    def generate_receipt(self):
        qid = self.controller.current_question_id
        data = self.controller.db.get_receipt_data(qid)

        if not data:
            return

        self.current_patient_id = data["patient_id"]
        # CHECK IF PDF ALREADY EXISTS
        if data.get("pdf_path") and os.path.exists(data["pdf_path"]):
            self.latest_receipt_path = data["pdf_path"]
            return

        filename = self.build_receipt_filename(data["patient_id"], data["result_id"])

        receipt = AutomateReceipt(
            filename=filename,
            patient_id=data["patient_id"],
            patient_name=data["patient_name"],
            contact_number=data["contact_number"],
            temperature=data["temperature"],
            test_risk_level=data["test_risk_level"],
            test_confidence=data["test_confidence"],
            eye_classification=data["eye_classification"],
            risk_level=data["risk_level"],
            recommendation=data["recommendation"],
            result_id=str(data["patient_id"]),
        )

        receipt.build()

        self.controller.db.save_pdf_path(
            self.controller.current_question_id,
            filename,
        )

        self.latest_receipt_path = filename

        #  PREPARE DATA FOR THERMAL PRINT
        thermal_data = {
            "patient_id": data.get("patient_id", "UNKNOWN"),
            "patient_name": data.get("patient_name", "UNKNOWN"),
            "temperature": data.get("temperature", 0),
            "contact_number": data.get("contact_number", "N/A"),
            "test_risk_level": data.get("test_risk_level") or "Pending",
            "test_conf": data.get("test_confidence") or 0,
            "eye_classification": data.get("eye_classification") or "Unknown",
            "eye_conf": data.get("eye_confidence") or 0,
            "risk_level": data.get("risk_level") or "UNDETERMINED",
            "recommendation": data.get("recommendation")
            or "No recommendation available. Please consult a medical professional for further evaluation.",
        }

        try:
            thermal_printer = ThermalPrinter(port="COM3", baudrate=115200)
            thermal_printer.print_report(**thermal_data)
            thermal_printer.close()
        except Exception as e:
            print("Thermal print error:", e)

    def build_result_cards(self):
        START_Y = 140
        WIDTH = 235
        HEIGHT = 150

        for i, item in enumerate(self.results_data):
            x_position = self.card_positions[i]

            card = ctk.CTkFrame(
                self,
                width=WIDTH,
                height=HEIGHT,
                fg_color="#F8FAFC",
                border_width=2,
                border_color="#E2E8F0",
                corner_radius=20,
            )
            card.place(x=x_position, y=START_Y)

            # ICON + COLOR FROM ARRAYS
            icon = self.icons[i] if i < len(self.icons) else self.temp_icon
            color = self.avatar_colors[i] if i < len(self.avatar_colors) else PRIMARY

            Avatar(
                card,
                width=60,
                height=60,
                image=icon,
                fg_color=color,
            ).place(x=20, y=20)

            # TITLE
            ctk.CTkLabel(
                card,
                text=item["title"],
                font=("Inter", 17),
                text_color=TEXT_SECONDARY,
            ).place(x=90, y=25)

            # VALUE
            ctk.CTkLabel(
                card,
                text=item["value"],
                font=("Poppins", 35),
                text_color=TEXT_PRIMARY,
            ).place(x=90, y=55)

            # STATUS
            ctk.CTkLabel(
                card,
                text=item["status"],
                font=("Inter", 15, "bold"),
                text_color=color,  # 🔥 matches icon color
            ).place(x=90, y=100)

    # def load_results(self):
    # # Populate this
    # self.results_data = [
    #     {
    #         "title": "Temperature",
    #         "value": "36.2 °C",
    #         "status": "NORMAL",
    #     },
    #     {
    #         "title": "Test Result",
    #         "value": "99%",
    #         "status": "SAFE",
    #     },
    #     {
    #         "title": "Eye Scan",
    #         "value": "80%",
    #         "status": "MILD",
    #     },
    #     {
    #         "title": "Risk Level",
    #         "value": "MILD",  # value to uppercase this
    #         "status": None,
    #     },
    # ]

    # qid = self.controller.current_question_id

    # if not qid:
    #     return

    # result = self.controller.db.get_diagnosis_results(qid)

    #         self.patient_chart = AnimatedHorizontalBarChart(
    #     self.bar_container,
    #     title="Top Contributing Factors",
    #     lines_config=[
    #         {"label": "temperature", "color": RED},
    #         {"label": "calf_pain", "color": VIOLET},
    #         {"label": "wounds", "color": YELLOW},
    #         {"label": "environment", "color": PINK},
    #         {"label": "headache_freq", "color": BLUE},
    #     ],
    # )

    # self.patient_chart.pack(fill="both", expand=True, padx=10, pady=10)
    # data = [
    #     {"score": 13.27, "feature": "temperature"},
    #     {"score": 2, "feature": "calf_pain"},
    #     {"score": 0.09, "feature": "wounds"},
    #     {"score": 0.4, "feature": "environment"},
    #     {"score": 50, "feature": "headache_freq"},
    # ]

    # self.patient_chart.update_chart(data)

    def load_results(self):
        qid = self.controller.current_question_id

        if not qid:
            return

        result = self.controller.db.get_diagnosis_results(qid)

        if not result:
            return

        # ✅ Extract values safely
        temperature = result["temperature"]
        test_class = result["test_classification"]
        test_conf = result["test_confidence"]
        eye_class = result["eye_classification"]
        eye_conf = result["eye_confidence"]
        risk = result["risk_level"]
        recommendation = result["recommendation"]

        # ✅ Safe formatting
        test_class = test_class.upper() if test_class else "UNKNOWN"
        eye_class = eye_class.upper() if eye_class else "UNKNOWN"
        risk_upper = risk.upper() if risk else "UNKNOWN"

        # test_conf = round(test_conf, 2) if test_conf else 0
        eye_conf = round(eye_conf, 2) if eye_conf else 0

        # 🔥 Use your temp function
        temp_status = self.get_temp_status(temperature)

        # ✅ Build cards
        self.results_data = [
            {
                "title": "Temperature",
                "value": f"{temperature} °C",
                "status": temp_status,
            },
            {
                "title": "Test Result",
                "value": f"{test_conf}%",
                "status": test_class,
            },
            {
                "title": "Eye Scan",
                "value": f"{eye_conf}%",
                "status": eye_class,
            },
            {
                "title": "Risk Level",
                "value": risk_upper,
                "status": None,
            },
        ]

        #     self.patient_chart = AnimatedHorizontalBarChart(
        #     self.bar_container,
        #     title="Top Contributing Factors",
        #     lines_config=[
        #         {"label": "temperature", "color": RED},
        #         {"label": "calf_pain", "color": VIOLET},
        #         {"label": "wounds", "color": YELLOW},
        #         {"label": "environment", "color": PINK},
        #         {"label": "headache_freq", "color": BLUE},
        #     ],
        # )

        # self.patient_chart.pack(fill="both", expand=True, padx=10, pady=10)
        # data = [
        #     {"score": 13.27, "feature": "temperature"},
        #     {"score": 2, "feature": "calf_pain"},
        #     {"score": 0.09, "feature": "wounds"},
        #     {"score": 0.4, "feature": "environment"},
        #     {"score": 50, "feature": "headache_freq"},
        # ]

        # self.patient_chart.update_chart(data)
        # ✅ Recommendation (safe)
        self.recommendation_label.configure(
            text=recommendation if recommendation else "No recommendation available."
        )

    def on_show(self):
        self.load_results()
        self.generate_receipt()
        self.controller.current_question_id = None
