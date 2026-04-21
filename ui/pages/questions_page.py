import customtkinter as ctk
from PIL import Image
from constants.seeds import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    PRIMARY,
    SECONDARY,
    QUESTIONS,
    CHEVRON_LEFT,
    CHEVRON_RIGHT,
    STRUCTURED_QUESTIONS as questionaires,
)
from ..components.avatar import Avatar
from CTkMessagebox import CTkMessagebox as mb
from models.test_classification_model import TestClassificationModel
import threading


class QuestionsPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            fg_color="transparent",
            # fg_color="#F8FAFC",
            # border_width=2,
            # border_color="#E2E8F0",
            corner_radius=15,
        )
        self.controller = controller
        self.db = controller.db
        self.test_model = TestClassificationModel()

        # ICONS
        self.question_icon = ctk.CTkImage(Image.open(QUESTIONS), size=(40, 40))
        self.prev_icon = ctk.CTkImage(Image.open(CHEVRON_LEFT), size=(40, 40))
        self.next_icon = ctk.CTkImage(Image.open(CHEVRON_RIGHT), size=(40, 40))

        # QUESTION ENGINE STATE
        self.questions = questionaires
        self.curr_page_index = 0
        self.answers = {}
        self.is_translated = False
        self.answer_var = ctk.StringVar()

        ctk.CTkLabel(
            self,
            text="Symptom Assessment Questionnaire",
            font=("Inter", 30, "bold"),
            text_color=TEXT_PRIMARY,
        ).place(x=40, y=10)

        ctk.CTkLabel(
            self,
            text="Please answer all questions honestly based on your current condition.",
            font=("Poppins", 20),
            text_color=TEXT_SECONDARY,
        ).place(x=40, y=50)

        self.pagination_label = ctk.CTkLabel(
            self,
            text="Questions 1 of 20",
            font=("Inter", 18),
            text_color=TEXT_SECONDARY,
        )
        self.pagination_label.place(x=40, y=90)

        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=1290,
            height=15,
            fg_color="#E5E7EB",  # light gray (track)
            progress_color="#14B8A6",  # your primary (fill)
            orientation="horizontal",
            mode="determinate",
        )
        self.progress_bar.set(0)
        self.progress_bar.place(x=40, y=130)

        self.percent_label = ctk.CTkLabel(
            self,
            text="0% Complete",
            font=("Poppins", 18),
            text_color=TEXT_SECONDARY,
        )
        self.percent_label.place(x=1200, y=90)

        self.questions_container = ctk.CTkFrame(
            self,
            # fg_color="#FFFFFF",
            fg_color="#E2E8F0",
            corner_radius=15,
            border_width=2,
            border_color="#E2E8F0",
            width=1300,
            height=640,
        )
        self.questions_container.place(x=40, y=170)

        Avatar(
            self.questions_container,
            width=80,
            height=80,
            image=self.question_icon,
            fg_color=PRIMARY,
        ).place(x=40, y=30)
        self.translate_var = ctk.StringVar(value=("Translate"))
        self.translate_option = ctk.CTkOptionMenu(
            self.questions_container,
            width=200,
            height=50,
            values=("English", "Filipino"),
            variable=self.translate_var,
            font=("Inter", 18),
            # fg_color="#0EA5E9",
            # button_color="#0284C7",
            # button_hover_color="#0369A1",
            fg_color=PRIMARY,
            button_color=SECONDARY,
            text_color="#FFFFFF",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#0F172A",
            dropdown_hover_color="#ECF1F7",
            dropdown_font=("Inter", 20.5),
            corner_radius=9,
            command=self.toggle_translate,
        )
        self.translate_option.place(x=1060, y=30)

        self.question_label = ctk.CTkLabel(
            self.questions_container,
            text="",
            font=("Inter", 25),
            text_color="#1E293B",
            wraplength=1200,
            justify="left",
        )
        self.question_label.place(x=90, y=130)

        self.options_container = ctk.CTkFrame(
            self.questions_container, width=1050, height=400, fg_color="transparent"
        )
        self.options_container.place(x=90, y=180)

        self.prev_btn = ctk.CTkButton(
            self,
            text="Previous",
            width=210,
            state=ctk.DISABLED,
            height=70,
            text_color="#FFFFFF",
            font=("Inter", 23, "bold"),
            image=self.prev_icon,
            compound="left",
            corner_radius=10,
            command=lambda: self.change_page("Prev"),
        )
        self.prev_btn.place(x=45, y=830)

        self.next_btn = ctk.CTkButton(
            self,
            text="Next",
            width=210,
            state=ctk.DISABLED,
            height=70,
            text_color="#FFFFFF",
            font=("Inter", 23, "bold"),
            image=self.next_icon,
            fg_color=PRIMARY,
            hover_color=SECONDARY,
            compound="right",
            corner_radius=10,
            command=lambda: self.change_page("Next"),
        )
        self.next_btn.place(x=1125, y=830)

        self.question_builder()

    # QUESTION BUILDER
    def question_builder(self):

        for widget in self.options_container.winfo_children():
            widget.destroy()

        seeds = self.questions[self.curr_page_index]

        question = (
            seeds["question_translate"] if self.is_translated else seeds["question"]
        )

        choices = seeds["choices_translate"] if self.is_translated else seeds["choices"]
        self.question_label.configure(
            text=question,
        )

        self.pagination_label.configure(
            text=f"Questions {self.curr_page_index + 1} of {len(self.questions)}"
        )

        self.answer_var = ctk.StringVar(
            value=self.answers.get(self.curr_page_index, "")
        )

        for idx, choice in enumerate(choices):
            card = ctk.CTkFrame(
                self.options_container,
                fg_color="#EEF2F7",
                border_color="#CBD5E1",
                corner_radius=12,
                height=90,
                border_width=2,
                width=1120,
            )
            card.pack(fill="x", pady=8)
            card.pack_propagate(False)
            card.bind("<Button-1>", lambda e, i=idx, c=card: self.select_option(i, c))

            rb = ctk.CTkRadioButton(
                card,
                text=f"   {choice}",
                variable=self.answer_var,
                value=str(idx),
                fg_color=PRIMARY,
                font=("Poppins", 22.5),
                text_color=TEXT_SECONDARY,
                width=40,
                command=lambda c=card: self.select_card(c),
            )
            rb.pack(anchor="w", padx=20, pady=25)

        if self.curr_page_index in self.answers:
            self.next_btn.configure(state=ctk.NORMAL)
        else:
            self.next_btn.configure(state=ctk.DISABLED)

    def select_option(self, idx, card):
        self.answer_var.set(str(idx))
        self.select_card(card)

    def select_card(self, selected_card):
        for card in self.options_container.winfo_children():
            card.configure(
                fg_color="#EEF2F7",
                border_color="#CBD5E1",
            )

        selected_card.configure(
            fg_color="#EEF2F7",
            border_color=PRIMARY,
            border_width=3,
        )

        self.save_answer()

    # SAVE ANSWER
    def save_answer(self):
        self.answers[self.curr_page_index] = self.answer_var.get()
        self.next_btn.configure(state=ctk.NORMAL)

    def toggle_translate(self, choice):
        self.is_translated = choice == "Filipino"

        if self.is_translated:
            self.question_label.configure(font=("Poppins", 25, "italic"))
        else:
            self.question_label.configure(font=("Poppins", 25))

        self.question_builder()

    def normalize_answer(self):
        results = []

        for q_index, choice_index in self.answers.items():
            seeds = self.questions[q_index]
            original_choice = seeds["choices"][int(choice_index)]
            results.append(original_choice)
        return results

    def load_patient_temp(self):
        question_id = self.controller.current_question_id
        temp = self.db.load_temperature(question_id)

        if temp is None:
            print("Temperature not found!")
            return 0  # fallback

        return temp

    def feed_inputs(self):
        temperature = self.load_patient_temp()

        inputs = []

        for i in range(len(self.questions)):
            choice_index = int(self.answers.get(i, 0))
            inputs.append(choice_index)

        inputs.append(float(temperature))

        return [inputs]

    def run_prediction(self, patient_inputs, answers, question_id):
        try:
            result = self.test_model.predict(patient_inputs)

            # return to UI thread safely
            self.after(
                0, lambda: self.handle_prediction_result(result, answers, question_id)
            )

        except Exception as e:
            self.after(0, lambda: self.show_error(e))

    def handle_prediction_result(self, result, answers, question_id):
        print("MODEL RESULT:", result)

        test_confidence = result["confidence"]
        test_classification = result["classification"]
        top_patient_factors = result["top_patient_factors"]

        success = self.db.save_question_responses(
            question_id,
            answers,
            test_classification,
            test_confidence,
            top_patient_factors,
        )

        if success:
            mb(
                title="Saved Answers",
                message="Responses saved successfully",
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
            self.controller.change_window("EyeScanPage")
        else:
            self.show_error("Failed to save responses")
        self.next_btn.configure(state=ctk.NORMAL)

    def show_error(self, error):
        mb(
            title="Error",
            message="Failed to save responses",
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

    # NAVIGATION
    def change_page(self, button):

        if button == "Next":
            if self.curr_page_index == len(self.questions) - 1:

                answers = self.normalize_answer()
                patient_inputs = self.feed_inputs()
                question_id = self.controller.current_question_id

                print("MODEL INPUT:", patient_inputs)

                self.next_btn.configure(state=ctk.DISABLED, text="Processing...")

                threading.Thread(
                    target=self.run_prediction,
                    args=(patient_inputs, answers, question_id),
                    daemon=True,
                ).start()

                return

            else:
                self.curr_page_index += 1

        elif button == "Prev":
            self.curr_page_index -= 1

        self.question_builder()
        self.update_buttons()
        self.update_progressbar()
        self.update_percentage()

    def update_buttons(self):
        if self.curr_page_index == 0:
            self.prev_btn.configure(state="disabled")
        else:
            self.prev_btn.configure(state="normal")

        if self.curr_page_index == len(self.questions) - 1:
            self.next_btn.configure(
                text="Submit",
                fg_color=PRIMARY,
                hover_color=SECONDARY,
            )
        else:
            self.next_btn.configure(text="Next")

    def update_progressbar(self):
        total = len(self.questions)
        current = self.curr_page_index + 1
        progress = current / total
        self.progress_bar.set(progress)

    def update_percentage(self):
        total = len(self.questions)
        answered = len(self.answers)

        percentage = int((answered / total) * 100)

        self.percent_label.configure(text=f"{percentage}% Complete")

    def clear_fields(self):
        # 🔥 RESET LOGIC STATE
        self.curr_page_index = 0
        self.answers.clear()
        self.is_translated = False

        # 🔥 RESET VARIABLE (VERY IMPORTANT)
        self.answer_var = ctk.StringVar()

        # 🔥 RESET UI
        self.progress_bar.set(0)
        self.percent_label.configure(text="0% Complete")

        self.prev_btn.configure(state=ctk.DISABLED)
        self.next_btn.configure(state=ctk.DISABLED, text="Next")

        # reset language dropdown
        self.translate_var.set("English")

        # 🔥 CLEAR OPTIONS UI
        for widget in self.options_container.winfo_children():
            widget.destroy()

        # 🔥 LOAD FIRST QUESTION AGAIN
        self.question_builder()

    def on_show(self):
        question_id = self.controller.current_question_id
        temp = self.db.load_temperature(question_id)
        print(f"Temp: {temp}")
