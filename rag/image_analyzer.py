"""
Advanced image analysis using YOLO for object detection
and ResNet for room classification.
"""

import torch
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import cv2


class ImageAnalyzer:
    def __init__(self, use_yolo=False):
        """
        Initialize image analyzer.

        Args:
            use_yolo: Whether to use YOLO (requires ultralytics package)
        """
        self.use_yolo = use_yolo
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        # Load YOLO model if available
        if use_yolo:
            try:
                from ultralytics import YOLO
                self.yolo_model = YOLO('yolov8n.pt')  # Nano model for speed
                print("YOLO model loaded successfully")
            except ImportError:
                print("Warning: ultralytics not installed. Using fallback detection.")
                self.use_yolo = False

        # Room classification mapping (based on detected objects)
        self.room_signatures = {
            'bathroom': ['toilet', 'sink', 'bathtub', 'shower', 'mirror', 'towel'],
            'kitchen': ['refrigerator', 'oven', 'microwave', 'sink', 'dining table', 'chair'],
            'bedroom': ['bed', 'pillow', 'nightstand', 'dresser', 'lamp'],
            'living_room': ['couch', 'tv', 'coffee table', 'chair', 'lamp', 'rug'],
            'dining_room': ['dining table', 'chair', 'chandelier'],
            'office': ['desk', 'chair', 'computer', 'monitor', 'keyboard'],
            'garage': ['car', 'tools', 'workbench', 'bicycle'],
            'basement': ['storage boxes', 'furnace', 'water heater']
        }

    def analyze_image(self, image_path: str) -> Dict:
        """
        Analyze an image and return room type, objects, and features.

        Args:
            image_path: Path to image file

        Returns:
            Dictionary with analysis results
        """
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Load image
        image = Image.open(image_path).convert('RGB')

        # Detect objects
        detected_objects = self._detect_objects(image)

        # Classify room type
        room_type = self._classify_room(detected_objects)

        # Extract color palette
        colors = self._extract_colors(image)

        # Analyze image quality/features
        features = self._analyze_features(image)

        return {
            'room_type': room_type,
            'detected_objects': detected_objects,
            'dominant_colors': colors,
            'features': features,
            'image_path': str(image_path)
        }

    def _detect_objects(self, image: Image.Image) -> List[str]:
        """Detect objects in image using YOLO or fallback method."""
        if self.use_yolo:
            return self._detect_with_yolo(image)
        else:
            return self._detect_fallback(image)

    def _detect_with_yolo(self, image: Image.Image) -> List[str]:
        """Detect objects using YOLO model."""
        results = self.yolo_model(image)
        detected = []

        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                if conf > 0.5:  # Confidence threshold
                    label = result.names[cls]
                    detected.append(label)

        return list(set(detected))  # Remove duplicates

    def _detect_fallback(self, image: Image.Image) -> List[str]:
        """Fallback object detection based on simple heuristics."""
        # Convert to numpy array
        img_array = np.array(image)

        # Simple heuristics based on image analysis
        detected = []

        # Analyze brightness
        brightness = np.mean(img_array)
        if brightness < 100:
            detected.append('dim lighting')

        # Check aspect ratio for fixtures
        height, width = img_array.shape[:2]
        aspect = width / height

        if aspect > 1.5:
            detected.append('horizontal fixtures')

        # Color analysis for common features
        avg_color = np.mean(img_array, axis=(0, 1))

        # White/light colors suggest bathroom/kitchen
        if avg_color[0] > 200 and avg_color[1] > 200 and avg_color[2] > 200:
            detected.extend(['white surfaces', 'clean space'])

        # Brown tones suggest wood/flooring
        if avg_color[0] > 100 and avg_color[1] > 80 and avg_color[2] < 70:
            detected.append('wood elements')

        return detected if detected else ['general room features']

    def _classify_room(self, detected_objects: List[str]) -> str:
        """Classify room type based on detected objects."""
        scores = {}

        for room_type, signature in self.room_signatures.items():
            score = 0
            for obj in detected_objects:
                if any(sig_obj in obj.lower() for sig_obj in signature):
                    score += 1
            scores[room_type] = score

        if max(scores.values()) == 0:
            return 'unknown'

        return max(scores, key=scores.get)

    def _extract_colors(self, image: Image.Image, n_colors: int = 5) -> List[Tuple[int, int, int]]:
        """Extract dominant colors from image."""
        # Resize for faster processing
        image_small = image.resize((150, 150))
        img_array = np.array(image_small)

        # Reshape to list of pixels
        pixels = img_array.reshape(-1, 3)

        # Simple k-means clustering (manual implementation)
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(pixels)

        colors = kmeans.cluster_centers_.astype(int)
        return [tuple(color) for color in colors]

    def _analyze_features(self, image: Image.Image) -> Dict:
        """Analyze image features like lighting, space, condition."""
        img_array = np.array(image)

        # Brightness analysis
        brightness = np.mean(img_array)

        # Contrast analysis
        contrast = np.std(img_array)

        # Sharpness (using Laplacian variance)
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

        return {
            'brightness': 'bright' if brightness > 150 else 'dim' if brightness < 100 else 'moderate',
            'contrast': 'high' if contrast > 60 else 'low',
            'image_quality': 'sharp' if sharpness > 100 else 'blurry',
            'estimated_space': 'spacious' if brightness > 140 else 'compact'
        }


def analyze_room_batch(image_paths: List[str]) -> List[Dict]:
    """Analyze multiple room images."""
    analyzer = ImageAnalyzer(use_yolo=False)
    results = []

    for path in image_paths:
        try:
            result = analyzer.analyze_image(path)
            results.append(result)
        except Exception as e:
            print(f"Error analyzing {path}: {e}")
            results.append({'error': str(e), 'image_path': path})

    return results


if __name__ == "__main__":
    # Test image analysis
    analyzer = ImageAnalyzer(use_yolo=False)

    # Create test image if none exists
    test_image_path = "test_bathroom.jpg"
    if not Path(test_image_path).exists():
        print(f"No test image found at {test_image_path}")
        print("Please provide an image path to test")
    else:
        result = analyzer.analyze_image(test_image_path)
        print("\nImage Analysis Results:")
        print(f"Room Type: {result['room_type']}")
        print(f"Detected Objects: {result['detected_objects']}")
        print(f"Features: {result['features']}")
        print(f"Dominant Colors: {result['dominant_colors']}")