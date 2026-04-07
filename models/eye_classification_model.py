from ultralytics import YOLO
import cv2
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "eye_model.pt")


class EyeClassificationModel:

    def __init__(self):
        self.model = None

    def load(self):
        if self.model is None:
            self.model = YOLO(MODEL_PATH)
        return self.model

    # def predict(
    #     self,
    #     image_path,
    #     save_dir,
    #     conf=0.60,  # 🔥 match your working script
    #     classes=[0, 1, 2, 3],
    # ):

    #     model = self.load()

    #     results = model.predict(
    #         source=image_path,
    #         conf=conf,
    #         classes=classes,
    #         show_conf=True,
    #         save=False,
    #         show=False,
    #     )

    #     os.makedirs(save_dir, exist_ok=True)

    #     filename = os.path.splitext(os.path.basename(image_path))[0]
    #     save_path = os.path.join(save_dir, f"{filename}_pred.jpg")

    #     plotted_img = None

    #     for r in results:
    #         plotted_img = r.plot()  # ✅ same as your working code

    #     # fallback (just in case)
    #     if plotted_img is None:
    #         plotted_img = cv2.imread(image_path)

    #     cv2.imwrite(save_path, plotted_img)

    #     return {"eye_scan_path": save_path}

    def predict(
        self,
        image_path,
        save_dir,
        conf=0.40,  # 🔥 LOWER THIS
        classes=[0, 1, 2, 3],
    ):

        model = self.load()

        results = model.predict(
            source=image_path,
            conf=conf,
            classes=classes,
            save=False,
            show=False,
        )

        os.makedirs(save_dir, exist_ok=True)

        filename = os.path.splitext(os.path.basename(image_path))[0]
        save_path = os.path.join(save_dir, f"{filename}_pred.jpg")

        plotted_img = None
        classification = "Unknown"
        confidence = 0.0

        for r in results:
            plotted_img = r.plot()

            # ✅ SIMPLE: just take FIRST detection
            if r.boxes is not None and len(r.boxes) > 0:
                box = r.boxes[0]

                cls = int(box.cls[0])
                conf_score = float(box.conf[0])

                classification = model.names[cls]
                # confidence = round(conf_score * 100, 2)
                confidence = conf_score * 100

        # fallback image
        if plotted_img is None:
            plotted_img = cv2.imread(image_path)

        cv2.imwrite(save_path, plotted_img)

        return {
            "classification": classification,
            "confidence": confidence,
            "eye_scan_path": save_path,
        }
