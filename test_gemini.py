from config import get_gemini_model, GEMINI_API_KEY
import sys

def test_connection():
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_api_key_here":
        print("Error: Please set your GEMINI_API_KEY in the .env file before running this test.")
        sys.exit(1)
        
    print("Testing Gemini API Connection...")
    try:
        model = get_gemini_model()
        response = model.generate_content("Hello! Are you ready to act as a financial advisor? Please respond with a short confirmation.")
        print("\nConnection Successful! Response from Gemini:")
        print("-" * 50)
        print(response.text)
        print("-" * 50)
    except Exception as e:
        print("\nConnection Failed!")
        print(f"Error details: {str(e)}")

if __name__ == "__main__":
    test_connection()
