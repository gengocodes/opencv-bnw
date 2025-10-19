import replicate
import requests

image_url = "saved_image_url.png"
output_path = "result_image_path.png"

output = replicate.run(
    "google/nano-banana",
    input={
        "prompt": (
            "Keep the technical drawing intact without arbitrarily adding or deleting any existing elements. "
            "Follow these rules precisely:\n"
            "1. Remove all elements marked or covered in red.\n"
            "2. Add all new elements drawn in green. Convert every green line into a normal black line with the same "
            "thickness, weight, and stroke style as the existing lines in the image. Convert all green text or numbers "
            "into normal black text that matches the font, size, and alignment of the existing reference numbers.\n"
            "3. Do not alter any part of the image that has no red or green markings.\n"
            "4. Ensure that the added elements and reference numbers are visually consistent with the rest of the drawing — "
            "same line style, same font, and same overall formatting and proportions.\n"
            "Make the result look as if it was part of the original drawing, seamlessly matching its visual style and technical format."
        ),
        "image_input": [image_url],
        "aspect_ratio": "match_input_image",
        "output_format": "png",
    },
)

result_url = output[0] if isinstance(output, list) else output
print(f"Output URL: {result_url}")

img_data = requests.get(result_url).content
with open(output_path, "wb") as f:
    f.write(img_data)

print(f"Cleaned image saved to {output_path}")
