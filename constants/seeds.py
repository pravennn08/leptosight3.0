import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SYSTEM
LOGO = os.path.join(BASE_DIR, "assets", "system", "logo.png")
CAMERA_PROMPT = os.path.join(BASE_DIR, "assets", "system", "camera_prompt.png")
BEEP = os.path.join(BASE_DIR, "assets", "system", "beep.wav")

# ICONS
PHONE = os.path.join(BASE_DIR, "assets", "icons", "phone.png")
ACCOUNT = os.path.join(BASE_DIR, "assets", "icons", "account.png")
HOME = os.path.join(BASE_DIR, "assets", "icons", "home.png")
TEST = os.path.join(BASE_DIR, "assets", "icons", "test.png")
RECORDS = os.path.join(BASE_DIR, "assets", "icons", "records.png")
PROFILE = os.path.join(BASE_DIR, "assets", "icons", "profile.png")
SETTINGS = os.path.join(BASE_DIR, "assets", "icons", "settings.png")
CHEVRON = os.path.join(BASE_DIR, "assets", "icons", "chevron.png")
LOGOUT = os.path.join(BASE_DIR, "assets", "icons", "logout.png")
DASHBOARD = os.path.join(BASE_DIR, "assets", "icons", "dashboard.png")
PATIENT_RECORDS = os.path.join(BASE_DIR, "assets", "icons", "folders.png")
USERS = os.path.join(BASE_DIR, "assets", "icons", "users.png")
NEXT = os.path.join(BASE_DIR, "assets", "icons", "next.png")
BELL = os.path.join(BASE_DIR, "assets", "icons", "bell.png")
PLUS = os.path.join(BASE_DIR, "assets", "icons", "plus.png")
CALENDAR = os.path.join(BASE_DIR, "assets", "icons", "calendar.png")
TRACK_ACTIVITY = os.path.join(BASE_DIR, "assets", "icons", "track.png")
QUESTIONS = os.path.join(BASE_DIR, "assets", "icons", "questions.png")
CHEVRON_RIGHT = os.path.join(BASE_DIR, "assets", "icons", "chevron-right.png")
RETRY = os.path.join(BASE_DIR, "assets", "icons", "retry.png")
CHEVRON_LEFT = os.path.join(BASE_DIR, "assets", "icons", "chevron-left.png")
CAMERA = os.path.join(BASE_DIR, "assets", "icons", "camera.png")
FLASH = os.path.join(BASE_DIR, "assets", "icons", "zap.png")
SAVE = os.path.join(BASE_DIR, "assets", "icons", "save.png")
CHECK = os.path.join(BASE_DIR, "assets", "icons", "check.png")
EYE = os.path.join(BASE_DIR, "assets", "icons", "eye.png")
DISTANCE = os.path.join(BASE_DIR, "assets", "icons", "scan.png")
TEMP = os.path.join(BASE_DIR, "assets", "icons", "temp.png")
RISK = os.path.join(BASE_DIR, "assets", "icons", "risk.png")
CHECK_TEST = os.path.join(BASE_DIR, "assets", "icons", "check-test.png")
RECEIPT = os.path.join(BASE_DIR, "assets", "icons", "receipt.png")
PRINTER = os.path.join(BASE_DIR, "assets", "icons", "printer.png")


# COLOR PALETTE
PRIMARY = "#14B8A6"
SECONDARY = "#0D9488"
BACKGROUND = "#FFFFFF"
SURFACE = "#FFFFFF"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"
TEXT_PRIMARY = "#111827"
TEXT_SECONDARY = "#6B7280"
DIVIDER = "#E5E7EB"
SIDEBAR_ACTIVE = "#E2E8F0"
SIDEBAR_HOVER = "#F1F5F9"

GREEN = "#14B8A6"
VIOLET = "#8B5CF6"
YELLOW = "#F59E0B"
ORANGE = "#f1c40f"
RED = "#EF4444"
PINK = "#EC4899"
BLUE = "#0EA5E9"
BLUE_HOVER = "#0284C7"


