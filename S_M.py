from flask import Flask, render_template, request, jsonify
import os
from image_utils import resize_image

app = Flask(__name__, static_url_path='/static')
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'bmp', 'gif', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Size and suffix mappings
CATEGORY_SIZES = {
    'upper_landing_page': {
        (560, 375): ['-blackcircles-tyres-med.jpg', '-blackcircles-tyres-med.webp'],
        (1120, 750): ['-blackcircles-tyres-lrg.webp'],
        (720, 482): ['blackcircles-tyres-m.webp'],
    },
    'lower_landing_page': {
        (480, 320): ['blackcircles-tyres-mn.webp', 'blackcircles-tyres-mn.jpg'],
    },
    'article_hero_image': {
        (770, 390): ['hero-blackcircles-sm.jpg', 'hero-blackcircles-sm.webp'],
        (1540, 780): ['hero-blackcircles-lrg.webp'],
    },
    'in_article_image': {
        (770, 426): ['article-1-blackcircles-sm.jpg', 'article-1-blackcircles-sm.webp'],
        (1540, 851): ['article-1-blackcircles-lrg.webp'],
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resize_image')
def resize_image_route():
    return render_template('resize_image.html')

@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['image']
    output_dir = request.form['output_dir']
    categories = request.form.getlist('categories[]')

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)

        try:
            # Process selected categories and resize images
            for category in categories:
                sizes = CATEGORY_SIZES.get(category, {})
                for size, suffixes in sizes.items():
                    resize_image(input_path, output_dir, size, suffixes)
            return jsonify({"message": "Images resized and saved successfully!"}), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

