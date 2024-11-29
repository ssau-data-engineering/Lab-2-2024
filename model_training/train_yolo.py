from ultralytics import YOLO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
args = parser.parse_args()

model = YOLO("yolo11n.pt")

results = model.train(data=f"{args.input}/data.yaml", project=f"{args.output}", epochs=100, imgsz=640, device=0)