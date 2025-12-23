import os
import time
import re
import pyperclip
from google import genai
from dotenv import load_dotenv

# --- 1. CONFIGURATION AND INITIALIZATION ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("FATAL ERROR: GEMINI_API_KEY not found in your .env file.")
    exit()

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    exit()

# Define the model
MODEL_NAME = "gemini-2.5-flash"

# --- 2. THE CONSTRAINED SYSTEM PROMPT (Token Saver) ---

SYSTEM_PROMPT = """
You are the "Refocus" assistant, providing rapid mental wellness support via text reframing. Your function is to reframe text that the user has copied (indicating self-criticism or high stress) into a more objective, balanced, and resilient statement using Cognitive Behavioral Therapy (CBT) principles.

Your Rules:
1. Do NOT diagnose, offer therapy, or give medical advice.
2. Be CONCISE. Limit your response to one single, reframed sentence or a brief two-sentence challenge.
3. Refactor: Rewrite the user's input to substitute emotional language with factual language. Frame challenges as solvable obstacles, not personal failures. Maintain a supportive tone, make it sound like a friend and make it personal.
4. Only provide the reframed text. Do not add salutations or additional commentary.

User Input to Refactor:
"""

# --- 3. SAFETY AND STIGMA REDUCTION ELEMENTS ---

CRISIS_KEYWORDS = ["hurt myself", "end my life", "suicide", "can't go on", "kill myself"]
CRISIS_MESSAGE = (
    "\n======================================================\n"
    " REFOCUS SAFETY PROTOCOL ACTIVATED \n"
    "This tool is NOT a substitute for professional care. Please contact:\n"
    "- 988 Suicide & Crisis Lifeline (Call or Text)\n"
    "- Crisis Text Line: Text HOME to 741741\n"
    "The monitoring session has been stopped. Please reach out for support.\n"
    "======================================================"
)

# Basic regex filter to minimize API calls (token saving)
# Triggers on common negative/stress words.
NEGATIVE_PATTERN = re.compile(
    r'(fail|terrible|horrible|useless|worthless|overwhelmed|never|always|disaster|mess up|screw up|stupid|idiot|dumb|unworthy|inadequate|hopeless|desperate|frustrated|angry|upset|depressed|anxious|scared|terrified|overwhelmed|traumatized|disappointed|disgusted|embarrassed|guilty|ashamed|shameful|selfish)', 
    re.IGNORECASE
)

# --- 4. CORE FUNCTION: GEMINI API CALL ---

def get_reframed_text(negative_text: str) -> str:
    """Sends text to Gemini for reframing."""
    
    # We use a single-turn generate_content call for efficiency
    full_prompt = SYSTEM_PROMPT + negative_text

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                {"role": "user", "parts": [
                    {"text": full_prompt}
                ]}
            ]
        )
        # Clean up any residual markdown or extra spaces
        return response.text.strip().replace('**', '').replace('*', '')
    
    except Exception as e:
        return f"[Refocus] Error: Could not connect to the AI model. Check your connection or API key. Details: {e}"

# --- 5. MAIN MONITORING LOOP ---

def start_clipboard_monitor():
    """Runs the main loop to monitor the clipboard."""
    
    print("======================================================")
    print(" Refocus - CBT Terminal Assistant is now running.")
    print(f"   Model: {MODEL_NAME}")
    print("   Action: Copy text containing self-criticism to trigger reframing.")
    print("   Press Ctrl+C to stop the application.")
    print("======================================================")
    
    last_clipboard_content = ""
    
    while True:
        try:
            current_clipboard_content = pyperclip.paste()
            
            # Check for new, non-empty, and different content
            if current_clipboard_content and current_clipboard_content != last_clipboard_content:
                
                # Convert content to lowercase for robust checks
                lower_content = current_clipboard_content.lower()
                
                # A. CRISIS CHECK
                if any(keyword in lower_content for keyword in CRISIS_KEYWORDS):
                    print(CRISIS_MESSAGE)
                    break 
                    
                # B. NEGATIVE WORD FILTER (The token saver)
                if NEGATIVE_PATTERN.search(lower_content) and len(lower_content.split()) > 4: # Min length check
                    
                    reframed_thought = get_reframed_text(current_clipboard_content)
                    
                    # Display the result clearly in the console
                    print("\n----------------------------------------")
                    print(" REFOCUS: NEW PERSPECTIVE")
                    print(f"Original Thought: '{current_clipboard_content.strip()[:60]}...'")
                    print(f"Reframed: > {reframed_thought}")
                    print("----------------------------------------")
                
                last_clipboard_content = current_clipboard_content
                
            time.sleep(1.5) # Check the clipboard every 1.5 seconds

        except KeyboardInterrupt:
            print("\nRefocus monitoring stopped by user. Take care!")
            break
        except pyperclip.PyperclipException:
            # Can occur if another program is blocking clipboard access briefly
            # print("Clipboard access temporarily blocked.") 
            time.sleep(1.5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

# --- 6. EXECUTION ---
if __name__ == "__main__":
    start_clipboard_monitor()