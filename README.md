# PESU Nexus

> A student-built academic companion for PES University — mock tests, performance analytics, and study materials, all in one place.

![Django](https://img.shields.io/badge/Django-6.1-092E20?style=flat-square&logo=django)
![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

---

## 📖 Overview

**PESU Nexus** is a Django web app designed by students, for students at PES University. It centralizes the academic tools that are usually scattered across WhatsApp groups, Google Drive folders, and photocopied notes.

Students can take timed mock tests, review detailed performance analytics, and browse semester-wise study materials — all through a clean, dark-themed interface built for focus.

---

## ✨ Features

### 🧪 Mock Tests
- Browse tests by **semester** and **course**
- Take **timed, server-enforced** tests — attempts are recorded even if you navigate away
- Full **test analysis** page per attempt with question-by-question breakdown
- **Leaderboards** to compare performance with peers

### 📊 Performance Analytics
- **Score trend** line chart across all attempts
- **Answer breakdown** stacked bar chart (correct / wrong / skipped)
- Per-attempt **donut charts** with score percentage
- Summary stats: total tests, average score, personal best

### 📚 Study Materials
- Semester-wise → subject-wise → resource navigation
- Slide decks and course materials in a structured hierarchy

### 👤 User Accounts
- Registration, login, logout (Django auth)
- Per-user test history and analytics
- Admin panel for content management

### 🎨 UI/UX
- Custom dark theme with an accent-driven design system
- Cursor-follow glow effect
- Fully responsive layout
- Zero external CSS frameworks — hand-written, optimized CSS

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 6.1 |
| **Language** | Python 3.12+ |
| **Database** | PostgreSQL (hosted on Supabase) |
| **DB Connector** | `psycopg2-binary`, `dj-database-url` |
| **Static Files** | WhiteNoise |
| **Config** | `python-dotenv` |
| **Frontend Charts** | Chart.js 4.4 |
| **Fonts** | Inter (Google Fonts) |
| **Hosting** | *TBD — Render / Railway* |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- A **Supabase** account (free tier works fine)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/flyingmachine723/PESU-Nexus.git
cd PESU-Nexus