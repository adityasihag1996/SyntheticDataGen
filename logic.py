import random
from PIL import Image, ImageDraw, ImageFont

from utils import check_overlap, get_brightness, get_color

# Function to create an image with random words placed on it
def create_random_words_image(words, backgrounds, fonts, output_path='output_image.png'):
    background_path = random.choice(backgrounds)
    background = Image.open(background_path)
    background_width, background_height = background.size
    draw = ImageDraw.Draw(background)

    # Determine how many words to display (3-6)
    num_words = random.randint(3, 6)
    chosen_words = random.sample(words, num_words)

    # List to keep track of word placements to avoid overlap
    placements = []

    # Dictionary to store the ground truths
    ground_truths = {}

    for word in chosen_words:
        placed = False
        while not placed:
            # Select a random font and size
            font_path = random.choice(fonts)
            font_size = random.randint(20, 100)  # Random font size
            font = ImageFont.truetype(font_path, font_size)

            # Calculate text size using textbbox
            text_width, text_height = draw.textbbox((0, 0), word, font=font)[2:]

            # Ensure text does not go out of bounds
            if text_width > background_width or text_height > background_height:
                continue  # Skip this word or try with a smaller font

            # Attempt to place the text randomly on the canvas without overlapping
            for _ in range(100):  # 100 attempts to find a non-overlapping placement
                random_x = random.randint(0, background_width - text_width)
                random_y = random.randint(0, background_height - text_height)
                new_rect = (random_x, random_y, random_x + text_width, random_y + text_height)

                # Check if within bounds and does not overlap
                if not check_overlap(new_rect, placements) and new_rect[2] <= background_width and new_rect[3] <= background_height:
                    placements.append(new_rect)
                    placed = True
                    break
            
            if not placed:
                # Decrease font size after every failed attempt to fit text
                font_size -= 5
                if font_size < 20:  # If font size is too small, skip word
                    break

        # If placement was successful, proceed with drawing
        if placed:
            # Get brightness and set text color
            brightness = get_brightness(background.crop(new_rect))
            text_color = get_color(brightness)

            # Draw text on the image
            draw.text((random_x, random_y), word, font=font, fill=text_color[1:4])

            # Save the ground truth data
            ground_truths[word] = {'filename': output_path, 'coordinates': new_rect}

    # Save the final image
    background.save(output_path)

    # Return the ground truths
    return ground_truths


# Function to create an image with 1 word placed on it, and cropped output
def generate_and_crop_image(words, backgrounds, fonts, output_path):
    background_path = random.choice(backgrounds)
    background = Image.open(background_path)
    background_width, background_height = background.size
    draw = ImageDraw.Draw(background)

    # Determine how many words to display (3-6)
    word = random.choice(words)

    # Load background and determine its size
    background = Image.open(background_path)
    background_width, background_height = background.size

    # Set an initial large font size
    font_size = 25
    font_path = random.choice(fonts)
    font = ImageFont.truetype(font_path, font_size)
    
    # Create a draw object
    draw = ImageDraw.Draw(background)
    
    # Find the best font size that makes the word span edge to edge
    text_width, text_height = draw.textsize(word, font=font)
    while text_width < background_width and text_height < background_height:
        # Increment the font size until the text width is larger than the background width
        font_size += 1
        font = ImageFont.truetype(font_path, font_size)
        text_width, text_height = draw.textsize(word, font=font)
    
    # Once we have a font size that's too large, step back to the previous size
    font_size -= 1
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(word, font=font)
    
    # Calculate the position to start the text to be centered
    x = (background_width - text_width) // 2
    y = (background_height - text_height) // 2

    brightness = get_brightness(background)
    text_color = get_color(brightness)
    
    # Draw the text
    draw.text((x, y), word, font=font, fill=text_color[1:4])
    
    # Crop the image to the text
    bbox = (x, y, x + text_width, y + text_height)
    cropped_image = background.crop(bbox)
    
    # Save the cropped image
    cropped_image.save(output_path)

    return word
