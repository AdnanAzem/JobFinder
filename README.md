# Job Finder

The **Job Finder** is a command-line tool that matches resumes to job listings using Natural Language Processing (NLP) and external APIs. It extracts skills from resumes, fetches job listings from the [JSearch API](https://jsearch.app/), and ranks jobs based on their relevance to the resume.

## Features

- **Resume Parsing**: Extracts skills from resumes using Hugging Face's `dslim/bert-base-NER` model.
- **Job Fetching**: Fetches job listings from the JSearch API based on user queries.
- **Job Matching**: Ranks jobs based on the similarity between the resume skills and job descriptions.
- **Interactive CLI**: Provides an easy-to-use command-line interface for uploading resumes and searching for jobs.

---

## Prerequisites

Before running the project, ensure you have the following installed:

1. **Python 3.8+**
2. **PostgreSQL** (or use [Neon DB](https://neon.tech/) for a free cloud-hosted PostgreSQL database)
3. **JSearch API Key** (sign up at [JSearch](https://jsearch.app/))

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ai-job-finder.git
   cd ai-job-finder
   ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a ```.env``` file in the root directory.
    - Add your JSearch API key and database connection string:
    ```bash
    DATABASE_URL=postgresql://user:password@host/dbname
    JSEARCH_API_KEY=your_jsearch_api_key
    ```

5. **Initialize the database**:
    - Run the following script to create the database tables:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

---

## Usage
### Command-Line Interface (CLI)
1. **Start the CLI**:

    Run the following command to start the interactive CLI:
    ```bash 
    python main.py start 
    ```

2. **Upload a Resume**

    - Choose option ```1``` to upload a resume.
    - Enter the path to your resume (PDF format).
    - The program will extract skills and store the resume in the database.

    **Example:**
    ```
    --- Job Finder ---
    1. Upload Resume
    2. Search Jobs
    3. Exit
    Choose an option: 1
    Enter the path to your resume (PDF): ./AdnanAzem-CV.pdf
    Resume uploaded successfully! ID: 1
    ```

3. **Search for Jobs**

    - Choose option ```2``` to search for jobs.
    - Enter your resume ID, job title, and location.
    - The program will fetch and display job recommendations.

    **Example:**
    ```
    --- Job Finder ---
    1. Upload Resume
    2. Search Jobs
    3. Exit
    Choose an option: 2
    Enter your resume ID: 1
    Enter job title (e.g., Software Engineer): Software Engineer
    Enter location (e.g., Israel): Israel

    Top Job Recommendations:
    Title: Software Engineer, Company: TechCorp, Score: 0.85
    Title: Full Stack Developer, Company: Innovate Ltd, Score: 0.78
    Title: Python Developer, Company: CodeMasters, Score: 0.72
    ```

4. **Exit**
    - Choose option ```3``` to exit the program.

---

### Graphical User Interface (GUI)
1. **Start the GUI**:
    - Run the following command to start the interactive GUI:
    ```bash 
    python gui.py 
    ```

2. **Upload a Resume**:
    - Click the Browse button to upload a resume (PDF).
    - The resume will be parsed, and the skills will be extracted and stored in the database.
    - The Resume ID will be displayed.

3. **Search for Jobs**:
    - Enter a Job Title (e.g., "Software Engineer") and Location (e.g., "Israel").
    - Click the Search Jobs button.
    - The top job recommendations will be displayed in the text area.

4. **Reset Fields**:
    - Click the Reset button to clear all fields and start over.
---

## Technologies Used

- **Python**: The core programming language.
- **Hugging Face Transformers**: For skill extraction using NLP.
- **JSearch API**: For fetching job listings.
- **PostgreSQL**: For storing resumes and job matches.
- **SQLAlchemy**: For database ORM and management.
- **Click**: For building the command-line interface.
- **Tkinter**: For building the graphical user interface.