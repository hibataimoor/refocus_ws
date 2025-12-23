You are correct. For a GitHub repository, a `README.md` file should be professional and informative. I will provide the complete README file content using Markdown, following the format you provided, and removing all emojis to maintain a professional tone.

---

# Refocus (CBT Terminal Assistant)

## Project Overview

**Refocus** is a lightweight, command-line application designed to provide immediate, private, and stigma-free mental wellness support within the Windows desktop environment.

Built using Python and the **Google Gemini API**, Refocus operates in the background by monitoring the user's clipboard for signs of self-critical, overly anxious, or defeatist language. When such a phrase is copied, the application leverages Gemini's reasoning capabilities to **reframe** the negative thought into a balanced, objective, and resilient statement based on principles of Cognitive Behavioral Therapy (CBT).

This tool improves access to self-help and reduces stigma by treating self-criticism as a "thought pattern to be *refactored*" rather than a personal crisis.

## Features

Refocus provides a single, critical function tailored for efficiency and privacy:

* **Clipboard Monitoring:** Runs silently in the terminal, constantly checking for newly copied text.
* **Token-Optimized Reframing:** When negative language is detected, the copied text is sent to the **`gemini-2.5-flash`** model with a highly constrained system prompt, ensuring extremely fast response times and low API costs.
* **CBT Alignment:** The AI's output is strictly limited to reframed, actionable, and objective perspectives, avoiding diagnosis or clinical advice.
* **Crisis Override:** Immediately detects high-risk keywords (e.g., "hurt myself") and prints crucial national hotline information before halting the program.
* **Stigma Reduction:** Keeps the entire interaction private within the user's local terminal, normalizing the act of correcting negative self-talk.

## 1. Prerequisites

To run Refocus, you need the following:

* **Python (3.9+):** The programming language environment.
* **A Gemini API Key:** Obtain one from [Google AI Studio].
* **A `.env` file:** A file to securely store your API key locally.

## 2. Setup and Installation

### A. Clone the Repository

If your project is hosted on GitHub:

```bash
git clone https://github.com/hibataimoor/refocus_ws/
cd refocus_ws

```

### B. Install Dependencies

Use the provided `requirements.txt` file to install all necessary Python libraries:

```bash
pip install -r requirements.txt

```

### C. Configure API Key

1. In the root directory of the project (`/refocus`), create a new file named **`.env`**.
2. Open the `.env` file and paste your Gemini API key in the following format:
```
GEMINI_API_KEY="YOUR_API_KEY_HERE"

```



## 3. Usage

### A. Start the Assistant

Run the main script from your terminal:

```bash
python refocus_app.py

```

### B. Trigger Reframing

1. **Run** the script as shown above.
2. Open any text editor, document, or chat window.
3. Type a phrase that reflects self-doubt, stress, or failure (e.g., "I'm going to fail this exam, I'm just not smart enough.").
4. **Copy** the text (Ctrl+C).

### C. View the Output

The **Refocus** output will instantly appear in your terminal, providing a new, objective perspective on your copied thought:

```
----------------------------------------
✨ **REFOCUS: NEW PERSPECTIVE**
Original Thought: 'I'm going to fail this exam, I'm just not smart enough.'
Reframed: > The task feels difficult, but difficulty is not proof of inability. Focus on the next section you can study and commit 30 minutes to it.
----------------------------------------

```

### D. Stop the Program

To end the monitoring session, press **`Ctrl + C`** in the terminal window.
