import pytesseract
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path

def generate_highlighted_image(pdf_path, weak_phrases, missing_sections, output_path):
    pages = convert_from_path(pdf_path, dpi=300)
    image = pages[0]
    draw = ImageDraw.Draw(image)

    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    highlights = []

    # Zayıf ifadeler
    for i, word in enumerate(data['text']):
        for phrase in weak_phrases:
            if phrase.lower() in word.lower().strip():
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                draw.rectangle([(x, y), (x + w, y + h)], outline="red", width=3)
                highlights.append({
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h,
                    "text": f'Zayıf ifade: "{phrase}"'
                })

    # Eksik bölümler - görselde yazı olarak gösteriliyor (isteğe bağlı)
    if missing_sections:
        font = ImageFont.load_default()
        x, y = 10, 10
        draw.text((x, y), "Eksik Bölümler:", fill="orange", font=font)
        y += 15
        for section in missing_sections:
            draw.text((x, y), f"- {section}", fill="orange", font=font)
            y += 15
            # Ayrıca highlights listesine ekleyelim tooltip için
            highlights.append({
                "x": x,
                "y": y,
                "width": 150,
                "height": 15,
                "text": f'Eksik bölüm: {section}'
            })

    image.save(output_path)
    return output_path, highlights
