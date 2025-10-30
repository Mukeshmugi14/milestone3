"""
CodeGalaxy - AI Models Integration
Hugging Face Inference API integration for Gemma-2B, Phi-2, and CodeBERT
"""

import os
import time
from huggingface_hub import InferenceClient
import database

# Initialize Hugging Face client
def get_hf_client():
    """
    Returns Hugging Face Inference Client
    """
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")

    return InferenceClient(token=api_key)

# Model endpoints
MODEL_ENDPOINTS = {
    "gemma-2b": "google/gemma-2b-it",
    "phi-2": "microsoft/phi-2",
    "codebert": "microsoft/codebert-base"
}

# ============================================================
# CODE GENERATION
# ============================================================

def generate_code(model_name, language, prompt, temperature=0.7, max_tokens=500):
    """
    Generates code using specified model
    Args:
        model_name: "gemma-2b", "phi-2", or "codebert"
        language: Programming language
        prompt: User's code generation prompt
        temperature: Model temperature (0-1)
        max_tokens: Maximum tokens to generate
    Returns: Dict with {success: bool, code: str, tokens: int, time: float, error: str}
    """
    try:
        start_time = time.time()

        client = get_hf_client()
        model_endpoint = MODEL_ENDPOINTS.get(model_name)

        if not model_endpoint:
            return {
                "success": False,
                "code": "",
                "tokens": 0,
                "time": 0,
                "error": f"Invalid model: {model_name}"
            }

        # Construct prompt for code generation
        formatted_prompt = f"""You are a code generation assistant. Generate clean, well-commented {language} code for the following task:

Task: {prompt}

Provide only the code without explanations.

Code:
"""

        # Call Hugging Face Inference API
        try:
            response = client.text_generation(
                formatted_prompt,
                model=model_endpoint,
                max_new_tokens=max_tokens,
                temperature=temperature,
                return_full_text=False
            )

            end_time = time.time()
            response_time = end_time - start_time

            # Extract generated code
            generated_code = response.strip() if isinstance(response, str) else str(response)

            # Estimate tokens (rough approximation)
            tokens_used = len(generated_code.split())

            # Record model usage
            database.record_model_usage(
                model_name=model_name,
                language=language,
                response_time=response_time,
                success=True
            )

            return {
                "success": True,
                "code": generated_code,
                "tokens": tokens_used,
                "time": response_time,
                "error": ""
            }

        except Exception as api_error:
            end_time = time.time()
            response_time = end_time - start_time

            # Record failed usage
            database.record_model_usage(
                model_name=model_name,
                language=language,
                response_time=response_time,
                success=False
            )

            # Determine error type
            error_message = str(api_error)
            if "rate limit" in error_message.lower():
                error_message = "Rate limit reached. Please wait a moment and try again."
            elif "timeout" in error_message.lower():
                error_message = "Request timed out. Please try again."
            else:
                error_message = "Model temporarily unavailable. Please try another model."

            return {
                "success": False,
                "code": "",
                "tokens": 0,
                "time": response_time,
                "error": error_message
            }

    except Exception as e:
        return {
            "success": False,
            "code": "",
            "tokens": 0,
            "time": 0,
            "error": f"Generation error: {str(e)}"
        }

# ============================================================
# CODE EXPLANATION
# ============================================================

def explain_code(code, language, model_name="gemma-2b"):
    """
    Explains provided code
    Args:
        code: Code to explain
        language: Programming language
        model_name: Model to use (default: gemma-2b)
    Returns: Dict with {success: bool, explanation: str, time: float, error: str}
    """
    try:
        start_time = time.time()

        client = get_hf_client()
        model_endpoint = MODEL_ENDPOINTS.get(model_name, MODEL_ENDPOINTS["gemma-2b"])

        # Construct prompt for code explanation
        formatted_prompt = f"""Explain the following {language} code in simple terms. Describe what it does, how it works, and any important details:

```{language}
{code}
```

Explanation:
"""

        try:
            response = client.text_generation(
                formatted_prompt,
                model=model_endpoint,
                max_new_tokens=300,
                temperature=0.7,
                return_full_text=False
            )

            end_time = time.time()
            response_time = end_time - start_time

            explanation = response.strip() if isinstance(response, str) else str(response)

            # Record model usage
            database.record_model_usage(
                model_name=model_name,
                language=language,
                response_time=response_time,
                success=True
            )

            return {
                "success": True,
                "explanation": explanation,
                "time": response_time,
                "error": ""
            }

        except Exception as api_error:
            end_time = time.time()
            response_time = end_time - start_time

            # Record failed usage
            database.record_model_usage(
                model_name=model_name,
                language=language,
                response_time=response_time,
                success=False
            )

            error_message = "Failed to explain code. Please try again."
            return {
                "success": False,
                "explanation": "",
                "time": response_time,
                "error": error_message
            }

    except Exception as e:
        return {
            "success": False,
            "explanation": "",
            "time": 0,
            "error": f"Explanation error: {str(e)}"
        }

