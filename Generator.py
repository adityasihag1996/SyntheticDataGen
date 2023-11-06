import os
from tqdm import tqdm
import argparse

from logic import create_random_words_image


def parse_opt():
    parser = argparse.ArgumentParser(description="Generate a synthetic dataset of images with text.")

    parser.add_argument("-n", "--dataset_size", type=int, required=True,
                        help="Size of the generated dataset, must be an integer.")
    parser.add_argument("-lv", "--large_vocab", action="store_const", const="large", default="small",
                    help="Vocabulary size: 'small' by default, 'large' if this option is specified")
    
    return parser.parse_args()


def generate_images(n, words, backgrounds, fonts, output_dir = 'generation_images'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the file to write the ground truths
    with open('ground_truths.txt', 'w') as gt_file:
        # Loop over the number of images to generate
        for i in tqdm(range(n), desc="Generating images"):
            # Call the function to create an image with random words
            image_name = f'image_{i}.png'
            output_path = os.path.join(output_dir, image_name)
            ground_truths = create_random_words_image(words, backgrounds, fonts, output_path)
            
            # Write ground truths for the current image to the file
            for truth in ground_truths:
                gt_file.write(f"{image_name},{truth},{ground_truths[truth]['coordinates']}\n")

    print("Generation Complete!")


# Example usage:
if __name__ == '__main__':
    # args
    args = parse_opt()

    n = args.dataset_size
    vocab_v = args.large_vocab

    # Store Words Images in memory
    hindi_vocab = []
    with open(f"{vocab_v}_hindi_vocab.txt", "r") as f:
        lines = f.readlines()
    for word in lines:
        hindi_vocab.append(word[:-1])

    # Store Background Images in memory
    background_images = []
    for img in os.listdir("Backgrounds/"):
        if img.startswith('.') is False:
            background_images.append("Backgrounds/" + img)

    # Store Fonts in memory
    fonts = []
    for font in os.listdir("Fonts/"):
        if font.startswith('.') is False:
            fonts.append("Fonts/" + font)

    # The actual execution entry point is here:
    generate_images(n, hindi_vocab, background_images, fonts)
