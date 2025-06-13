import cv2
import os
import logging
from typing import List

logger = logging.getLogger(__name__)

def extract_screenshots_from_video(video_path: str, interval_seconds: int = 60) -> List[str]:
    """
    Video'dan belirli aralıklarla screenshot alır.
    
    Args:
        video_path: Video dosyasının yolu
        interval_seconds: Screenshot'lar arasındaki süre (saniye)
    
    Returns:
        Screenshot dosya yollarının listesi
    """
    screenshot_paths = []
    
    try:
        # Video'yu aç
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError("Video dosyası açılamadı")
        
        # Video özelliklerini al
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_seconds = total_frames / fps
        
        logger.info(f"Video FPS: {fps}, Toplam Frame: {total_frames}, Süre: {duration_seconds:.2f} saniye")
        
        # Screenshot alınacak frame'leri hesapla
        frame_interval = int(fps * interval_seconds)
        screenshot_times = []
        
        for i in range(0, total_frames, frame_interval):
            screenshot_times.append(i)
        
        # Her belirlenen frame'den screenshot al
        for i, frame_number in enumerate(screenshot_times):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = cap.read()
            
            if ret:
                # Screenshot dosya adını oluştur
                screenshot_path = f"temp_screenshot_{i+1}.jpg"
                cv2.imwrite(screenshot_path, frame)
                screenshot_paths.append(screenshot_path)
                
                # Screenshot zamanını hesapla
                screenshot_time = frame_number / fps
                logger.info(f"Screenshot {i+1} alındı: {screenshot_time:.2f} saniye")
            else:
                logger.warning(f"Frame {frame_number} okunamadı")
        
        cap.release()
        
        logger.info(f"Toplam {len(screenshot_paths)} screenshot alındı")
        return screenshot_paths
        
    except Exception as e:
        logger.error(f"Video işleme hatası: {str(e)}")
        raise
    
    finally:
        # Video capture'ı kapat
        if 'cap' in locals():
            cap.release()

def cleanup_screenshots(screenshot_paths: List[str]):
    """
    Geçici screenshot dosyalarını temizler.
    
    Args:
        screenshot_paths: Temizlenecek dosya yollarının listesi
    """
    for path in screenshot_paths:
        if os.path.exists(path):
            try:
                os.remove(path)
                logger.info(f"Geçici dosya silindi: {path}")
            except Exception as e:
                logger.warning(f"Dosya silinemedi {path}: {str(e)}") 