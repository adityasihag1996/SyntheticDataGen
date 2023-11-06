import math, random
from PIL import Image, ImageStat

# Function to check if the new position overlaps with any existing ones
def check_overlap(new_rect, existing_rects):
    for rect in existing_rects:
        if (new_rect[0] < rect[2] and new_rect[2] > rect[0] and
                new_rect[1] < rect[3] and new_rect[3] > rect[1]):
            return True
    return False

# Get how bright an image is
def get_brightness(im_file, file_mode = False):
    if file_mode:    
        im = Image.open(im_file)
    else:
        im = im_file
    stat = ImageStat.Stat(im)
    gs = (math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2)) 
         for r,g,b in im.getdata())
    return sum(gs)/stat.count[0]

# Get Color for font, depending on brightness of background
def get_color(brightness):
    T = random.randint(175, 255)
    
    color_brightness = 0
    if brightness > 135:
        color_brightness = 0
        while True:
            R, G, B = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            color_brightness = math.sqrt(0.299*(R**2) + 0.587*(G**2) + 0.114*(B**2))
            if color_brightness < 20:
                break
    elif brightness < 135:
        color_brightness = 0
        while True:
            R, G, B = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            color_brightness = math.sqrt(0.299*(R**2) + 0.587*(G**2) + 0.114*(B**2))
            if color_brightness > 230:
                break
    
    return color_brightness, R, G, B, T

# A utility function to calculate the bounding box of the text
def calculate_text_bbox(draw, text, font):
    return draw.textbbox((0, 0), text, font=font)
