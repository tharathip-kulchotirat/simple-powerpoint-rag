class PPTProcessingError(Exception):
    """Custom exception for PPT processing failures"""
    def __init__(self, message="Failed to process PowerPoint file"):
        super().__init__(message)

class LLMConfigurationError(Exception):
    """Custom exception for LLM setup issues"""
    def __init__(self, message="LLM configuration error"):
        super().__init__(message)

def handle_errors(func):
    """Global error handler decorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (PPTProcessingError, LLMConfigurationError) as e:
            logger.error(f"Application error: {str(e)}")
            st.error(f"Application error: {str(e)}")
        except Exception as e:
            logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
            st.error("An unexpected error occurred. Please try again.")
    return wrapper