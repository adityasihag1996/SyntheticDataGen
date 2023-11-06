# Synthetic Dataset Generator

## Overview
This project provides a tool for generating a synthetic dataset of images with text overlay. It is designed to create images with random words from either a small or large vocabulary, placed on a variety of background images and using different font styles. This dataset can be useful for various computer vision and machine learning tasks such as OCR (Optical Character Recognition), text detection, and more.

## Features
- Generation of custom-sized datasets.
- Selection between small and large vocabularies.
- Use of custom background images and fonts.
- Output images and ground truth data stored neatly in designated directories.

## Prerequisites
Before running the script, make sure you have installed the required dependencies:

```
pip install -r requirements.txt
```

## Usage

**_NOTE:-_** Before running the script, you can add your own background images to the `/Backgrounds/` directory to personalize the dataset. The repository includes only a few sample background images for demonstration purposes.

Navigate to the cloned repository's directory and execute the script with the required parameters:

```
python runner.py -n <number_of_images> -lv [--large_vocab]
```

+ **-n** or **--dataset_size** is a required argument that specifies the number of images to generate.
+ **-lv** or **--large_vocab** is an optional flag. When specified, the script will use a large vocabulary set; otherwise, it defaults to a small vocabulary.


## Output
The script generates images and stores them in the `/generated_images` directory. A single ground truth file named `/ground_truths.txt` is created, containing the filename, word, and bounding box coordinates for each word in the images.

```
SyntheticDatasetGenerator/
│
├── generated_images_/
│ ├── image_0.png
│ ├── image_0.png
│ └── ...
│
└── ground_truths.txt
```


## Sample Image
Below is a sample image from the generated dataset:

![Sample Image](/sample.png "Sample Image Title")

## Sample Ground Truth
Here's an example of the contents of the ground_truths.txt file:
```
image_0.png,word1,(x1,y1,x2,y2)
image_0.png,word2,(x3,y3,x4,y4)
image_1.png,word3,(x5,y5,x6,y6)
...
```
Coordinates are in the format (x1,y1,x2,y2), where (x1,y1) is the top-left corner and (x2,y2) is the bottom-right corner of the bounding box.

## To Do

- [ ] Implement text rotation for more realistic text placement.
- [ ] Add multiprocessing support to improve image generation speed.
- [ ] Fetch random background and text from the web.

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your proposed changes.

