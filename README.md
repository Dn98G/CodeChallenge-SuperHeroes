## Code Challenge = Superheroes
# 🦸‍♂️ Superhero Powers API

This is a RESTful API built with **Flask**, **SQLAlchemy**, and **Flask-Migrate** that manages superheroes, their abilities, and the strengths of those abilities. It allows clients to retrieve, update, and link superheroes with their powers in a structured way.

---

## 🚀 Features

- List all superheroes and their aliases
- View a superhero's powers and strength details
- List all available powers
- Update a power's description
- Assign a power to a superhero with a strength level (`Strong`, `Average`, or `Weak`)
- Input validation and descriptive error responses
- Cascade delete behavior between related entities

---

## 🧱 Technologies Used

- Python 3.x
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-RESTful
- SQLite (default, easily replaceable via `DATABASE_URL`)

---

## 📦 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/superhero-api.git
cd superhero-api