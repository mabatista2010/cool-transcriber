from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size):
    # Create a new image with a white background
    image = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a colored circle as background
    circle_color = '#FF4B4B'  # Match the theme primary color
    draw.ellipse([size//10, size//10, size-size//10, size-size//10], fill=circle_color)
    
    # Draw a microphone icon (simplified as a rectangle and circle)
    mic_color = 'white'
    center_x = size // 2
    center_y = size // 2
    mic_width = size // 4
    mic_height = size // 3
    
    # Draw the microphone body
    draw.rectangle(
        [center_x - mic_width//2, center_y - mic_height//2,
         center_x + mic_width//2, center_y + mic_height//2],
        fill=mic_color
    )
    
    # Draw the microphone top
    draw.ellipse(
        [center_x - mic_width//2, center_y - mic_height//2 - mic_width//4,
         center_x + mic_width//2, center_y - mic_height//2 + mic_width//4],
        fill=mic_color
    )
    
    return image

def main():
    # Ensure static directory exists
    os.makedirs('static', exist_ok=True)
    
    # Generate icons in required sizes
    sizes = [192, 512]
    for size in sizes:
        icon = create_icon(size)
        icon.save(f'static/icon-{size}x{size}.png')
        print(f'Generated icon-{size}x{size}.png')

if __name__ == '__main__':
    main()
