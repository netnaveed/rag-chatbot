import subprocess
import sys
import shutil

# List of required Python packages
required_packages = [
    "nltk",
    "faiss-cpu",
    "sentence-transformers",
    "streamlit",
    "flask",
    "numpy"
]

def install_packages():
    print("\n📦 Installing Python dependencies...\n")
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully.")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}. Please install manually.")

def check_ollama():
    print("\n🤖 Checking for Ollama installation...")
    if shutil.which("ollama") is None:
        print("❌ Ollama is not installed.")
        print("👉 Download it from https://ollama.com/download and make sure it's running.")
    else:
        print("✅ Ollama is installed.")
        print("📌 Example: Run `ollama pull mistral` to download a model.")

def download_nltk_data():
    try:
        import nltk
        nltk.download('punkt')
        print("✅ NLTK 'punkt' downloaded.")
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}")

if __name__ == "__main__":
    install_packages()
    check_ollama()
    download_nltk_data()
