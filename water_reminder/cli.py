import os
import json
import click
import time
import threading
from pathlib import Path
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import logging
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WaterReminder:
    def __init__(self, interval=None, name=None):
        self.config_dir = Path.home() / ".water-reminder"
        self.config_file = self.config_dir / "config.json"

        config = self._load_config()
        self.interval = interval if interval is not None else config.get("interval", 1.0)
        self.name = name if name is not None else config.get("name", "User")

        if interval is not None or name is not None:
            self._save_config()

        self.running = False
        self.icon = None
        self.last_notification = None
        self.root = None
        self.notification_window = None
        self.lock = threading.Lock()

    def _load_config(self):
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_config(self):
        config = {
            'interval': self.interval,
            'name': self.name
        }
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def create_tray_icon(self):
        size = 128
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        drop_color = (0, 120, 255, 255)
        ripple_color = (0, 120, 255, 100)

        draw.ellipse([(size//4, size//4), (3*size//4, 3*size//4)], fill=drop_color)
        draw.polygon([(size//2, 3*size//4), (size//4, 3*size//4), (size//2, 7*size//8)], fill=drop_color)

        ripple_size = size//4
        draw.ellipse([(size//2-ripple_size, size//2-ripple_size),
                      (size//2+ripple_size, size//2+ripple_size)],
                     outline=ripple_color, width=3)
        return image

    def show_notification(self):
        try:
            with self.lock:
                current_time = datetime.now().strftime("%H:%M:%S")
                self.last_notification = current_time

                if self.icon:
                    self.icon.notify(f"💧 Hey {self.name}, time to drink water! 💧", "Water Reminder")
                    logger.info(f"Notification sent at {current_time}")

                def create_window():
                    try:
                        if self.notification_window:
                            self.notification_window.destroy()

                        self.notification_window = tk.Toplevel()
                        self.notification_window.title("Water Reminder")
                        self.notification_window.geometry("400x200")
                        self.notification_window.configure(bg='#e6f3ff')
                        self.notification_window.attributes('-topmost', True)

                        message = f"💧 Hey {self.name}, time to drink water! 💧\n\nLast reminder: {self.last_notification}"
                        label = ttk.Label(self.notification_window, text=message,
                                          background='#e6f3ff', font=('Arial', 12),
                                          justify='center')
                        label.pack(expand=True, pady=20)

                        button = ttk.Button(self.notification_window,
                                            text="I've had water! 💧",
                                            command=self.close_notification)
                        button.pack(pady=10)

                        self.notification_window.update_idletasks()
                        width = self.notification_window.winfo_width()
                        height = self.notification_window.winfo_height()
                        x = (self.notification_window.winfo_screenwidth() // 2) - (width // 2)
                        y = (self.notification_window.winfo_screenheight() // 2) - (height // 2)
                        self.notification_window.geometry(f'{width}x{height}+{x}+{y}')
                        self.notification_window.lift()
                        self.notification_window.grab_set()
                    except Exception as e:
                        logger.error(f"Error creating window: {str(e)}")

                if self.root:
                    self.root.after(0, create_window)
        except Exception as e:
            logger.error(f"Error showing notification: {str(e)}")

    def close_notification(self):
        with self.lock:
            if self.notification_window:
                try:
                    self.notification_window.grab_release()
                    self.notification_window.destroy()
                    self.notification_window = None
                except:
                    pass

    def run_schedule(self):
        try:
            self.show_notification()
            interval_seconds = int(self.interval * 60)
            logger.info("Water reminder started.")

            while self.running:
                logger.info(f"Waiting {interval_seconds} seconds...")

                for sec in range(interval_seconds, 0, -1):
                    if not self.running:
                        break
                    print(f"⏳ Next reminder in: {sec} sec", end='\r')
                    time.sleep(1)

                if self.running:
                    logger.info("Triggering next reminder...")
                    self.show_notification()
        except Exception as e:
            logger.error(f"Error in schedule loop: {str(e)}")
            self.stop()

    def start(self):
        if self.running:
            logger.info("Reminder already running.")
            return

        try:
            self.running = True

            def start_tk_loop():
                self.root = tk.Tk()
                self.root.withdraw()
                self.root.mainloop()

            tk_thread = threading.Thread(target=start_tk_loop, daemon=True)
            tk_thread.start()

            for _ in range(50):
                if self.root:
                    break
                time.sleep(0.1)

            if not self.root:
                raise RuntimeError("Failed to initialize Tkinter root window.")

            image = self.create_tray_icon()
            menu = Menu(
                MenuItem('Stop', lambda: self.stop()),
                MenuItem('Exit', lambda: self.exit())
            )
            self.icon = Icon("water_reminder", image, "Water Reminder", menu)

            scheduler_thread = threading.Thread(target=self.run_schedule, daemon=True)
            scheduler_thread.start()

            self.icon.run()
        except Exception as e:
            logger.error(f"Error starting reminder: {str(e)}")
            self.stop()

    def stop(self):
        try:
            self.running = False
            if self.icon:
                self.icon.stop()
            if self.notification_window:
                self.close_notification()
            if self.root:
                try:
                    self.root.quit()
                except:
                    pass
            logger.info("Reminder stopped.")
        except Exception as e:
            logger.error(f"Error stopping reminder: {str(e)}")

    def exit(self):
        try:
            self.stop()
            os._exit(0)
        except Exception as e:
            logger.error(f"Error exiting: {str(e)}")
            os._exit(1)

@click.group()
def cli():
    """Water Reminder CLI - Stay hydrated!"""
    pass

@cli.command()
@click.option('--interval', '-i', type=float, help='Set interval in minutes (e.g. 0.1 = 6 sec)')
@click.option('--name', '-n', type=str, help='Set your name for reminders')
def start(interval, name):
    """Start the water reminder"""
    try:
        reminder = WaterReminder(interval, name)
        reminder.start()
    except Exception as e:
        logger.error(f"Failed to start: {str(e)}")
        click.echo("Error: could not start reminder. Check logs.")

@cli.command()
def stop():
    """Stop the water reminder"""
    click.echo("To stop, close the tray icon or end the process manually.")

if __name__ == '__main__':
    cli()
