import os
from PIL import Image, ImageDraw, ImageFont
import random

def create_placeholder_image(path, width, height, text):
    """Create a placeholder image with the given dimensions and text."""
    # Create a new image with a light gray background
    img = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    # Add a border
    border_color = (200, 200, 200)
    draw.rectangle([(0, 0), (width-1, height-1)], outline=border_color, width=1)
    
    # Add some random decorative elements
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
    
    # Add the text
    try:
        font_size = min(width, height) // 10
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw the text
    draw.text((x, y), text, fill=(150, 150, 150), font=font)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    # Save the image
    img.save(path)
    print(f"Created placeholder image: {path}")

def main():
    # Define the images to create
    images = [
        ('static/images/logo-colegio.png', 200, 100, 'LOGO'),
        ('static/images/hero-image.jpg', 1200, 600, 'IMAGEN PRINCIPAL'),
        ('static/images/actividad-deportes.jpg', 400, 300, 'DEPORTES'),
        ('static/images/actividad-arte.jpg', 400, 300, 'ARTE'),
        ('static/images/actividad-ciencia.jpg', 400, 300, 'CIENCIA'),
        ('static/images/teachers/default.jpg', 200, 200, 'PROFESOR')
    ]
    
    # Create each image
    for path, width, height, text in images:
        create_placeholder_image(path, width, height, text)

if __name__ == "__main__":
    main()
