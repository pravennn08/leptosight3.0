import time
from datetime import datetime


class ThermalPrinter:
    def __init__(self, device="/dev/usb/lp0", max_chars=32):
        # Open printer as file instead of serial
        self.printer = open(device, "wb")
        self.max_chars = max_chars

        # ESC/POS Commands
        self.CENTER = b"\x1b\x61\x01"
        self.LEFT = b"\x1b\x61\x00"
        self.BOLD_ON = b"\x1b\x45\x01"
        self.BOLD_OFF = b"\x1b\x45\x00"
        self.CUT = b"\x1d\x56\x00"

    # BASIC WRITE
    def write(self, text):
        self.printer.write(text.encode("utf-8"))

    def write_raw(self, data):
        self.printer.write(data)

    # STYLES
    def center(self):
        self.write_raw(self.CENTER)

    def left(self):
        self.write_raw(self.LEFT)

    def bold_on(self):
        self.write_raw(self.BOLD_ON)

    def bold_off(self):
        self.write_raw(self.BOLD_OFF)

    def line(self):
        self.write("-" * self.max_chars + "\n")

    #  SECTION HEADER
    def section(self, title):
        self.center()
        self.bold_on()
        self.write("-" * self.max_chars + "\n")
        self.write(title.upper() + "\n")
        self.write("-" * self.max_chars + "\n")
        self.bold_off()

    #  KEY VALUE ALIGN
    def kv(self, key, value):
        key = f"{key}:"
        spacing = 16 - len(key)
        if spacing < 1:
            spacing = 1
        line = key + (" " * spacing) + str(value)
        self.write(line + "\n")

    #  DATE TIME
    def print_datetime_line(self):
        now = datetime.now()

        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%I:%M %p")

        left = f"Date: {date_str}"
        right = f"Time: {time_str}"

        spaces = self.max_chars - len(left) - len(right)
        if spaces < 2:
            spaces = 2

        line = left + (" " * spaces) + right
        self.write(line + "\n")

    #  WRAP TEXT
    def wrapped_text(self, text):
        words = text.split(" ")
        line = ""

        for word in words:
            if len(line) + len(word) + 1 > self.max_chars:
                if len(word) > self.max_chars:
                    while len(word) > 0:
                        space_left = self.max_chars - len(line)

                        if space_left <= 1:
                            self.write(line + "\n")
                            line = ""
                            space_left = self.max_chars

                        chunk = word[: space_left - 1]
                        word = word[space_left - 1 :]

                        self.write(line + chunk + "-\n")
                        line = ""
                else:
                    self.write(line + "\n")
                    line = word
            else:
                if line == "":
                    line = word
                else:
                    line += " " + word

        if line:
            self.write(line + "\n")

    #  MAIN REPORT
    def print_report(
        self,
        patient_id,
        patient_name,
        temperature,
        contact_number,
        test_result,
        test_conf,
        eye_classification,
        eye_conf,
        risk_level,
        recommendation,
    ):
        # HEADER
        self.center()
        self.bold_on()
        self.write("\nLEPTOSIGHT DIAGNOSTIC REPORT\n")
        self.bold_off()

        self.print_datetime_line()

        # PATIENT INFO
        self.section("Patient Information")
        self.left()
        self.kv("Patient ID", patient_id)
        self.kv("Patient Name", patient_name)
        self.kv("Contact No", contact_number)

        # TEST RESULTS
        self.section("Test Results")
        self.kv("Temperature", f"{temperature:.1f} C")
        self.kv("Test Result", test_result)
        self.kv("Test Confidence", f"{test_conf}%")
        self.kv("Eye Classification", eye_classification)
        self.kv("Eye Confidence", f"{eye_conf}%")

        # FINAL ASSESSMENT
        self.section("Final Assessment")
        self.bold_on()
        self.write(f"RISK LEVEL: {risk_level}\n")
        self.bold_off()

        self.write("\nRecommendation:\n")
        self.wrapped_text(recommendation)

        # DISCLAIMER
        self.section("Disclaimer")
        self.wrapped_text("AI-assisted screening only.")
        self.wrapped_text("Not a medical diagnosis.")
        self.wrapped_text("Consult a licensed physician.")

        self.write("\n\n")

        # CUT PAPER
        self.write_raw(self.CUT)

    #  CLOSE
    def close(self):
        self.printer.close()


# #  SAMPLE USAGE
# if __name__ == "__main__":
#     printer = ThermalPrinter(device="/dev/usb/lp0")

#     data = {
#         "patient_id": "P-001",
#         "patient_name": "Jade Lucas",
#         "temperature": 36.2,
#         "contact_number": "09123456789",
#         "test_result": "Safe",
#         "test_conf": 92,
#         "eye_classification": "Safe",
#         "eye_conf": 85,
#         "risk_level": "SAFE",
#         "recommendation": "Recommend practicing preventive measures, avoiding floodwater exposure, and maintaining good hygiene.",
#     }

#     printer.print_report(**data)
#     printer.close()
