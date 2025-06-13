from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.openai_vision import analyze_image_with_gpt
import os
import logging

app = Flask(__name__)
CORS(app)  # CORS desteği ekle

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    temp_path = None # temp_path'i başlangıçta tanımla
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image_file = request.files['image']
        
        # Dosya türü kontrolü
        if not image_file.filename or '.' not in image_file.filename:
            return jsonify({'error': 'Invalid file format'}), 400
            
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not any(image_file.filename.lower().endswith(ext) for ext in allowed_extensions):
            return jsonify({'error': 'File type not allowed. Please upload an image.'}), 400

        temp_path = "temp_image.jpg"
        image_file.save(temp_path)

        logger.info(f"Image saved to {temp_path}")
        
        # OpenAI ile analiz
        result = analyze_image_with_gpt(temp_path)
        
        logger.info("Analysis completed successfully")
        
        return jsonify({
            'success': True,
            'result': result,
            'message': 'Kafe analizi tamamlandı'
        })
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Geçici dosyayı temizle
        if temp_path is not None and os.path.exists(temp_path):
            os.remove(temp_path)
            logger.info(f"Temporary file {temp_path} removed")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Kafe analiz API çalışıyor'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
