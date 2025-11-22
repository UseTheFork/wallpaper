import os

from PIL import Image


def create_thumbnails():
    """Create thumbnails for all images in the 'all' directory"""
    all_dir = "all"
    thumb_dir = "thumbnails"

    # Create thumbnails directory if it doesn't exist
    os.makedirs(thumb_dir, exist_ok=True)

    # Get all PNG files from the all directory
    if not os.path.exists(all_dir):
        print(f"Directory '{all_dir}' not found")
        return []

    image_files = sorted([f for f in os.listdir(all_dir) if f.endswith((".png", ".jpg"))])

    # Create thumbnails
    for filename in image_files:
        img_path = os.path.join(all_dir, filename)
        thumb_path = os.path.join(thumb_dir, filename)

        # Open image and create thumbnail
        with Image.open(img_path) as img:
            img.thumbnail((200, 200))
            img.save(thumb_path)

    return image_files


def update_readme(image_files):
    """Update README.md with a grid of thumbnail images"""
    readme_path = "README.MD"

    # Create markdown content with header
    header = """# UseTheFork's walls

Hi! This is my repository of wallpapers which I've collected over the years.

Disclaimer: These wallpapers are sourced from many, many, many sources on the internet. I did not make any of these, although I have *edited* several of them a little bit and use lutgen to convert them to the catppuccin-mocha colour scheme. Zero credit belongs to me in that regard, I'm simply the collector. If you are the artist of one of these wallpapers, please **contact me** I will happily take the wallpaper down or add credit in this README.


# Preview
| Column 1 | Column 2 | Column 3 | Column 4 |
| -------- | -------- | -------- | -------- |
"""

    # Create table rows with 4 columns
    grid_content = header
    cols = 4
    for i in range(0, len(image_files), cols):
        row_files = image_files[i : i + cols]

        # Add images in this row
        grid_content += "| "
        for filename in row_files:
            thumb_path = f"thumbnails/{filename}"
            grid_content += f"![{filename}]({thumb_path}) | "
        grid_content += "\n"

    # Write to README
    with open(readme_path, "w") as f:
        f.write(grid_content)


def main():
    print("Creating thumbnails...")
    image_files = create_thumbnails()

    if image_files:
        print(f"Created {len(image_files)} thumbnails")
        print("Updating README.md...")
        update_readme(image_files)
        print("Done!")
    else:
        print("No images found")


if __name__ == "__main__":
    main()
