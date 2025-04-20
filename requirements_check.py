import subprocess
import sys
import shutil
import os
from nltk.data import find

REQUIREMENTS_FILE = "requirements.txt"

class EnvironmentChecker:
    def __init__(self):
        self.missing_packages = []

    def read_requirements(self):
        if not os.path.exists(REQUIREMENTS_FILE):
            print(f"❌ {REQUIREMENTS_FILE} not found.")
            sys.exit(1)

        with open(REQUIREMENTS_FILE, "r") as f:
            packages = [
                line.strip()
                for line in f
                if line.strip() and not line.startswith("#")
            ]
        return packages

    def check_packages(self):
        print("\n📦 Checking Python dependencies...\n")
        for package in self.read_requirements():
            try:
                __import__(package.split("==")[0].split(">=")[0].split("<=")[0])
                print(f"✅ {package} is installed.")
            except ImportError:
                print(f"❌ {package} is missing.")
                self.missing_packages.append(package)

    def check_ollama(self):
        print("\n🤖 Checking for Ollama installation...")
        if shutil.which("ollama") is None:
            print("❌ Ollama is not installed.")
            print("👉 Download it from https://ollama.com/download and make sure it's running.")
        else:
            print("✅ Ollama is installed.")

    def check_nltk_data(self):
        print("\n🔍 Checking NLTK 'punkt' tokenizer data...")
        try:
            find('tokenizers/punkt')
            print("✅ NLTK 'punkt' tokenizer data is already downloaded.")
        except LookupError:
            print("❌ NLTK 'punkt' tokenizer data is not found.")
            print("👉 Run this in Python shell: `import nltk; nltk.download('punkt')`")

if __name__ == "__main__":
    checker = EnvironmentChecker()
    checker.check_packages()
    checker.check_nltk_data()
    checker.check_ollama()
