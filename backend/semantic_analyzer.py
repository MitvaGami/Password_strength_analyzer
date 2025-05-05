import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from nltk.corpus import wordnet
    WORDNET_AVAILABLE = True
    logger.info("NLTK WordNet successfully imported")
except Exception as e:
    WORDNET_AVAILABLE = False
    logger.warning(f"Error importing NLTK WordNet: {e}")
    logger.warning("Semantic analysis will return empty results")


def semantic_match(password):
    """
    Find dictionary words in the password.
    Returns a list of words found in the password that match dictionary entries.
    If WordNet is not available, returns an empty list.
    """
    if not WORDNET_AVAILABLE:
        return []

    try:
        # Extract potential words from the password (only alphabetic characters)
        words = [''.join(filter(str.isalpha, part))
                 for part in password.split()]
        # Filter out empty strings
        words = [word for word in words if word]

        matches = []
        for word in words:
            if word and len(word) > 2:  # Only check words with at least 3 characters
                try:
                    if wordnet.synsets(word):
                        matches.append(word)
                except Exception as e:
                    logger.warning(f"Error checking word '{word}': {e}")

        return matches
    except Exception as e:
        logger.error(f"Error in semantic analysis: {e}")
        return []

# Test function to verify WordNet is working


def test_wordnet():
    if WORDNET_AVAILABLE:
        try:
            test_word = "test"
            synsets = wordnet.synsets(test_word)
            logger.info(
                f"WordNet test successful. Found {len(synsets)} synsets for '{test_word}'")
            return True
        except Exception as e:
            logger.error(f"WordNet test failed: {e}")
            return False
    else:
        logger.warning("WordNet not available for testing")
        return False


# Run test on module import
test_wordnet()
