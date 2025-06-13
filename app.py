from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.openai_vision import analyze_image_with_gpt
from utils.video_processor import extract_screenshots_from_video, cleanup_screenshots
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

@app.route('/analyze-video', methods=['POST'])
def analyze_video():
    temp_video_path = None
    screenshot_paths = []
    
    try:
        if 'video' not in request.files:
            return jsonify({'error': 'No video uploaded'}), 400

        video_file = request.files['video']
        
        # Dosya türü kontrolü
        if not video_file.filename or '.' not in video_file.filename:
            return jsonify({'error': 'Invalid file format'}), 400
            
        allowed_extensions = {'mp4', 'avi', 'mov', 'mkv', 'wmv'}
        if not any(video_file.filename.lower().endswith(ext) for ext in allowed_extensions):
            return jsonify({'error': 'File type not allowed. Please upload a video file (mp4, avi, mov, mkv, wmv).'}), 400

        # Video dosyasını kaydet
        temp_video_path = "temp_video.mp4"
        video_file.save(temp_video_path)
        logger.info(f"Video saved to {temp_video_path}")
        
        # Video'dan screenshot'ları al (1 dakikada bir)
        screenshot_paths = extract_screenshots_from_video(temp_video_path, interval_seconds=60)
        
        if not screenshot_paths:
            return jsonify({'error': 'No screenshots could be extracted from video'}), 400
        
        # Her screenshot için analiz yap
        analysis_results = []
        for i, screenshot_path in enumerate(screenshot_paths):
            try:
                logger.info(f"Analyzing screenshot {i+1}/{len(screenshot_paths)}")
                result = analyze_image_with_gpt(screenshot_path)
                
                # Screenshot zamanını hesapla (dakika cinsinden)
                screenshot_time_minutes = i + 1
                
                analysis_results.append({
                    'screenshot_number': i + 1,
                    'time_minutes': screenshot_time_minutes,
                    'analysis': result
                })
                
            except Exception as e:
                logger.error(f"Error analyzing screenshot {i+1}: {str(e)}")
                analysis_results.append({
                    'screenshot_number': i + 1,
                    'time_minutes': i + 1,
                    'analysis': f"Analiz hatası: {str(e)}"
                })
        
        logger.info(f"Video analysis completed. {len(analysis_results)} screenshots analyzed.")
        
        return jsonify({
            'success': True,
            'results': analysis_results,
            'total_screenshots': len(analysis_results),
            'message': f'Video analizi tamamlandı. {len(analysis_results)} screenshot analiz edildi.'
        })
        
    except Exception as e:
        logger.error(f"Error during video analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        # Geçici dosyaları temizle
        if temp_video_path is not None and os.path.exists(temp_video_path):
            os.remove(temp_video_path)
            logger.info(f"Temporary video file {temp_video_path} removed")
        
        if screenshot_paths:
            cleanup_screenshots(screenshot_paths)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Kafe analiz API çalışıyor'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
