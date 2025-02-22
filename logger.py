import logging

def setup_logger():
    """Setup logging for the AI assistant."""
    logging.basicConfig(
        filename="output.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

logging.info("Logger initialized.")
