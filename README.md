Automated Project Development & Planning

Automating project management can significantly improve efficiency and consistency in software development. This project aims to automate the end-to-end project setup process using Python, Streamlit, Jira API, GitHub API, and Natural Language Processing (NLP). The primary goal is to reduce manual effort and streamline project planning, ticket management, repository setup, and test case generation.

📋 Project Tasks Overview

task 1)Automating Jira Ticket Creation from Requirement Docs.
* Extracts requirements from .docx files and automatically creates Jira tickets.
* Uses python-docx for reading .docx files.
* Integrates with the Jira API to create tickets directly from extracted text.

task 2) Automating GitHub Repository Creation and Structuring
* Automatically creates branches based on the Jira tickets created in task 1.
* Creates initial directory structures for each ticket.
* Uses the GitHub API for repository and branch management.

Task 3: Automating Test Case Creation Based on Jira Tickets
* Generates test case files based on the summary and description of Jira tickets.
* Automatically adds the test files to the appropriate GitHub branches.
* Uses consistent branch naming conventions to organize test cases.

🚀 Key Features

* Automated Jira Ticket Creation: Extracts user stories from .docx files and creates corresponding Jira tasks.

* Automated GitHub Branch Creation: Sets up GitHub branches for each Jira ticket with appropriate directory structures.

* Automated Test Case Generation: Generates Python test files for each ticket to ensure quality and consistency.

* Seamless API Integration: Leverages Jira and GitHub APIs for full automation.

* Single-Click Execution: Runs all tasks from a single Streamlit app interface.

🛠️ Technologies Used

Python for scripting and automation.

Streamlit for the interactive web app.

Jira API for ticket management.

GitHub API for repository and branch automation.

NLP (Natural Language Processing) for requirement extraction.

Python Libraries:

jira for Jira API integration.

PyGithub for GitHub API integration.

python-docx for .docx file processing.

📦 Project Structure
Automated-Project-Development-Planning/
├── Task-1/  # Jira Ticket Creation
├── Task-2/  # GitHub Repo Setup
├── Task-3/  # Test Case Generation
├──Streamlit App  # All task with GUI.
└── README.md

📹 Demo Video
The demo video showcasing the complete workflow is available in the repository.

📝 How to Run the Project

Clone the Repository:
git clone https://github.com/Krunalsangani13/Automating-Project-Development-Planning.git

Install Dependencies:
pip install streamlit jira PyGithub python-docx

Run the Streamlit App:
streamlit run Automated_Project_Management_Streamlit.py

Set Up Jira and GitHub Tokens:
* Update the JIRA API Token and GitHub PAT in the Streamlit app interface.
  
Start Automating!

📚 Skills Demonstrated

* Python Programming - Automating real-world tasks using Python.
* NLP - Extracting structured data from unstructured text.
* API Integration - Working with Jira and GitHub APIs.
* Automation - Building end-to-end project automation pipelines.
* Documentation - Creating clear and comprehensive project documentation.




