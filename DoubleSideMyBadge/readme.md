# Double-Sided PDF Generator

This script converts a single-sided PDF into a double-sided PDF by creating a rotated version of each page below the original. This is particularly useful for generating double-sided name badges for fanfold paper.

## Requirements

- Python 3
- `fpdf`
- `pdf2image`
- `tqdm`

You can install the required Python packages using pip:

```
pip install fpdf pdf2image tqdm
```

## Usage

```
python3 DoubleSideMyBadge.py input.pdf
```

The script will generate a new PDF file prefixed with the current timestamp and `_DoubleSided_`.

For example, if the input file is `badges.pdf`, the output will be something like `2210271230_DoubleSided_badges.pdf`.

## How It Works

1. The script first converts the PDF pages into images.
2. For each image, it creates a rotated version.
3. Both the original and the rotated versions are added to a new PDF page, one above the other.
4. The process is repeated for all pages.
