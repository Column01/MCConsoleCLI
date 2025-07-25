import collections
import json
import threading

import requests


class Server:
    def __init__(self, app, server_name):
        self.app = app
        self.server_name = server_name
        self.output_buffer = collections.deque(maxlen=1000)
        self.player_list_buffer = []
        self.headers = {"x-api-key": self.app.api_key} if self.app.api_key else None
        self.base_url = f"{self.app.url}/servers/{server_name}"
        self.stop_event = threading.Event()

        self.output_thread = threading.Thread(target=self.stream_output)
        self.output_thread.start()

        self.player_list_thread = threading.Thread(target=self.update_player_list)
        self.player_list_thread.start()

    def stream_output(self):
        url = self.base_url + "/output"
        try:
            with self.app.session.get(
                url, headers=self.headers, stream=True
            ) as response:
                buffer = ""
                if self.stop_event.is_set() or response.status_code == 404:
                    return
                for chunk in response.iter_content(chunk_size=1):
                    if self.stop_event.is_set():
                        return
                    if chunk:
                        buffer += chunk.decode("utf-8")
                        if "\n" in buffer:
                            lines = buffer.split("\n")
                            buffer = lines[
                                -1
                            ]  # Keep the last incomplete line in the buffer
                            for line in lines[:-1]:
                                try:
                                    json_data = json.loads(line)
                                    self.output_buffer.append(json_data)

                                except json.JSONDecodeError:
                                    print(f"Error decoding JSON: {line}")
        except requests.exceptions.RequestException as e:
            if not self.stop_event.is_set():
                print(f"Error occurred during streaming: {e}")
                self.stop_event.set()
                self.app.refresh_servers()

    def update_player_list(self):
        while not self.stop_event.is_set():
            try:
                response = requests.get(self.base_url + "/players", headers=self.headers)
                response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
                json_data = response.json()
                player_list = json_data.get("players", [])
                self.player_list_buffer = player_list
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while retrieving player list: {e}")
            # Update player list every 5 seconds
            self.stop_event.wait(5)

    def get_output(self):
        return self.output_buffer.copy()

    def get_player_list(self):
        return self.player_list_buffer.copy()

    def stop(self):
        self.stop_event.set()
        self.output_thread.join(timeout=1)
        self.player_list_thread.join(timeout=1)