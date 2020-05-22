# Synthetic Dataset Generator (Hindi)

Synthetically create a dataset of images of Devanagari text drawn on images

**Prerequisites:**
- Python 3.5 and above
- PIL (Image)
- numpy
- matplotlib

**You will also need to install Pillow’s require external libraries before you run the code.
The libraries enables PIL to draw complex fonts like Devanagari on images correctly.**

Follow the steps on Pillow's Installation page to install libraries correctly, depending on what system you are using: https://pillow.readthedocs.io/en/stable/installation.html

**How to run script:**

python3 Generator.py "dataset_size" -lv -v -mt

Use the following args for the following use:

Positional arguments:

  dataset_size   ->   Size of the generated dataset


Optional arguments:

  -h, --help   ->   show this help message and exit
  
  -lv, --large_vocab   ->   Use Large Vocab, Default is Small Vocab
  
  -v, --verbose   ->   (Verbose) Display progress of generation
  
  -mt, --multithreading   ->   Use multithreading
