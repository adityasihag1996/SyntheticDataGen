import os, random
from tqdm import tqdm
import argparse

from logic import create_random_words_image, generate_and_crop_image


def parse_opt():
    parser = argparse.ArgumentParser(description="Generate a synthetic dataset of images with text.")

    parser.add_argument("-n", "--dataset_size", type=int, required=True,
                        help="Size of the generated dataset, must be an integer.")
    parser.add_argument("-lv", "--large_vocab", action="store_const", const="large", default="small",
                    help="Vocabulary size: 'small' by default, 'large' if this option is specified")
    parser.add_argument("-s", "--single", action="store_true", default=False,
                    help="Do you want to generate single word images?")

    return parser.parse_args()


def generate_multi_images(n, words, backgrounds, fonts, output_dir = 'gen_multi_images'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the file to write the ground truths
    with open('ground_truths_multi.txt', 'w') as gt_file:
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


def generate_single_images(n, words, backgrounds, fonts, output_dir = 'gen_single_images'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open the file to write the ground truths
    with open('ground_truths_single.txt', 'w') as gt_file:
        # Loop over the number of images to generate
        for i in tqdm(range(n), desc="Generating images"):
            # Call the function to create an image with random words
            image_name = f'image_{i}.png'
            output_path = os.path.join(output_dir, image_name)

            word = generate_and_crop_image(words, backgrounds, fonts, output_path)
            
            # Write ground truths for the current image to the file
            gt_file.write(f"{image_name},{word}\n")

    print("Generation Complete!")


# Example usage:
if __name__ == '__main__':
    # args
    args = parse_opt()

    n = args.dataset_size
    vocab_v = args.large_vocab
    single = args.single

    # Store Words Images in memory
    hindi_vocab = []
    with open(f"{vocab_v}_vocab.txt", "r") as f:
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
    if single:
        generate_single_images(n, hindi_vocab, background_images, fonts)
    else:
        generate_multi_images(n, hindi_vocab, background_images, fonts)

