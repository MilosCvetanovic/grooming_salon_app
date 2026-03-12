<div align="center">

<img src="static/images/logo.svg" alt="Project Logo" width="120" height="120" />

# grooming_salon_app

**This project is a sophisticated Grooming Salon Management System built with Django and Django REST Framework, featuring comprehensive user and dog profile management, a multi-step appointment booking workflow, an integrated review system for rating completed grooming services, and a full CRUD-based Loyalty Program API that tracks customer rewards and generates discount vouchers.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/github/actions/workflow/status/yourusername/projectname/ci.yml)](https://github.com/yourusername/projectname/actions)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[🚀 Live Demo](https://projectname.vercel.app) · [📖 Documentation](https://docs.projectname.dev) · [🐛 Report a Bug](https://github.com/yourusername/projectname/issues/new?template=bug_report.md) · [💡 Request a Feature](https://github.com/yourusername/projectname/issues/new?template=feature_request.md)

</div>

---

<!--
  ╔══════════════════════════════════════════════════════════╗
  ║  BEGINNER TIP: A README is the front door of your repo.  ║
  ║  Someone lands here and decides in ~10 seconds whether   ║
  ║  to keep reading or leave. Make every section count.     ║
  ╚══════════════════════════════════════════════════════════╝

  Delete all comments like this before publishing.
  They are here to guide you while writing.
-->

## Table of Contents

<!-- TIP: Keep this updated as you add/remove sections.
     GitHub renders anchor links automatically from headings. -->

- [About the Project](#about-the-project)
- [Built With](#built-with)
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

---

## About the Project

<!-- TIP: This is the most important section. If someone reads nothing else,
     they should understand the project from this alone. Answer three questions:
     1. What is the problem?
     2. What does this project do to solve it?
     3. Why is this better than other solutions? -->

Pet owners often face a fragmented and time-consuming process when trying to book grooming services. Managing pet profiles, tracking loyalty rewards across multiple visits, and finding available slots usually requires manual communication (phone calls or messages), which leads to double bookings, forgotten details about the pet's needs, and a lack of transparency regarding service quality.

This project provides a centralized, automated platform that streamlines the entire grooming journey. It offers:
- **A Multi-step Booking Engine**: Ensures all necessary data (service, groomer, pet, and time) is captured in one flow.
- **Pet Digital Cards**: Stores specific pet details and a high-quality personal photo for easy identification and style tracking.
- **Integrated Loyalty & Review Systems**: Automates reward tracking and builds trust through verified service ratings, all accessible via a modern REST API.

Unlike generic booking tools or manual ledger-keeping, this solution is purpose-built for the grooming industry. It combines specialized pet management with a dynamic loyalty program that is fully controlled by the user (CRUD functionality). By using a Django & DRF architecture, it offers superior data integrity, high security for user data, and the flexibility to be used as a backend for both web and mobile applications, ensuring a seamless experience across all devices.

**Key highlights:**

- 🚀 **Zero setup** — one install command, works immediately
- 🔒 **Privacy-first** — all data stored locally as plain JSON
- 📊 **Instant reports** — weekly/monthly summaries in your terminal
- 🧩 **Extensible** — add custom tags, clients, and rates per project
- ⚡ **Fast** — written in Python, starts in < 5ms

> **Note:** This project is under active development. Some features listed in the roadmap are not yet available. Check the [Roadmap](#roadmap) section for details.

---

## Built With

<!-- TIP: List every major technology/framework/library used.
     Link to their official sites. This helps people assess compatibility
     and also signals your tech choices upfront. -->

| Technology                                                            | Purpose       |
|-----------------------------------------------------------------------|---------------|
| [Python 3.14.3](https://www.python.org/)                              | Core language |
| [Django](https://www.djangoproject.com/)                              | Web framework |
| [Django Rest Framework (DRF)](https://www.django-rest-framework.org/) | REST APIs     |



---

## Getting Started

**1. Clone the repository and navigate into the project directory**
```bash
git clone https://github.com/MilosCvetanovic/grooming_salon_app.git

cd grooming_salon_app
```

**2. Open the project in IDE - PyCharm** *(recommended)*

**3. Install all required dependencies**
```bash
pip install -r requirements.txt
```

**4. Create, configure and connect to your PostgreSQL *(or other)* database**

- You can do it in pgAdmin or directly in your IDE.
- Save your credentials.

**5. Generate your Django secret key**

- Run the Django shell:
```bash
python manage.py shell
```
- Inside the shell, run the following Python code to import and call the function:
```python
from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())
```
- Save the Django secret key.

**6. Set up MailGun for email verification support**

- Create a free account at [mailgun.com](https://www.mailgun.com), generate an **API Key** and **Domain**, and **SAVE** them.


**7. Configure environment variables**

- Rename `.env.template` to `.env` and fill in all your credentials (including **saved data** from above).

**7. Apply database migrations**
```bash
python manage.py makemigrations

python manage.py migrate
```

**8. Load initial fixture data**
```bash
python manage.py loaddata services.json groomers.json notes.json groups.json
```

**9. Start the production server**
```bash
python manage.py runserver --insecure
```

- Application is available at → **http://localhost:8000**

---

## Prerequisites

<!-- TIP: This section should be so clear that someone with no knowledge
     of your project can get it running in under 5 minutes.
     Test it yourself on a fresh machine before publishing. -->

Before installing, make sure your environment meets these requirements:

- **Python** v3.14.3 or higher — [Download Go](https://www.python.org/)
  ```bash
  # Verify your Python version
  python --version
  # Should output: Python 3.14.3
  ```
- **Git** — [Download Git](https://git-scm.com/)
  ```bash
  git --version
  ```
  
- **PyCharm** v2025.3.3 — [Download PyCharm](https://www.jetbrains.com/pycharm/)

- **PostgreSQL** v18 2025, 2022— [Download PostgreSQL](https://www.postgresql.org/)

- **macOS / Linux / Windows** 

> **Don't have Python installed?** Follow the [official installation guide](https://docs.python.org/3/using/index.html) — it takes about 3 minutes.

---

## Project Structure

<!-- TIP: Include this section if your project has more than ~10 files.
     It helps contributors understand where to look for things.
     Only explain non-obvious folders/files. -->

```
grooming_salon/
.
├── grooming_salon/            # Project Root
│   ├── accounts/              # User Management (Custom User Model, Auth, Signals)
│   ├── common/                # Shared Components (Landing Page, Base)
│   ├── dogs/                  # Dog Management (Digital Dog Cards, Profiles)
│   ├── loyalty_api/           # REST API: Loyalty Rewards & Customer Points
│   ├── notifications_api/     # REST API: User Notifications
│   ├── reviews/               # Feedback System (Ratings & Service Reviews)
│   ├── services/              # Core Logic (Appointment Booking & Service Catalog)
│   ├── utils/                 # Project Configuration (Validators, Mixins, Utils)
│   ├── tests/                 # Project Tests (Organized by App)
│   ├── static/                # Global Assets (CSS, JavaScript, Fonts, Images)
│   ├── templates/             # HTML Templates (Organized by App)
│   └── media/                 # User-uploaded Content (Pet & Profile Photos)
│
├── .env                       # Environment Variables (Private - Not on Git)
├── .env.template              # Template for Environment Configuration
├── .gitignore                 # Instructions for Git to ignore specific files
├── manage.py                  # Django Management CLI
├── README.md                  # Project Documentation
└── requirements.txt           # Project Dependencies & Libraries
```

---



## Contact

<!-- TIP: Give people a clear way to reach you. At minimum, link to GitHub issues.
     You can also add email, Twitter/X, Discord, etc. -->

**Maintainer:** Miloš Cvetanović — [@MilosCvetanovic](https://github.com/MilosCvetanovic) — milos.cvetanovic07@gmail.com

**Project link:** [https://github.com/MilosCvetanovic/grooming_salon_app.git](https://github.com/MilosCvetanovic/grooming_salon_app.git)

**Bugs & features:** [Open an issue](https://github.com/MilosCvetanovic/grooming_salon_app/issues)

**General questions:** [Contact directly](https://github.com/MilosCvetanovic)

---

## Acknowledgements

<!-- TIP: Credit everyone who helped or inspired the project.
     It's good karma and it's good form. -->

- [SoftUni](https://softuni.rs/) — for the incredible 2 years of Full Stack Development journey — thank you 🙏🏻
- Everyone who has opened an issue, submitted a PR, or starred this repo — thank you ❤️

---

<div align="center">

If this project saved you time, consider giving it a ⭐ — it helps others find it!

**[⭐ Star on GitHub](https://github.com/yourusername/projectname)**

</div>