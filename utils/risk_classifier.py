RISK_ORDER = {
    "Safe": 0,
    "Mild": 1,
    "Moderate": 2,
    "Severe": 3,
}


def compute_risk(test_class, test_conf, eye_class, eye_conf):

    if test_class == "Unknown":
        return eye_class
    if eye_class == "Unknown":
        return test_class

    test_score = RISK_ORDER[test_class]
    eye_score = RISK_ORDER[eye_class]

    # 🔥 SAFETY RULE
    if test_score == 3 or eye_score == 3:
        return "Severe"

    # weighted (70% test, 30% eye)
    final_score = (test_score * 0.7) + (eye_score * 0.3)

    final_index = round(final_score)

    for key, value in RISK_ORDER.items():
        if value == final_index:
            return key
