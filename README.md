# AI Travel Planner with crewAI and Streamlit

This project is a comprehensive, AI-powered travel planner built using **Streamlit** for the user interface and **crewAI** for the intelligent backend. It uses a team of specialized AI agents to generate a complete, personalized travel itinerary based on user preferences.

## Demo

*(Add your screenshots or a GIF of the application in action here!)*



## Features

* **Interactive UI:** A clean, multi-tab Streamlit form to capture all necessary travel details, including basic info, preferences, and special requests.
* **Dynamic Travel Persona:** Calculates your "Travel Persona" (e.g., Adventure Seeker, Culture Explorer) on the fly based on your selected interests.
* **Multi-Agent Backend:** Uses a `crewAI` team of 5 specialized agents:
    * **Travel Coordinator:** Handles flights, hotels, and logistics.
    * **Budget Analyst:** Provides detailed cost breakdowns and money-saving tips.
    * **Travel Planner:** Creates a detailed day-by-day itinerary.
    * **Local Expert:** Offers authentic local insights, safety tips, and hidden gems.
    * **Experience Curator:** Designs unique, memorable experiences based on your interests.
* **Comprehensive Output:** Generates a complete plan displayed in organized tabs (Overview, Itinerary, Travel & Stay, Budget, etc.).
* **Downloadable Plan:** Allows you to download the full itinerary as a `.txt` file.
* **API Key Check:** Verifies if the `GOOGLE_API_KEY` is loaded correctly and displays a warning in the sidebar if it's missing.

## Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **AI Agents:** [crewAI](https://www.crewai.com/)
* **LLM:** Google Gemini (via `langchain-google-genai`)
* **Dependencies:** `python-dotenv`

## Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
````

### 2\. Create a Virtual Environment

This project uses a virtual environment (`.venv`) to manage dependencies.

```bash
# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# For Windows
python -m venv .venv
.\.venv\Scripts\activate
```

### 3\. Install Required Packages

The `requirements.txt` file contains all the necessary Python libraries.

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file, create one and add the following:

**`requirements.txt`**

```
streamlit
crewai
python-dotenv
langchain-google-genai
```

Then run `pip install -r requirements.txt`.

### 4\. Set Up Environment Variables

The project requires a Google API Key to use the Gemini model.

1.  Create a new file named `.env` in the root of your project directory.
2.  Add your API key to this file:

**`.env`**

```
GOOGLE_API_KEY="your_google_api_key_here"
```

##  How to Run

Once you have completed the setup, you can run the Streamlit app with the following command:

```bash
streamlit run app.py
```

This will start the application, and you can access it in your web browser at `http://localhost:8501`.

##  Project Structure

```
.
├── app.py              # The main Streamlit frontend application
├── trip_agents.py      # The crewAI backend, defines agents and tasks
├── style.css           # (Optional) CSS file for custom styling
├── requirements.txt    # List of Python dependencies
├── .env                # (You must create this) Stores the GOOGLE_API_KEY
└── README.md           # This file
```

-----

##  Example Output
<img width="1918" height="926" alt="image" src="https://github.com/user-attachments/assets/8d38b4b2-9c29-4666-bccb-05e7c06501b6" />
<img width="1918" height="928" alt="image" src="https://github.com/user-attachments/assets/01df8899-49e1-4618-8968-e92cec53a4f4" />



```
