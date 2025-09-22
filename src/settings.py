import os

class settings:
    def __init__(self):
        # Save settings to a specific path, e.g., user's home directory under ".pt1_settings"
        self.settings_path = os.path.join(os.path.expanduser("~"), ".pt1_settings", "pt1_settings.ini")
        os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)

        self.defaults = {
            'theme': 'dark',
            'font_family': 'System',
        }
        self.settings = self.defaults.copy()

        # Ensure file exists and load current settings
        if os.path.exists(self.settings_path):
            self.read_settings()
        else:
            self.write_settings(self.settings)

    def write_settings(self, updates: dict | None = None) -> dict:
        """
        Writes settings to the file. If updates provided, they are merged first.
        Returns the final settings dict.
        """
        if updates:
            self.settings.update(updates)

        os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
        with open(self.settings_path, 'w', encoding='utf-8') as f:
            for key, value in self.settings.items():
                f.write(f"{key}={value}\n")
        return self.settings.copy()

    def read_settings(self) -> dict:
        """
        Reads settings from file and returns them as a dict.
        Missing keys fall back to defaults.
        """
        data = self.defaults.copy()
        if os.path.exists(self.settings_path):
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or '=' not in line:
                        continue
                    key, value = line.split('=', 1)
                    data[key] = value
        self.settings = data
        return data.copy()

    def get(self, key: str, default=None):
        """
        Returns a single setting with optional default.
        """
        # Ensure in-memory state matches file
        if not self.settings:
            self.read_settings()
        return self.settings.get(key, default)

    def set(self, key: str, value):
        """
        Sets a single setting and persists it.
        """
        self.write_settings({key: value})