# ============================================================
# CODE IMPROVEMENT
# ============================================================

def improve_code(code, language, focus="general", model_name="gemma-2b"):
    """
    Improves provided code based on focus area
    Args:
        code: Code to improve
        language: Programming language
        focus: "Performance", "Readability", "Security", or "Best Practices"
        model_name: Model to use (default: gemma-2b)
    Returns: Dict with {success: bool, improved_code: str, notes: str, time: float, error: str}
    """
    try:
        start_time = time.time()

        client = get_hf_client()
        model_endpoint = MODEL_ENDPOINTS.get(model_name, MODEL_ENDPOINTS["gemma-2b"])

        # Construct prompt for code improvement
        formatted_prompt = f"""Improve the following {language} code focusing on {focus}.
Provide the improved code and explain what changes were made:

Original Code:
```{language}
{code}
```

Improved Code:
"""

        try:
            response = client.text_generation(
                formatted_prompt,
                model=model_endpoint,
                max_new_tokens=500,
                temperature=0.7,
                return_full_text=False
            )

            end_time = time.time()
            response_time = end_time - start_time

            result = response.strip() if isinstance(response, str) else str(response)

            # Try to separate code and notes
            # This is a simple split; in production, you'd want more sophisticated parsing
            parts = result.split("Changes:" if "Changes:" in result else "Explanation:")
            improved_code = parts[0].strip()
            notes = parts[1].strip() if len(parts) > 1 else "Code improved."

            # Record model usage
            database.record_model_usage(
                model_name=model_name,
                language=language,
                response_time=response_time,
                success=True
            )

            return {
                "success": True,
                "improved_code": improved_code,
                "notes": notes,
                "time": response_time,
                "error": ""
            }

        except Exception as api_error:
            end_time = time.time()
            response_time = end_time - start_time

            # Record failed usage
            database.record_model_usage(
                model_name=model_name,
                language=language,
                response_time=response_time,
                success=False
            )

            error_message = "Failed to improve code. Please try again."
            return {
                "success": False,
                "improved_code": "",
                "notes": "",
                "time": response_time,
                "error": error_message
            }

    except Exception as e:
        return {
            "success": False,
            "improved_code": "",
            "notes": "",
            "time": 0,
            "error": f"Improvement error: {str(e)}"
        }

# ============================================================
# CHALLENGE GENERATION
# ============================================================

def generate_challenge(language, topic, difficulty):
    """
    Generates a daily coding challenge
    Args:
        language: Programming language
        topic: Topic (e.g., "Arrays", "Strings", "Functions")
        difficulty: "Easy", "Medium", or "Hard"
    Returns: Dict with {success: bool, description: str, hint: str, solution: str, error: str}
    """
    try:
        client = get_hf_client()
        model_endpoint = MODEL_ENDPOINTS["gemma-2b"]

        # Construct prompt for challenge generation
        formatted_prompt = f"""Create a {difficulty} coding challenge in {language} focusing on {topic}.

Provide:
1. Challenge description (what to build)
2. A hint (approach to solve it)
3. A sample solution

Format:
DESCRIPTION: [challenge description]
HINT: [solving approach]
SOLUTION: [code solution]

Generate:
"""

        try:
            response = client.text_generation(
                formatted_prompt,
                model=model_endpoint,
                max_new_tokens=600,
                temperature=0.8,
                return_full_text=False
            )

            result = response.strip() if isinstance(response, str) else str(response)

            # Parse response (simplified parsing)
            description = ""
            hint = ""
            solution = ""

            if "DESCRIPTION:" in result:
                parts = result.split("DESCRIPTION:")[1].split("HINT:")
                description = parts[0].strip()

                if len(parts) > 1:
                    hint_parts = parts[1].split("SOLUTION:")
                    hint = hint_parts[0].strip()

                    if len(hint_parts) > 1:
                        solution = hint_parts[1].strip()

            # Fallback if parsing failed
            if not description:
                description = result
                hint = "Think about the problem step by step."
                solution = "Solution will be provided upon request."

            return {
                "success": True,
                "description": description,
                "hint": hint,
                "solution": solution,
                "error": ""
            }

        except Exception as api_error:
            return {
                "success": False,
                "description": "",
                "hint": "",
                "solution": "",
                "error": "Failed to generate challenge. Please try again."
            }

    except Exception as e:
        return {
            "success": False,
            "description": "",
            "hint": "",
            "solution": "",
            "error": f"Challenge generation error: {str(e)}"
        }

