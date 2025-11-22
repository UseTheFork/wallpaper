import os
import subprocess

from PIL import Image


def clear_output_directories():
    """Clear the thumbnails and catppuccin_mocha directories"""
    thumb_dir = "thumbnails"
    catppuccin_dir = "catppuccin_mocha"

    for directory in [thumb_dir, catppuccin_dir]:
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print(f"Cleared {directory}/")


def renumber_files():
    """Renumber all PNG files in the 'all' directory sequentially"""
    all_dir = "all"

    if not os.path.exists(all_dir):
        print(f"Directory '{all_dir}' not found")
        return

    # Get all PNG files and sort them
    png_files = sorted([f for f in os.listdir(all_dir) if f.endswith(".png")])

    # Rename files to temporary names first to avoid conflicts
    temp_names = []
    for i, filename in enumerate(png_files):
        old_path = os.path.join(all_dir, filename)
        temp_name = f"temp_{i}.png"
        temp_path = os.path.join(all_dir, temp_name)
        os.rename(old_path, temp_path)
        temp_names.append(temp_name)

    # Rename from temporary names to final sequential names
    for i, temp_name in enumerate(temp_names):
        temp_path = os.path.join(all_dir, temp_name)
        new_name = f"{i + 1:03d}.png"
        new_path = os.path.join(all_dir, new_name)
        os.rename(temp_path, new_path)

    print(f"Renumbered {len(png_files)} files")


def convert_to_png():
    """Convert all images in the 'all' directory to PNG format"""
    all_dir = "all"

    if not os.path.exists(all_dir):
        print(f"Directory '{all_dir}' not found")
        return

    # Get all image files
    image_files = [
        f
        for f in os.listdir(all_dir)
        if f.endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
    ]

    for filename in image_files:
        if not filename.endswith(".png"):
            img_path = os.path.join(all_dir, filename)
            # Create new filename with .png extension
            name_without_ext = os.path.splitext(filename)[0]
            new_filename = name_without_ext + ".png"
            new_path = os.path.join(all_dir, new_filename)

            try:
                # Convert to PNG
                im = Image.open(img_path)
                im.save(new_path)

                # Delete original file only after successful conversion
                os.remove(img_path)
                print(f"Converted {filename} to {new_filename}")
            except Exception as e:
                print(f"Error converting {filename}: {e}")
                # If conversion failed and new file was created, remove it
                if os.path.exists(new_path):
                    os.remove(new_path)


def create_thumbnails():
    """Create thumbnails for all images in the 'all' directory"""
    all_dir = "all"
    thumb_dir = "thumbnails"
    catppuccin_dir = "catppuccin_mocha"

    # Create thumbnails directory if it doesn't exist
    os.makedirs(thumb_dir, exist_ok=True)
    os.makedirs(catppuccin_dir, exist_ok=True)

    # Get all PNG files from the all directory
    if not os.path.exists(all_dir):
        print(f"Directory '{all_dir}' not found")
        return []

    image_files = sorted([f for f in os.listdir(all_dir) if f.endswith((".png"))])

    # Create thumbnails
    for filename in image_files:
        img_path = os.path.join(all_dir, filename)
        thumb_path = os.path.join(thumb_dir, filename)
        catppuccin_path = os.path.join(catppuccin_dir, filename)

        try:
            # Verify the image can be opened before processing
            with Image.open(img_path) as img:
                # Convert with lutgen to catppuccin-mocha
                subprocess.run(
                    [
                        "lutgen",
                        "apply",
                        img_path,
                        "-p",
                        "catppuccin-mocha",
                        "-o",
                        catppuccin_path,
                    ],
                    check=True,
                )

                # Create thumbnail
                img.thumbnail((200, 200))
                img.save(thumb_path)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

    return image_files


def update_readme(image_files):
    """Update README.md with a grid of thumbnail images"""
    readme_path = "README.MD"

    # Create markdown content with header
    header = """# UseTheFork's walls

Hi! This is my repository of wallpapers which I've collected over the years.

Disclaimer: These wallpapers are sourced from many, many, many sources on the internet. I did not make any of these, although I have *edited* several of them a little bit and use lutgen to convert them to the catppuccin-mocha colour scheme. Zero credit belongs to me in that regard, I'm simply the collector. If you are the artist of one of these wallpapers, please **contact me** I will happily take the wallpaper down or add credit in this README.

**Note:** Catppuccin Mocha versions of all wallpapers are automatically generated and available in the `catppuccin_mocha/` directory.

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
            full_path = f"all/{filename}"
            grid_content += f"[![{filename}]({thumb_path})]({full_path}) | "
        grid_content += "\n"

    # Write to README
    with open(readme_path, "w") as f:
        f.write(grid_content)


def main():
    print("Clearing output directories...")
    clear_output_directories()

    print("Converting images to PNG...")
    convert_to_png()

    print("Renumbering files...")
    renumber_files()

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
