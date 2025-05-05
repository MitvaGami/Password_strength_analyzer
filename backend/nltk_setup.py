"""
Script to download and verify NLTK WordNet data.
Run this script before starting the Flask application.
"""

import os
import sys
import nltk
from pathlib import Path


def setup_wordnet():
    print("Setting up NLTK WordNet...")

    # Download WordNet if not already present
    print("Downloading WordNet...")
    nltk.download('wordnet')

    # Verify the download was successful
    nltk_data_path = os.path.join(os.path.expanduser(
        '~'), 'AppData', 'Roaming', 'nltk_data')
    wordnet_path = os.path.join(nltk_data_path, 'corpora', 'wordnet')

    print(f"Expected WordNet path: {wordnet_path}")
    if os.path.exists(wordnet_path):
        print(f"✓ WordNet data found at: {wordnet_path}")
    else:
        print(f"✗ WordNet data NOT found at expected location")

    # Test if WordNet can be loaded
    try:
        from nltk.corpus import wordnet
        synsets = wordnet.synsets('test')
        print(
            f"✓ WordNet successfully loaded! Found {len(synsets)} synsets for the word 'test'")
    except Exception as e:
        print(f"✗ Error loading WordNet: {e}")

    print("\nIf you see any errors above, try the following troubleshooting steps:")
    print("1. Make sure you have internet connection when downloading")
    print("2. Try running Python as administrator")
    print("3. Manually create the directory structure if needed")
    print("4. Verify your NLTK installation with 'pip install --upgrade nltk'")


if __name__ == "__main__":
    setup_wordnet()
