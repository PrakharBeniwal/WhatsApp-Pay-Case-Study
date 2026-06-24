"""Crop individual phone mockups from the NotebookLM prototype images using
hand-measured bounding boxes (auto-detection failed on dark-UI phones / bright tables)."""
import os
from PIL import Image

SRC = r"c:\Users\91960\Claude\Projects\PM journey\whatsapp case study\deck_media"
OUT = r"c:\Users\91960\Claude\Projects\PM journey\whatsapp case study\deck_media\web"
SHEET = r"C:\Users\91960\AppData\Local\Temp\claude\c--Users-91960-Claude-Projects-PM-journey-whatsapp-case-study\c94a0d9e-c941-44cf-9892-4ef852b7abbe\scratchpad\grids"
os.makedirs(OUT, exist_ok=True)

# file -> (key, [ (L,T,R,B), ... ])  hand-measured per phone
BOXES = {
    "sol1_ctwa.png": ("ctwa", [
        (50, 116, 236, 476), (267, 116, 454, 476), (704, 116, 891, 476),
        (922, 116, 1109, 475), (1141, 116, 1328, 476)]),
    # Boxes frame each phone bezel only. Crop top must clear the slide title
    # (~y80) and the device-name labels on the remittance slide; x positions were
    # re-measured off a 2x fine grid so phones aren't clipped or offset.
    "sol2_jiomart.png": ("jiomart", [
        (70, 82, 256, 478), (356, 82, 546, 478), (766, 82, 952, 478), (1090, 82, 1278, 478)]),
    "sol3_5thtab.png": ("fifthtab", [
        (84, 50, 320, 558), (540, 50, 776, 558)]),
    "sol4_remittance.png": ("remit", [
        (508, 74, 694, 484), (705, 70, 920, 490)]),
}

all_crops = []
for fn, (key, boxes) in BOXES.items():
    im = Image.open(os.path.join(SRC, fn)).convert("RGB")
    crops = []
    for i, b in enumerate(boxes, 1):
        c = im.crop(b)
        c.save(os.path.join(OUT, f"{key}_p{i}.png")); crops.append(c)
        print(f"{key}_p{i}: {b} -> {c.size}")
    all_crops.append((key, crops))

ch = 360
total_w = sum(int(c.width*ch/c.height)+12 for _, cs in all_crops for c in cs) + 12
sheet = Image.new("RGB", (max(total_w, 100), ch+24), (236, 229, 221))
xx = 12
for key, crops in all_crops:
    for c in crops:
        w = int(c.width*ch/c.height); sheet.paste(c.resize((w, ch)), (xx, 12)); xx += w+12
sheet.save(os.path.join(SHEET, "contact_sheet.png"))
print("phones:", sum(len(cs) for _, cs in all_crops))