# DATA PRIVACY ACT

# GENERAL INSTRUCTIONS
INSTRUCTIONS = [
    {
        "title": "Position Your Camera",
        "sub_title": "Ensure the camera is positioned at eye level",
    },
    {
        "title": "Focus on the Screen",
        "sub_title": "Keep your eyes centered on the screen at all times",
    },
    {
        "title": "Stay Still and Blink Normally",
        "sub_title": "Maintain a steady position for about 15 seconds",
    },
    {
        "title": "Answer Quick Questions",
        "sub_title": "Complete the short questionnaire after scanning",
    },
]

# CAMERA TIPS

CAMERA_TIPS = [
    {
        "title": "Camera at eye level",
        "sub_title": "Keep your head straight",
    },
    {
        "title": "Eyes centered",
        "sub_title": "Look at the center dot",
    },
    {
        "title": "Good lighting",
        "sub_title": "Avoid shadows and glare",
    },
    {
        "title": "Proper distance",
        "sub_title": "Stay 40–60 cm from camera",
    },
]

# QUESTIONAIRES
STRUCTURED_QUESTIONS = [
    {
        "question": "Did any part of your body contact floodwater or muddy water?",
        "choices": [
            "No contact",
            "Feet only",
            "Feet and legs",
            "Large areas of the body",
        ],
        "question_translate": "May bahagi ba ng iyong katawan na nadikit sa baha o maputik na tubig?",
        "choices_translate": [
            "Walang nadikit",
            "Paa lamang",
            "Paa at binti",
            "Malalaking bahagi ng katawan",
        ],
    },
    {
        "question": "During that exposure, did you have any cuts or wounds?",
        "choices": [
            "No",
            "Small healed scratches",
            "Open cuts or wounds",
            "Multiple or untreated wounds",
        ],
        "question_translate": "Sa panahong iyon, mayroon ka bang sugat o hiwa?",
        "choices_translate": [
            "Wala",
            "Maliit na gasgas na magaling na",
            "Bukas na sugat o hiwa",
            "Maramihan o hindi nagamot na sugat",
        ],
    },
    {
        "question": "In the past few weeks, which environment were you most exposed to?",
        "choices": [
            "Mostly indoors",
            "Outdoors but dry areas",
            "Wet or muddy areas",
            "Flooded areas",
        ],
        "question_translate": "Sa nakaraang mga linggo, saan ka pinaka-madalas na nalantad?",
        "choices_translate": [
            "Kadalasang nasa loob ng bahay",
            "Sa labas ngunit tuyong lugar",
            "Basâ o maputik na lugar",
            "Lugar na binaha",
        ],
    },
    {
        "question": "How did your illness begin?",
        "choices": [
            "Suddenly within a day",
            "Gradually over several days",
            "I am not sure",
            "I have not noticed a clear change",
        ],
        "question_translate": "Paano nagsimula ang iyong nararamdaman na sakit?",
        "choices_translate": [
            "Biglaan sa loob ng isang araw",
            "Unti-unti sa loob ng ilang araw",
            "Hindi sigurado",
            "Walang malinaw na pagbabago",
        ],
    },
    {
        "question": "How would you describe your overall body condition today?",
        "choices": [
            "Almost normal",
            "Slightly weak or uncomfortable",
            "Noticeably weak or painful",
            "Very weak, difficulty doing daily activities",
        ],
        "question_translate": "Paano mo ilalarawan ang kalagayan ng iyong katawan ngayon?",
        "choices_translate": [
            "Halos normal",
            "Bahagyang nanghihina o hindi komportable",
            "Kapansin-pansing nanghihina o masakit ang katawan",
            "Napakahina at hirap sa pang-araw-araw na gawain",
        ],
    },
    {
        "question": "How often have you experienced headaches recently?",
        "choices": ["Not at all", "Occasionally", "Frequently", "Almost constantly"],
        "question_translate": "Gaano kadalas kang nakakaranas ng sakit ng ulo kamakailan?",
        "choices_translate": [
            "Hindi kailanman",
            "Paminsan-minsan",
            "Madalas",
            "Halos palagi",
        ],
    },
    {
        "question": "When you have a headache, how intense does it feel?",
        "choices": [
            "Mild pressure",
            "Moderate pain but tolerable",
            "Strong pain affecting focus",
            "Severe pain affecting daily activities",
        ],
        "question_translate": "Kapag sumasakit ang iyong ulo, gaano ito kalala?",
        "choices_translate": [
            "Banayad na pressure",
            "Katamtamang sakit ngunit natitiis",
            "Malakas na sakit na nakakaapekto sa pag-iisip",
            "Matinding sakit na nakakaapekto sa gawain",
        ],
    },
    {
        "question": "How has your appetite changed recently?",
        "choices": [
            "No change",
            "Slight decrease",
            "Significant decrease",
            "Unable to eat normally",
        ],
        "question_translate": "Paano nagbago ang iyong gana sa pagkain kamakailan?",
        "choices_translate": [
            "Walang pagbabago",
            "Bahagyang nabawasan",
            "Malaking nabawas",
            "Hindi makakain nang normal",
        ],
    },
    {
        "question": "Have you experienced nausea recently?",
        "choices": ["Not at all", "Occasionally", "Frequently", "Almost all the time"],
        "question_translate": "Nakakaranas ka ba ng pagduduwal kamakailan?",
        "choices_translate": [
            "Hindi kailanman",
            "Paminsan-minsan",
            "Madalas",
            "Halos palagi",
        ],
    },
    {
        "question": " Have you vomited since feeling unwell?",
        "choices": ["No", "Once", "Several times", "Frequently or daily"],
        "question_translate": " Nagsuka ka ba mula nang makaramdam ng sakit?",
        "choices_translate": [
            "Hindi",
            "Isang beses",
            "Ilang beses",
            "Madalas o araw-araw",
        ],
    },
    {
        "question": "Have you noticed any skin changes recently?",
        "choices": [
            "No",
            "Mild redness or itching",
            "Visible rashes",
            "Spreading or worsening rashes",
        ],
        "question_translate": "May napansin ka bang pagbabago sa balat kamakailan?",
        "choices_translate": [
            "Wala",
            "Bahagyang pamumula o pangangati",
            "May pantal",
            "Kumakalat o lumalala ang pantal",
        ],
    },
    {
        "question": "Have you noticed changes in your eyes?",
        "choices": [
            "No changes",
            "Mild redness or irritation",
            "Redness with discomfort",
            "Redness with pain or light sensitivity",
        ],
        "question_translate": "May napansin ka bang pagbabago sa iyong mga mata?",
        "choices_translate": [
            "Walang pagbabago",
            "Bahagyang pamumula o iritasyon",
            "Pamumula na may kirot",
            "Pamumula na may sakit o pagiging sensitibo sa liwanag",
        ],
    },
    {
        "question": "How do your eyes react to bright light or screens?",
        "choices": [
            "No discomfort",
            "Slight discomfort",
            "Need to squint or rest eyes",
            "Avoid light due to discomfort",
        ],
        "question_translate": "Paano tumutugon ang iyong mga mata sa maliwanag na ilaw o screen?",
        "choices_translate": [
            "Walang problema",
            "Bahagyang hindi komportable",
            "Kailangang ipikit o ipahinga ang mata",
            "Iniiwasan ang liwanag",
        ],
    },
    {
        "question": "When pressing on your abdomen, what do you feel?",
        "choices": [
            "No discomfort",
            "Mild tenderness",
            "Noticeable pain",
            "Pain that makes you avoid pressure",
        ],
        "question_translate": "Kapag pinipisil ang iyong tiyan, ano ang iyong nararamdaman?",
        "choices_translate": [
            "Walang sakit",
            "Bahagyang kirot",
            "Kapansin-pansing sakit",
            "Sakit na iniiwasan ang pagdiin",
        ],
    },
    {
        "question": "Have you noticed changes in your bowel movements?",
        "choices": [
            "No changes",
            "Slightly looser than usual",
            "Frequent loose stools",
            "Persistent diarrhea",
        ],
        "question_translate": "May pagbabago ba sa iyong pagdumi?",
        "choices_translate": [
            "Walang pagbabago",
            "Bahagyang malambot ang dumi",
            "Madalas na malambot ang dumi",
            "Tuloy-tuloy na pagtatae",
        ],
    },
    {
        "question": "How does abdominal discomfort affect your movement?",
        "choices": [
            "No effect",
            "Slight discomfort when bending",
            "Pain limits bending or twisting",
            "Pain limits normal movement",
        ],
        "question_translate": "Paano naaapektuhan ng pananakit ng tiyan ang iyong paggalaw?",
        "choices_translate": [
            "Walang epekto",
            "Bahagyang kirot kapag yumuyuko",
            "Nililimitahan ang pagyuko o pag-ikot",
            "Nililimitahan ang normal na galaw",
        ],
    },
    {
        "question": "Which activity makes fatigue most noticeable?",
        "choices": [
            "Walking",
            "Standing",
            "Household/work tasks",
            "Resting still feels tiring",
        ],
        "question_translate": "Sa anong gawain pinaka-napapansin ang pagkapagod?",
        "choices_translate": [
            "Paglalakad",
            "Pagtayo",
            "Gawain sa bahay o trabaho",
            "Kahit nagpapahinga ay pagod pa rin",
        ],
    },
    {
        "question": "How would you describe your energy level even after rest?",
        "choices": [
            "Normal",
            "Slightly tired",
            "Easily exhausted",
            "Extremely fatigued",
        ],
        "question_translate": "Paano mo ilalarawan ang iyong lakas kahit pagkatapos magpahinga?",
        "choices_translate": [
            "Normal",
            "Bahagyang pagod",
            "Mabilis mapagod",
            "Matinding pagkapagod",
        ],
    },
    {
        "question": "What happens when you press or massage your calves?",
        "choices": [
            "No pain or discomfort",
            "Mild soreness",
            "Clear pain or tenderness",
            "Strong pain causing withdrawal",
        ],
        "question_translate": "Ano ang nararamdaman kapag pinipisil o minamasahe ang iyong binti (calf)?",
        "choices_translate": [
            "Walang sakit",
            "Bahagyang kirot",
            "May malinaw na sakit o lambot",
            "Matinding sakit",
        ],
    },
    {
        "question": "How do your legs feel when walking or climbing stairs?",
        "choices": [
            "Same as usual",
            "Slight heaviness",
            "Pain or stiffness with movement",
            "Pain that limits walking",
        ],
        "question_translate": "Ano ang pakiramdam ng iyong mga binti kapag naglalakad o umaakyat ng hagdan?",
        "choices_translate": [
            "Karaniwan lang",
            "Bahagyang mabigat",
            "Masakit o matigas kapag gumagalaw",
            "Sakit na nakakahadlang sa paglalakad",
        ],
    },
]

# RECOMENDATIONS BASED ON RISK LEVEL
RECOMMENDATIONS = [
    {
        "classification": "Safe",
        "recommendation": "Recommend practicing preventive measures, avoiding flood water exposure, and maintaining good hygiene.",
    },
    {
        "classification": "Mild",
        "recommendation": "Recommend to take medicine antibiotics are needed. Keep a close watch on your symptoms.",
    },
    {
        "classification": "Moderate",
        "recommendation": "Recommend taking antibiotics only with a proper prescription from a health worker. Laboratory tests may be needed to confirm your condition.",
    },
    {
        "classification": "Severe",
        "recommendation": "Recommend going to the nearest hospital immediately for urgent medical care.",
    },
]
