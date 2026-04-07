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
from ..components.messagebox import MessageBox as mb
from models.test_classification_model import TestClassificationModel


class QuestionsPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(
            master,
            # fg_color="transparent",
            fg_color="#F8FAFC",
            border_width=2,
            border_color="#E2E8F0",
            corner_radius=15,
        )
        self.controller = controller
        self.db = controller.db
        self.test_model = TestClassificationModel()

        # ICONS
        self.question_icon = ctk.CTkImage(Image.open(QUESTIONS), size=(50, 50))
        self.prev_icon = ctk.CTkImage(Image.open(CHEVRON_LEFT), size=(40, 40))
        self.next_icon = ctk.CTkImage(Image.open(CHEVRON_RIGHT), size=(40, 40))

        # QUESTION ENGINE STATE
        self.questions = questionaires
        self.curr_page_index = 0
        self.answers = {}
        self.is_translated = False
        self.answer_var = ctk.StringVar()

        ctk.CTkLabel(self, text="QUESTIONS").pack(expand=True)

        self.pagination_label = ctk.CTkLabel(
            self,
            text="Questions 1 of 20",
            font=("Inter", 20),
            text_color=TEXT_SECONDARY,
        )
        self.pagination_label.place(x=40, y=40)

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
        self.progress_bar.place(x=40, y=80)

        self.percent_label = ctk.CTkLabel(
            self,
            text="0% Complete",
            font=("Poppins", 18),
            text_color=TEXT_SECONDARY,
        )
        self.percent_label.place(x=1200, y=40)

        self.questions_container = ctk.CTkFrame(
            self,
            fg_color="#F8FAFC",
            border_width=2,
            border_color="#E2E8F0",
            corner_radius=20,
            width=1300,
            height=670,
        )
        self.questions_container.place(x=30, y=120)

        Avatar(
            self.questions_container,
            width=90,
            height=90,
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
            dropdown_hover_color="#E2E8F0",
            dropdown_font=("Inter", 19),
            corner_radius=9,
            command=self.toggle_translate,
        )
        self.translate_option.place(x=1060, y=30)

        self.question_label = ctk.CTkLabel(
            self.questions_container,
            text="",
            font=("Inter", 28),
            text_color=TEXT_PRIMARY,
            wraplength=1200,
            justify="left",
        )
        self.question_label.place(x=90, y=145)

        self.options_container = ctk.CTkFrame(
            self.questions_container, width=1050, height=400, fg_color="transparent"
        )
        self.options_container.place(x=90, y=200)

        self.prev_btn = ctk.CTkButton(
            self,
            text="Previous",
            width=250,
            state=ctk.DISABLED,
            height=75,
            text_color="#FFFFFF",
            font=("Inter", 25, "bold"),
            image=self.prev_icon,
            compound="left",
            corner_radius=10,
            command=lambda: self.change_page("Prev"),
        )
        self.prev_btn.place(x=60, y=815)

        self.next_btn = ctk.CTkButton(
            self,
            text="Next",
            width=250,
            state=ctk.DISABLED,
            height=75,
            text_color="#FFFFFF",
            font=("Inter", 25, "bold"),
            image=self.next_icon,
            compound="right",
            corner_radius=10,
            command=lambda: self.change_page("Next"),
        )
        self.next_btn.place(x=1045, y=815)

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
        self.question_label.configure(text=question, font=("Inter", 26))

        self.pagination_label.configure(
            text=f"Questions {self.curr_page_index + 1} of {len(self.questions)}"
        )

        self.answer_var = ctk.StringVar(
            value=self.answers.get(self.curr_page_index, "")
        )

        for idx, choice in enumerate(choices):
            card = ctk.CTkFrame(
                self.options_container,
                fg_color="#F8FAFC",
                corner_radius=12,
                height=90,
                border_width=2,
                border_color="#E2E8F0",
                width=1050,
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
                text_color="#1E293B",
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
            card.configure(fg_color="#F8FAFC", border_color="#E2E8F0")

        selected_card.configure(
            fg_color="#EFF6FF",
            border_color=PRIMARY,
            border_width=3,
        )

        self.save_answer()

    # SAVE ANSWER
    def save_answer(self):
        self.answers[self.curr_page_index] = self.answer_var.get()
        self.next_btn.configure(state=ctk.NORMAL)

    def normalize_answer(self):
        results = []

        for q_index, choice_index in self.answers.items():
            seeds = self.questions[q_index]
            original_choice = seeds["choices"][int(choice_index)]
            results.append(original_choice)
        return results

    def toggle_translate(self, choice):
        self.is_translated = choice == "Filipino"

        if self.is_translated:
            self.question_label.configure(font=("Arial", 25, "italic"))
        else:
            self.question_label.configure(font=("Arial", 25))

        self.question_builder()

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

    # NAVIGATION
    def change_page(self, button):
        if button == "Next":
            # if self.curr_page_index == len(self.questions) - 1:
            #     answers = self.normalize_answer()
            #     # print(answers)
            #     patient_inputs = self.feed_inputs(temperature=38.5)
            #     print("MODEL INPUT:", patient_inputs)

            #     # MODEL PREDICTION
            #     result = self.test_model.predict(patient_inputs)
            #     print("MODEL RESULT:", result)

            #     patient_id = self.controller.current_user[0]
            #     temp = 38.5

            #     test_confidence = result["confidence"]
            #     test_classification = result["classification"]
            #     top_patient_factors = result["top_patient_factors"]

            #     question_id = self.db.save_question_responses(
            #         patient_id,
            #         temp,
            #         answers,
            #         test_classification,
            #         test_confidence,
            #         top_patient_factors,
            #     )

            #     if question_id:
            #         self.controller.current_question_id = question_id
            #         # mb.showinfo("Saved", "Responses saved successfully")
            #         mb(
            #             title="Saved Answers",
            #             message="Responses saved successfully",
            #             options=("Thanks",),
            #             icon="check",
            #         ).show()
            #         self.controller.change_window("EyeScanPage")
            #     else:

            #         # mb.showerror("Error", "Failed to save responses")
            #         mb(
            #             title="Error",
            #             message="Failed to save responses",
            #             options=("Okay",),
            #             icon="cancel",
            #         ).show()

            #     return
            if self.curr_page_index == len(self.questions) - 1:
                answers = self.normalize_answer()

                patient_inputs = self.feed_inputs()
                print("MODEL INPUT:", patient_inputs)

                # MODEL
                result = self.test_model.predict(patient_inputs)
                print("MODEL RESULT:", result)

                question_id = self.controller.current_question_id

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
                    ).show()

                    self.controller.change_window("EyeScanPage")
                else:
                    mb(
                        title="Error",
                        message="Failed to save responses",
                        options=("Okay",),
                        icon="cancel",
                    ).show()

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

    def on_show(self):
        question_id = self.controller.current_question_id
        temp = self.db.load_temperature(question_id)
        print(f"Temp: {temp}")
