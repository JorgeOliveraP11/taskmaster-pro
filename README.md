# TaskMaster Pro - SaaS MVP

TaskMaster Pro is a professional corporate task management tool built using **AI-Native Development** workflows. It follows **Clean Architecture** principles to ensure scalability, maintainability, and professional coding standards.

## 🚀 Technologies
- **IDE:** Cursor AI
- **Backend:** Python 3.10+ (FastAPI)
- **Database:** SQLite
- **ORM:** Prisma
- **Testing:** Pytest

## 🏗️ Architecture
The project follows **Clean Architecture**:
- **Domain:** Business entities and repository interfaces.
- **Application:** Use cases and business logic (Service layer).
- **Infrastructure:** External implementations (Prisma, SQLite).
- **Presentation:** FastAPI routers and Pydantic schemas.

## 🛠️ Getting Started

### Prerequisites
- Python installed
- Node.js (required for Prisma CLI)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/JorgeOliveraP11/taskmaster-pro
   cd taskmaster-pro
   ```
2. **Install dependencies:**

```bash
   pip install -r requirements.txt
```
3. **Database Setup:**
Initialize the database and generate the Prisma client:

```bash
   npx prisma db push
   npx prisma generate
```
4. **Run the Application:**

```bash
   uvicorn app.main:app --reload
   The API will be available at http://127.0.0.1:8000/docs.
```
## 🤖 AI Workflow (Cursor AI Prompts)

This project was built using the following prompt sequence in Cursor AI:

1. **Setup (.cursorrules):** "Generate a .cursorrules file for a FastAPI + Prisma + SQLite project. Follow Clean Architecture. Use strong typing, Google-style docstrings, and ensure all API responses follow a standard JSON structure."

2. **Data Modeling (Composer):** "Create a data model in SQLite using Prisma for a task app with fields: id, title, description, status (pending/completed), and creation date."

3. **Logic Generation:** "Generate the API endpoints to manage tasks. Include data validation and global error handling. Also, create a function to filter tasks by status."

4. **Testing:** "Generate a suite of unit tests using pytest for the TaskService. Mock the database calls."

## ✅ Features
- Create, Read, Update, and Delete tasks.
- Filter tasks by status (PENDING/COMPLETED).
- Automated data validation using Pydantic.
- Global Exception Handling.
