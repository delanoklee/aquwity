#!/usr/bin/env python3
"""
Generate Acuity app icon - a simple, modern design
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size=512):
    """Create a simple icon with 'A' and focus circles"""

    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Brand colors - purple/indigo gradient
    primary_color = (99, 102, 241, 255)  # Indigo
    secondary_color = (139, 92, 246, 255)  # Purple

    # Draw rounded square background
    margin = size // 8
    draw.rounded_rectangle(
        [(margin, margin), (size - margin, size - margin)],
        radius=size // 6,
        fill=primary_color
    )

    # Draw focus circles (representing focus/attention)
    center = size // 2
    for i in range(3):
        radius = size // 4 - (i * size // 16)
        draw.ellipse(
            [(center - radius, center - radius),
             (center + radius, center + radius)],
            outline=(255, 255, 255, 180 - i * 40),
            width=size // 64
        )

    # Draw large 'A' in the center
    try:
        # Try to use a system font
        font_size = size // 2
        # Try Windows font first, then Linux
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", font_size)
        except:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()

    # Draw 'A'
    text = "A"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (size - text_width) // 2 - bbox[0]
    text_y = (size - text_height) // 2 - bbox[1]

    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)

    return img

def main():
    """Generate icons in multiple sizes"""

    print("Generating Acuity app icons...")

    # Generate high-res base icon
    base_icon = create_icon(512)
    base_icon.save('assets/icon_512.png')
    print("✓ Created icon_512.png")

    # Generate various sizes for different platforms
    sizes = {
        'icon_256.png': 256,
        'icon_128.png': 128,
        'icon_64.png': 64,
        'icon_32.png': 32,
        'icon_16.png': 16,
    }

    for filename, size in sizes.items():
        resized = base_icon.resize((size, size), Image.LANCZOS)
        resized.save(f'assets/{filename}')
        print(f"✓ Created {filename}")

    # Create Windows ICO file (multiple sizes in one file)
    ico_sizes = [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256)]
    base_icon.save('assets/icon.ico', sizes=ico_sizes)
    print("✓ Created icon.ico (Windows)")

    # Create macOS ICNS-compatible PNG
    base_icon.save('assets/icon.icns.png')
    print("✓ Created icon.icns.png (macOS)")

    print("\n✨ All icons generated successfully!")

if __name__ == '__main__':
    main()
