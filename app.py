from flask import Flask, render_template, request, redirect, url_for, flash
import os
from utils.extract_text import extract_text_from_file
from utils.analyze_text import analyze_cv, load_template
from utils.highlight_generator import generate_highlighted_image

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "gizli_anahtar_buraya"  # flash mesajlar için gerekli

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_cv():
    if request.method == 'POST':
        if 'cvfile' not in request.files:
            flash("Dosya bulunamadı!", "danger")
            return redirect(request.url)

        file = request.files['cvfile']
        if file.filename == '':
            flash("Lütfen bir dosya seçin!", "warning")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(filepath)

            try:
                extracted_text = extract_text_from_file(filepath)
            except Exception as e:
                flash(f"Dosya işlenirken hata oluştu: {str(e)}", "danger")
                return redirect(request.url)

            template = load_template("developer")
            analysis_result = analyze_cv(extracted_text, template)

            highlighted_image_path = None
            highlights_data = []
            if filename.lower().endswith('.pdf') and (analysis_result.get('weak_phrases') or analysis_result.get('missing_sections')):
                highlighted_image_path, highlights_data = generate_highlighted_image(
                    filepath,
                    analysis_result.get('weak_phrases', []),
                    analysis_result.get('missing_sections', []),
                    os.path.join('static', 'highlighted.png')
                )

            return render_template(
                "index.html",
                extracted_text=extracted_text,
                analysis=analysis_result,
                image_path=highlighted_image_path,
                highlights=highlights_data
            )
        else:
            flash("Sadece PDF ve DOCX dosyaları yükleyebilirsiniz!", "warning")
            return redirect(request.url)

    return render_template("index.html", extracted_text=None, analysis=None, image_path=None, highlights=[])

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
