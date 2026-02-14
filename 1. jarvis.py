"""
Ultimate Professional Single-File Voice Assistant
PEP8 / flake8 / pylint compliant
"""

from __future__ import annotations

import os
import datetime
import logging
import webbrowser
import subprocess
from typing import Optional

import pyttsx3
import speech_recognition as sr
import wikipedia


# ==========================================================
# Configuration
# ==========================================================

# ---- Chrome Profile (YOUR PROFILE 16) ----
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_PROFILE = "Profile 16"

# ---- Web URLs ----
GOOGLE_URL = "https://www.google.com"
DRIVE_URL = "https://drive.google.com"
WHATSAPP_WEB_URL = "https://web.whatsapp.com"
LINKEDIN_WEB_URL = "https://www.linkedin.com"
SNAPCHAT_WEB_URL = "https://www.snapchat.com/web"
GMAIL_URL = "https://mail.google.com"
YOUTUBE_URL = "https://www.youtube.com"
INSTAGRAM_URL = "https://www.instagram.com"


# ==========================================================
# Logging Setup
# ==========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

LOGGER = logging.getLogger(__name__)


# ==========================================================
# Assistant Class
# ==========================================================


class JarvisAssistant:
    """Advanced voice-controlled assistant."""

    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self._configure_voice()

    # ------------------------------------------------------

    def _configure_voice(self) -> None:
        voices = self.engine.getProperty("voices")
        if voices:
            self.engine.setProperty("voice", voices[0].id)

    # ------------------------------------------------------

    def speak(self, text: str) -> None:
        LOGGER.info("Speaking: %s", text)
        self.engine.say(text)
        self.engine.runAndWait()

    # ------------------------------------------------------

    def greet_user(self) -> None:
        hour = datetime.datetime.now().hour

        if hour < 12:
            greeting = "Good Morning!"
        elif hour < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"

        self.speak(greeting)
        self.speak("I am Jarvis. How may I help you?")

    # ------------------------------------------------------

    def listen(self) -> Optional[str]:
        try:
            with sr.Microphone() as source:
                LOGGER.info("Listening...")
                self.recognizer.pause_threshold = 1
                audio = self.recognizer.listen(source)

            text = self.recognizer.recognize_google(audio)
            return text.lower().strip()

        except Exception as error:  # pylint: disable=broad-except
            LOGGER.error("Speech error: %s", error)
            return None

    # ------------------------------------------------------
    # Chrome Profile
    # ------------------------------------------------------

    def _open_chrome(self, url: Optional[str] = None) -> None:
        try:
            command = [
                CHROME_PATH,
                f"--profile-directory={CHROME_PROFILE}",
            ]

            if url:
                command.append(url)

            subprocess.Popen(command)
            self.speak("Opening Chrome")

        except OSError as error:
            LOGGER.error("Chrome launch failed: %s", error)
            self.speak("Unable to open Chrome.")

    # ------------------------------------------------------
    # Store App Opener (Microsoft Store apps)
    # ------------------------------------------------------

    def _open_store_app(self, protocol: str, name: str) -> None:
        try:
            subprocess.Popen(f"start {protocol}", shell=True)
            self.speak(f"Opening {name} app")
        except OSError as error:
            LOGGER.error("%s launch failed: %s", name, error)
            self.speak(f"Unable to open {name} app.")

    # ------------------------------------------------------
    # Open Website
    # ------------------------------------------------------

    def _open_website(self, url: str, name: str) -> None:
        webbrowser.open_new_tab(url)
        self.speak(f"Opening {name}")

    # ------------------------------------------------------

    def _open_website_dynamic(self, name: str) -> None:
        url = f"https://www.{name}.com"
        webbrowser.open_new_tab(url)
        self.speak(f"Opening {name} on web")

    # ------------------------------------------------------

    def handle_command(self, command: str) -> None:
        LOGGER.info("Command received: %s", command)

        # ---- Wikipedia ----
        if "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            self.speak("Searching Wikipedia")
            try:
                summary = wikipedia.summary(topic, sentences=2)
                self.speak(summary)
            except wikipedia.exceptions.WikipediaException:
                self.speak("Unable to fetch information.")
            return

        # ---- Time ----
        if "time" in command:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.speak(f"The time is {current_time}")
            return

        # ---- Chrome ----
        if "open chrome" in command:
            self._open_chrome()
            return

        # ---- Google ----
        if "open google" in command:
            self._open_website(GOOGLE_URL, "Google")
            return

        # ---- Drive ----
        if "open drive" in command:
            self._open_website(DRIVE_URL, "Google Drive")
            return

        # ---- WhatsApp (Microsoft Store Version) ----
        if "open whatsapp" in command:
            if "app" in command:
                self._open_store_app("whatsapp:", "WhatsApp")
            else:
                self._open_website(WHATSAPP_WEB_URL, "WhatsApp Web")
            return

        # ---- LinkedIn ----
        if "open linkedin" in command:
            self._open_website(LINKEDIN_WEB_URL, "LinkedIn")
            return

        # ---- Snapchat ----
        if "open snapchat" in command:
            self._open_website(SNAPCHAT_WEB_URL, "Snapchat")
            return

        # ---- Gmail ----
        if "open gmail" in command:
            self._open_website(GMAIL_URL, "Gmail")
            return

        # ---- YouTube ----
        if "open youtube" in command:
            self._open_website(YOUTUBE_URL, "YouTube")
            return

        # ---- Instagram ----
        if "open instagram" in command:
            self._open_website(INSTAGRAM_URL, "Instagram")
            return

        # ---- Dynamic fallback ----
        if "open" in command:
            name = (
                command.replace("open", "")
                .replace("in web", "")
                .replace("app", "")
                .strip()
            )
            if name:
                self._open_website_dynamic(name)
                return

        self.speak("Sorry, I did not understand that command.")


# ==========================================================
# Main
# ==========================================================


def main() -> None:
    assistant = JarvisAssistant()
    assistant.greet_user()

    while True:
        command = assistant.listen()
        if command:
            assistant.handle_command(command)


if __name__ == "__main__":
    main()
