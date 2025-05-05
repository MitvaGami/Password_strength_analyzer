from flask import Flask, request, jsonify
from flask_cors import CORS  # Add CORS support
from normalizer import normalize_password
from semantic_analyzer import semantic_match
from context_parser import parse_context
from strength_evaluator import evaluate_strength
from ml_model import predict_strength
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend can connect


@app.route('/api/analyze', methods=['POST'])  # Use correct route
def analyze():
    data = request.get_json()
    if not data or "password" not in data:
        return jsonify({"error": "Missing 'password' in request"}), 400

    password = data["password"]
    logger.info(f"Analyzing password (masked): {password[:2]}{'*' * (len(password)-2)}")

    try:
        normalized = normalize_password(password)
        logger.info("Password normalized successfully")
    except Exception as e:
        logger.error(f"Error normalizing password: {e}")
        normalized = password
    
    try:
        semantic = semantic_match(normalized)
        logger.info(f"Semantic analysis found {len(semantic)} matches")
    except Exception as e:
        logger.error(f"Error in semantic analysis: {e}")
        semantic = []
    
    try:
        context = parse_context(normalized)
        logger.info(f"Context analysis complete: {len(context.get('entities', []))} entities found")
    except Exception as e:
        logger.error(f"Error in context analysis: {e}")
        context = {"entities": [], "year": None}
    
    try:
        heuristic_score = evaluate_strength(normalized)
        logger.info(f"Heuristic strength score: {heuristic_score}")
    except Exception as e:
        logger.error(f"Error in strength evaluation: {e}")
        heuristic_score = 0
    
    try:
        ml_prediction = predict_strength(normalized)
        logger.info(f"ML prediction: {ml_prediction}")
    except Exception as e:
        logger.error(f"Error in ML prediction: {e}")
        ml_prediction = 0

    response = {
        "normalized": normalized,
        "semantic": semantic,
        "context": context,
        "heuristic_strength": heuristic_score,
        "ml_prediction": ml_prediction
    }
    
    logger.info("Analysis complete, returning results")
    return jsonify(response)


if __name__ == '__main__':
    logger.info("Starting Flask server...")
    try:
        # Test NLTK before starting server
        from semantic_analyzer import test_wordnet
        wordnet_status = "available" if test_wordnet() else "NOT available"
        logger.info(f"WordNet is {wordnet_status}")
    except Exception as e:
        logger.warning(f"Could not verify WordNet status: {e}")
    
    app.run(debug=True)