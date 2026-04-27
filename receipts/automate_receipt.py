from reportlab.platypus import SimpleDocTemplate, Preformatted, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import mm
from reportlab.lib.enums import TA_CENTER


class AutomateReceipt:
    def __init__(
        self,
        filename="receipt.pdf",
        date="",
        time="",
        patient_id="",
        patient_name="",
        contact_number="",
        temperature=0,
        test_classification="",
        test_confidence="",
        eye_classification="",
        eye_confidence="",
        risk_level="",
        recommendation="",
    ):
        self.filename = filename

        #  DATA
        self.date = date
        self.time = time
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.contact_number = contact_number
        self.temperature = temperature
        self.test_classification = test_classification
        self.test_confidence = test_confidence
        self.eye_classification = eye_classification
        self.eye_confidence = eye_confidence
        self.risk_level = risk_level
        self.recommendation = recommendation

        #  PDF SETUP
        self.doc = SimpleDocTemplate(
            self.filename,
            pagesize=(58 * mm, 200 * mm),
            leftMargin=5,
            rightMargin=5,
            topMargin=5,
            bottomMargin=5,
        )

        self.style = ParagraphStyle(
            name="receipt",
            fontName="Courier",
            fontSize=8,
            leading=11,
            alignment=TA_CENTER,
        )

        self.bold_style = ParagraphStyle(
            name="bold",
            fontName="Courier-Bold",
            fontSize=8,
            leading=11,
            alignment=TA_CENTER,
        )

        self.max_chars = 30
        self.line = "-" * self.max_chars
        self.story = []

    #  HELPERS
    def center(self, text):
        return text.center(self.max_chars)

    def kv_center(self, key, value):
        return self.kv_line(key, value).center(self.max_chars)

    def kv_line(self, key, value):
        key = f"{key}:"
        spacing = 17 - len(key)
        spacing = max(1, spacing)

        # 🔥 DO NOT CENTER (this preserves layout)
        return key + (" " * spacing) + str(value)

    def wrap_center(self, text):
        words = text.split()
        lines = []
        line = ""

        for word in words:
            if len(line) + len(word) + 1 > self.max_chars:
                lines.append(line.center(self.max_chars))
                line = word
            else:
                line = word if line == "" else line + " " + word

        if line:
            lines.append(line.center(self.max_chars))

        return "\n".join(lines)

    def add(self, text, bold=False):
        style = self.bold_style if bold else self.style
        self.story.append(Preformatted(text, style))

    def spacer(self, h=6):
        self.story.append(Spacer(1, h))

    #  BUILD
    def build(self):
        # HEADER
        self.add(self.center("LEPTOSIGHT DIAGNOSTIC REPORT"), bold=True)

        dt = f"Date: {self.date} Time: {self.time}"
        self.add(self.center(dt))

        self.add(self.line)

        # PATIENT
        self.add(self.center("PATIENT INFORMATION"), bold=True)
        self.add(self.line)

        self.add(self.kv_line("Patient ID", self.patient_id))
        self.add(self.kv_line("Patient Name", self.patient_name))
        self.add(self.kv_line("Contact No", self.contact_number))

        self.add(self.line)

        # TEST RESULTS
        self.add(self.center("TEST RESULTS"), bold=True)
        self.add(self.line)

        self.add(self.kv_center("Temperature", f"{self.temperature:.1f} C"))
        self.add(self.kv_center("Test Result", self.test_classification))
        self.add(self.kv_center("Test Confidence", f"{self.test_confidence}%"))
        self.add(self.kv_center("Eye Class", self.eye_classification))
        self.add(self.kv_center("Eye Confidence", f"{self.eye_confidence}%"))

        self.add(self.line)

        # FINAL
        self.add(self.center("FINAL ASSESSMENT"), bold=True)
        self.add(self.line)

        self.add(self.center(f"RISK LEVEL: {self.risk_level}"), bold=True)

        self.spacer()

        self.add(self.center("Recommendation:"))
        self.add(self.wrap_center(self.recommendation))

        self.add(self.line)

        # DISCLAIMER
        self.add(self.center("DISCLAIMER"), bold=True)
        self.add(self.line)

        # self.add(self.center("AI-assisted screening only."))
        # self.add(self.center("Not a medical diagnosis."))
        # self.add(self.center("Consult a licensed physician."))

        self.add(
            self.center(
                "This result is based on AI-\nassisted screening and is inte-\nnded for preliminary assessment only."
            )
        )
        self.add(self.center("It is not a medical diagnosis."))
        self.add(
            self.center(
                "Please consult a licensed \nphysician for proper evaluation\nand confirmation."
            )
        )

        # BUILD
        self.doc.build(self.story)


# TEST CODE
receipt = AutomateReceipt(
    filename="hehe.pdf",
    date="2026-04-04",
    time="12:09 AM",
    patient_id="P-001",
    patient_name="Juan Dela Cruz",
    contact_number="09123456789",
    temperature=36.2,
    test_classification="Safe",
    test_confidence="92%",
    eye_classification="NORMAL",
    eye_confidence="85%",
    risk_level="LOW",
    recommendation="Recommend practicing preventive measures, avoiding floodwater exposure, and maintaining good hygiene.",
)

receipt.build()
