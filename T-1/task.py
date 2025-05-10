from jira import JIRA 
from docx import Document
import pdfplumber
import os

# step 1: jira connection setup
JIRA_EMAIL="krunaltemp1312@gmail.com"
JIRA_API_TOKEN="ATATT3xFfGF0m2hT76p98PamB2UplDmhIXqR9TZzXpXiA7Xy34mmK7FZu2wNAdIBIQmpl_enwBKKLwYRv6Orf7nlLYfGcEnA0hLmP4gi1SbALogo74_Hg6KveA6RQ-id8zsS1zuiAABRbTxzOvdYq5cztG1QGUPjG9q_RNBK3MaDaHwFct5bnQo=6369861D"
JIRA_SERVER="https://krunaltemp1312.atlassian.net"
PROJECT_KEY='KAN'

jira_options={'server':JIRA_SERVER}
jira=JIRA(options=jira_options,basic_auth=(JIRA_EMAIL,JIRA_API_TOKEN))


# step 2: extract Requirements from Word (.docx)

def extract_from_docx(path):
    doc=Document(path)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]

def extract_from_pdf(path):
    text_lines=[]
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text=page.extract_text()
            if text:
                lines=[line.strip() for line in text.split('\n') if line.strip()]
                text_lines.extend(lines)
    return text_lines

def extract_from_txt(path):
    with open(path,'r',encoding='utf-8')as file:
        return [line.strip() for line in file if line.strip()]

def extract_requirements(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.docx':
        return extract_from_docx(path)
    elif ext == '.pdf':
        return extract_from_pdf(path)
    elif ext == '.txt':
        return extract_from_txt(path)
    else:
        raise ValueError("Unsupported file type: " + ext)

def classify_lines(lines):
    classified = []
    for line in lines:
        line_lower = line.lower()
        if "epic" in line_lower:
            classified.append((line, "Epic"))
        elif any(x in line_lower for x in ["task", "todo", "feature"]):
            classified.append((line, "Task"))
        elif any(x in line_lower for x in ["sub-task", "step", "detail"]):
            classified.append((line, "Sub-task"))
        else:
            classified.append((line, "Task"))  # Default to task
    return classified


# step 3: Create Jira Tickets.
def create_jira_tickets(requirements):
    seen = set()
    classified = classify_lines(requirements)
    
    for i, (req, issue_type) in enumerate(classified, start=1):
        if req in seen:
            continue
        seen.add(req)

        issue_dict = {
            'project': {'key': PROJECT_KEY},
            'summary': f"{issue_type} {i}: {req[:50]}...",
            'description': req,
            'issuetype': {'name': issue_type}
        }

        issue = jira.create_issue(fields=issue_dict)
        print(f"✅ Created: {issue.key} | Type: {issue_type} | Summary: {req[:50]}")

#step 4: Run the Script.

if __name__=="__main__":
    file_path = r"C:\Users\dell\3D Objects\task-2\TASK_2\requirements.docx"
    reqs=extract_requirements(file_path)
    
    if not reqs:
        print("⚠️ No valid requirements found in the file.")
    else:
        create_jira_tickets(reqs)