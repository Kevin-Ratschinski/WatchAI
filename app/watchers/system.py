import json

import psutil
from watchers.watcher import Watcher


class SystemWatcher(Watcher):
    """A watcher that collects system statistics."""

    def watch(self) -> str:
        """Collects CPU and memory"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()

        data = {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_info.percent,
        }

        return json.dumps(data, indent=2)