# ============================================================
# MODEL TESTING
# ============================================================

def test_model_api(model_name):
    """
    Tests connection to a specific model
    Args:
        model_name: "gemma-2b", "phi-2", or "codebert"
    Returns: Dict with {connected: bool, message: str, response_time: float}
    """
    try:
        start_time = time.time()

        client = get_hf_client()
        model_endpoint = MODEL_ENDPOINTS.get(model_name)

        if not model_endpoint:
            return {
                "connected": False,
                "message": f"Invalid model: {model_name}",
                "response_time": 0
            }

        # Test with a simple prompt
        test_prompt = "Print 'Hello World' in Python:"

        response = client.text_generation(
            test_prompt,
            model=model_endpoint,
            max_new_tokens=50,
            temperature=0.7,
            return_full_text=False
        )

        end_time = time.time()
        response_time = end_time - start_time

        return {
            "connected": True,
            "message": f"Successfully connected to {model_name}",
            "response_time": response_time
        }

    except Exception as e:
        return {
            "connected": False,
            "message": f"Failed to connect: {str(e)}",
            "response_time": 0
        }

# ============================================================
# BATCH CODE GENERATION (For multiple prompts)
# ============================================================

def batch_generate_code(model_name, language, prompts):
    """
    Generates code for multiple prompts
    Args:
        model_name: Model to use
        language: Programming language
        prompts: List of prompts
    Returns: List of result dicts
    """
    results = []

    for prompt in prompts:
        result = generate_code(model_name, language, prompt)
        results.append(result)

        # Add small delay to avoid rate limiting
        time.sleep(1)

    return results

# ============================================================
# MODEL SELECTION HELPER
# ============================================================

def get_model_info(model_name):
    """
    Returns information about a specific model
    Args:
        model_name: "gemma-2b", "phi-2", or "codebert"
    Returns: Dict with model information
    """
    model_info = {
        "gemma-2b": {
            "name": "Gemma-2B",
            "full_name": "Google Gemma 2B Instruct",
            "description": "Best for general-purpose code generation. Produces clean, well-structured code.",
            "strengths": ["General purpose", "Clear code", "Good documentation"],
            "best_for": ["Web development", "Scripts", "General programming"]
        },
        "phi-2": {
            "name": "Phi-2",
            "full_name": "Microsoft Phi-2",
            "description": "Fast and efficient, great for quick tasks and prototyping.",
            "strengths": ["Speed", "Efficiency", "Quick responses"],
            "best_for": ["Prototyping", "Simple scripts", "Fast iterations"]
        },
        "codebert": {
            "name": "CodeBERT",
            "full_name": "Microsoft CodeBERT",
            "description": "Specialized in code analysis and understanding. Excellent for explanations.",
            "strengths": ["Code analysis", "Understanding", "Documentation"],
            "best_for": ["Code review", "Explanation", "Documentation"]
        }
    }

    return model_info.get(model_name, {
        "name": "Unknown",
        "description": "Model information not available",
        "strengths": [],
        "best_for": []
    })

# ============================================================
# ERROR CODE DETECTION
# ============================================================

def detect_errors(code, language):
    """
    Detects potential errors in code
    Args:
        code: Code to analyze
        language: Programming language
    Returns: Dict with {success: bool, errors: list, suggestions: list}
    """
    try:
        client = get_hf_client()
        model_endpoint = MODEL_ENDPOINTS["codebert"]

        formatted_prompt = f"""Analyze the following {language} code for potential errors, bugs, or issues:

```{language}
{code}
```

List any errors or issues found:
"""

        response = client.text_generation(
            formatted_prompt,
            model=model_endpoint,
            max_new_tokens=200,
            temperature=0.5,
            return_full_text=False
        )

        analysis = response.strip() if isinstance(response, str) else str(response)

        # Parse analysis (simplified)
        errors = []
        if "error" in analysis.lower() or "issue" in analysis.lower():
            errors.append(analysis)

        suggestions = ["Consider reviewing the code for the issues mentioned above."]

        return {
            "success": True,
            "errors": errors if errors else ["No obvious errors detected."],
            "suggestions": suggestions
        }

    except Exception as e:
        return {
            "success": False,
            "errors": [],
            "suggestions": [],
            "error": f"Error detection failed: {str(e)}"
        }
