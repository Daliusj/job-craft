 
# JobCraft and Jobcraft Insights - Web Scraping and Data Analysis Toolset

## Project Installation
The installation process outlined below is applicable for the entire JobCraft and JobCraft Insights project.
To install the project, clone the repository and install the required dependencies:
```bash
git clone [Your Repository URL]
cd [Repository Name]
pip install -r requirements.txt

## JOBCRAFT (backend)

**JobCraft** is a comprehensive web scraping program for job listings.

#### Features
- **Web Scraping:** Utilizes Selenium and BeautifulSoup to scrape job listings from the CV.lt website.
- **Data Management:** Manages job-related data stored in CSV format, supporting functionalities such as loading, appending, overwriting, and updating data.
- **GPT-4 Parsing:** Uses the OpenAI GPT-4 model for parsing job descriptions and extracting information such as hard/soft skills, minimum experience, technologies, and a binary indicator for programmer roles.
- **Logging:** Provides logging capabilities with file and console output support to track updates and potential errors during execution.
- **Configurability:** Allows configuration of parameters such as search keywords, timing between requests, and log paths.

#### Usage
To run the script, execute it from the command line with the desired action:
```bash
python script_name.py update
```
Optional argument:
- `--full` or `-f`: Run a full update, overwriting existing data.
- The script logs updates and errors to facilitate tracking and debugging.

#### Configuration
Adjust the configuration parameters in the script to match your requirements, such as search keywords, timing between requests.

#### Frontend Integration
For frontend integration, the script provides functions to retrieve data and information.

#### Files and Modules
- `CvLtScraper.py`: Web scraping job listings from CV.lt with search keywords, configurable parameters, and logging capabilities.
- `WebScraper.py`: A simple web scraper with error handling and logging functionality.
- `Data.py`: Manages job-related data in CSV format with loading, appending, updating, and retrieval functionalities.
- `GptParser.py`: Parses job descriptions, extracting structured information like skills and experience requirements.
- `Logger.py`: Basic logging utility with file and console output.
- `jobcraft.py`: Updates and logs job crafting data, with a command-line interface for execution.

## JOBCRAFT INSIGHTS (frontend)

**JobCraft Insights** - Data Analysis Tool

JobCraft is a versatile frontend and data analysis tool tailored for developers and software engineers to explore and analyze the dynamic job market. The tool incorporates web scraping capabilities to collect and analyze job listings from the CV.lt website, providing insights into job trends and facilitating personalized job searches.

#### Features
- **Data Retrieval and Filtering**
  - Jobs Data Exploration: View and explore detailed information about job listings, including titles, companies, salaries, minimum experience, locations, and validity periods.
  - Real-Time Data Updates: Utilize web scraping to ensure up-to-date job data retrieval.
  - Filtering Options: Customize your job search using filters such as salary range, minimum experience, preferred technologies.

- **Data Visualization**
  - Salary Distribution: Visualize the distribution of job salaries.
  - Company Distribution: Explore the number of job listings per company.
  - Hard and Soft Skills Word Clouds: Gain insights into the most frequently mentioned hard and soft skills.
  - Minimum Experience Required: Understand the distribution of minimum experience requirements.
  - Technologies Word Cloud: Explore the technologies mentioned in job listings.
  - Company-wise Salary Comparison: Compare average salaries across different companies.
  - Job Title Word Cloud: Discover the most common job titles.
  - Job Distribution by Technology: Visualize job distribution based on preferred technologies.

#### Launching JobCraft Insights with Streamlit
To launch the JobCraft Insights (frontend) with Streamlit, ensure you have Streamlit installed in your environment.
Navigate to the directory containing the Home.py script and execute it using Streamlit:

```bash
streamlit run Home.py
```

This command will start the Streamlit server and the JobCraft Insights interface will be accessible in your web browser.


```

