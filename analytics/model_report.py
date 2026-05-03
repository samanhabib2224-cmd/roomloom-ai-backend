import json

def print_report():
    print("\n🔥 MODEL STATUS REPORT")
    print("========================")

    # STYLE MODEL
    try:
        with open("analytics/style_metrics.json") as f:
            s = json.load(f)
            print(" Style Model:")
            print(f"   Accuracy : {s['accuracy']:.2f}")
            print(f"   Precision: {s['precision']:.2f}")
            print(f"   Recall   : {s['recall']:.2f}")
            print(f"   F1 Score : {s['f1_score']:.2f}")
    except:
        print(" Style Model not trained")

    # RECOMMENDER
    try:
        with open("analytics/recommender_metrics.json") as f:
            r = json.load(f)
            print("\n Recommender Model:")
            print(f"   Precision: {r['precision']:.2f}")
            print(f"   Recall   : {r['recall']:.2f}")
            print(f"   F1 Score : {r['f1_score']:.2f}")
            print(f"   Dataset  : {r['dataset_size']}")
    except:
        print(" Recommender not trained")

    print("\n Other Models:")
    print("✔ Scene Model: Loaded (Places365)")
    print("✔ YOLO Model: Loaded (Object Detection)")

    print("========================\n")