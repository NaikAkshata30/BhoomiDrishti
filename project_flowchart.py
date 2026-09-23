from PIL import Image, ImageDraw, ImageFont

W, H = 1400, 700
bg = '#f5f7fb'
img = Image.new('RGB', (W, H), bg)
draw = ImageDraw.Draw(img)

# Colors
blue = '#3a8dde'
cyan = '#63d4d1'
green = '#7fcf9c'
yellow = '#f6d55c'
orange = '#f7b267'
red = '#ee6c6c'
text = '#1a1f2b'
muted = '#39465a'
line = '#2f3d4d'

# Fonts
try:
    title_font = ImageFont.truetype('arial.ttf', 30)
    body_font = ImageFont.truetype('arial.ttf', 22)
    small_font = ImageFont.truetype('arial.ttf', 18)
except Exception:
    title_font = ImageFont.load_default()
    body_font = ImageFont.load_default()
    small_font = ImageFont.load_default()

# Helper for rounded rect

def rounded_box(x, y, w, h, fill, radius=26, outline=None, width=2):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline or fill, width=width)


def centered_text(x, y, w, h, text_value, font, fill=text):
    bbox = draw.textbbox((0, 0), text_value, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = x + (w - tw) / 2
    ty = y + (h - th) / 2
    draw.text((tx, ty), text_value, font=font, fill=fill)

# Node positions
boxes = [
    {'x': 60, 'y': 80, 'w': 180, 'h': 120, 'fill': '#dfeefb', 'title': 'Data\nSources'},
    {'x': 300, 'y': 80, 'w': 220, 'h': 120, 'fill': '#dffaf8', 'title': 'Ingestion\n& QA'},
    {'x': 590, 'y': 80, 'w': 220, 'h': 120, 'fill': '#dff4d9', 'title': 'MySQL\n+ ORM'},
    {'x': 885, 'y': 80, 'w': 220, 'h': 120, 'fill': '#f0f3d3', 'title': 'Risk\nEngine'},
    {'x': 1180, 'y': 80, 'w': 180, 'h': 120, 'fill': '#f8d9c4', 'title': 'Map\n+ Dashboard'},
]

# Add bottom row
boxes2 = [
    {'x': 255, 'y': 330, 'w': 220, 'h': 110, 'fill': '#e9d9ff', 'title': 'Project\nbarriers'},
    {'x': 560, 'y': 330, 'w': 220, 'h': 110, 'fill': '#fde3c6', 'title': 'Climate\nsignals'},
    {'x': 865, 'y': 330, 'w': 220, 'h': 110, 'fill': '#dfeefb', 'title': 'Scenario\nSimulator'},
]

# draw boxes
for box in boxes + boxes2:
    rounded_box(box['x'], box['y'], box['w'], box['h'], box['fill'], radius=28, outline='#2f3d4d', width=2)
    centered_text(box['x'], box['y'], box['w'], box['h'], box['title'], title_font)

# Arrows connecting row 1
for i in range(len(boxes)-1):
    x1 = boxes[i]['x'] + boxes[i]['w']
    y1 = boxes[i]['y'] + boxes[i]['h']/2
    x2 = boxes[i+1]['x']
    y2 = boxes[i+1]['y'] + boxes[i+1]['h']/2
    draw.line([(x1, y1), (x1 + 30, y1), (x2 - 30, y2), (x2, y2)], fill=line, width=4)
    draw.polygon([(x2-18, y2-10), (x2, y2), (x2-18, y2+10)], fill=line)

# Connect mid row to model and dashboard
# from Risk Engine to bottom items
risk = boxes[3]
for b in boxes2:
    x1 = risk['x'] + risk['w']
    y1 = risk['y'] + risk['h'] / 2
    x2 = b['x']
    y2 = b['y'] + b['h'] / 2
    draw.line([(x1, y1), (x1 + 35, y1), (x2 - 35, y2), (x2, y2)], fill=line, width=4)
    draw.polygon([(x2-18, y2-10), (x2, y2), (x2-18, y2+10)], fill=line)

# extra vertical arrow from MySQL to Risk engine? not necessary

# small title
# draw.text((540, 250), 'Land Acquisition Risk Intelligence Flow', font=title_font, fill=text)

# draw minimal subtitle under top row
subtitle = 'Project data flow'
draw.text((600, 245), subtitle, font=small_font, fill=muted)

# Add small text in the map box area to denote actual features
sub_text = 'project overview\nmap pins\nalerts\nrecommendations'
caption_box = (1188, 230, 1360, 330)
centered_text(caption_box[0], caption_box[1], caption_box[2]-caption_box[0], caption_box[3]-caption_box[1], sub_text, small_font, fill=muted)

img.save('project_flowchart.png')
print('Created project_flowchart.png')
