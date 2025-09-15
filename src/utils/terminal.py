# terminal_anim.py
from rich.console import Console
from rich.live import Live
from rich.text import Text
import threading
import time

class AnimatedTerminal:
    def __init__(self, width=40, fps=20):
        self.console = Console()
        self.width = width
        self.fps = fps
        self.queue = []          # Warteschlange für Texte
        self.running = True
        self.lock = threading.Lock()
        
        # Startet die Live-Animation in einem separaten Thread
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def println(self, text):
        """Text zur Anzeige in die Warteschlange legen"""
        with self.lock:
            self.queue.append(text)

    def _run(self):
        pos = 0
        direction = 1
        current_text = ""
        color_styles = ["bold red", "bold green", "bold yellow", "bold blue", "bold magenta", "bold cyan"]

        with Live(console=self.console, refresh_per_second=self.fps) as live:
            while self.running:
                # Hole Text aus der Warteschlange
                with self.lock:
                    if self.queue:
                        current_text = self.queue.pop(0)

                # Animierte Position
                colored_text = Text(" " * pos + current_text, style=color_styles[pos % len(color_styles)])
                live.update(colored_text)

                # Update Position
                pos += direction
                if pos >= self.width or pos <= 0:
                    direction *= -1

                time.sleep(1 / self.fps)

    def stop(self):
        """Animation stoppen"""
        self.running = False
        self.thread.join()
