import mss
import mss.tools
from PIL import Image
import io
import base64
from typing import Optional, Tuple
import imagehash

class ScreenshotCapture:
    """Handles screenshot capture and comparison"""

    def __init__(self):
        self.previous_screenshot: Optional[Image.Image] = None
        self.previous_hash: Optional[imagehash.ImageHash] = None

    def capture_screenshot(self) -> Image.Image:
        """Capture a screenshot of the primary monitor"""
        with mss.mss() as sct:
            # Capture the primary monitor
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)

            # Convert to PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')

            return img

    def compare_screenshots(self, img1: Image.Image, img2: Image.Image) -> float:
        """
        Compare two screenshots and return similarity score (0.0 to 1.0)
        Uses perceptual hashing for efficient comparison
        """
        # Resize images for faster comparison
        size = (256, 256)
        img1_resized = img1.resize(size)
        img2_resized = img2.resize(size)

        # Calculate perceptual hashes
        hash1 = imagehash.phash(img1_resized)
        hash2 = imagehash.phash(img2_resized)

        # Calculate similarity (0 = identical, higher = more different)
        hash_diff = hash1 - hash2

        # Convert to similarity score (0.0 to 1.0, where 1.0 is identical)
        # Max hash difference is typically around 64 for completely different images
        max_diff = 64
        similarity = 1.0 - (min(hash_diff, max_diff) / max_diff)

        return similarity

    def capture_and_compare(self) -> Tuple[Image.Image, bool, float]:
        """
        Capture a screenshot and compare with previous one
        Returns: (screenshot, is_inactive, similarity_score)
        """
        current_screenshot = self.capture_screenshot()

        is_inactive = False
        similarity = 0.0

        if self.previous_screenshot is not None:
            similarity = self.compare_screenshots(self.previous_screenshot, current_screenshot)
            # If similarity is very high (>95%), consider it inactive
            is_inactive = similarity > 0.95

        # Update previous screenshot
        self.previous_screenshot = current_screenshot.copy()

        return current_screenshot, is_inactive, similarity

    def image_to_base64(self, img: Image.Image, format: str = 'PNG') -> str:
        """Convert PIL Image to base64 string for API transmission"""
        buffered = io.BytesIO()
        img.save(buffered, format=format)
        img_bytes = buffered.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        return img_base64

    def save_screenshot(self, img: Image.Image, filepath: str):
        """Save screenshot to file"""
        img.save(filepath, 'PNG')

    def get_screenshot_for_api(self) -> Tuple[str, bool, float]:
        """
        Capture screenshot and prepare for API call
        Returns: (base64_image, is_inactive, similarity)
        """
        screenshot, is_inactive, similarity = self.capture_and_compare()
        base64_img = self.image_to_base64(screenshot)
        return base64_img, is_inactive, similarity
