import time

import obsws_python as obs


class Observer:
    def __init__(self):
        self._client = obs.EventClient()
        self._client.callback.register(
            [
                self.on_scene_item_selected,
            ]
        )
        print(f"Registered events: {self._client.callback.get()}")
        self.running = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._client.disconnect()
    
    def on_scene_item_selected(self, data):
        """A Scene item has been selected."""
        print(f"{data.scene_item_id} item toggled")


if __name__ == "__main__":
    with Observer() as observer:
        while observer.running:
            time.sleep(0.1)