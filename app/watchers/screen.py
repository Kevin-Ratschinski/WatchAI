import base64
import io

from PIL import ImageGrab
from watchers.watcher import Watcher


class ScreenWatcher(Watcher):
    """
    Monitors screen activity.
    """

    def __init__(self, config):
        super().__init__(config)
        print("ScreenWatcher initialized.")

    def watch(self) -> str | None:
        """
        Takes a screenshot and returns it as a
        Base64-encoded string.
        """
        print("ScreenWatcher: Taking screenshot...")
        try:
            # Take a screenshot
            screenshot = ImageGrab.grab()

            # Convert the image to bytes and then to Base64
            buffered = io.BytesIO()
            screenshot.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            print("ScreenWatcher: Screenshot successfully encoded.")

            return img_str
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
