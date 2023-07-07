# KODY Website

![KODY Logo](website/static/images/kody_icon.jpg)

KODY is a website developed using Python Flask, designed to connect users who are looking for apartments to rent with agents who post available rental properties. This README provides an overview of the KODY website and outlines the necessary steps to set up and run the application.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Database](#database)
- [Models](#models)
- [Contributing](#contributing)
- [Authors](#authors)

## Features

- Users can search and browse available rental properties.
- Agents can post their rental properties on the website.
- User registration and login system.
- Contact agents via email for inquiries.
- User and property management.

## Installation

To install and set up the KODY website locally, follow these steps:

1. Clone the repository:

```
git clone https://github.com/your-username/kody.git
```

2. Navigate to the project directory:

```
cd KODY
```

3. Activate the virtual environment (recommended):

```
source kody_env/bin/activate
```

4. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

To run the KODY website locally, follow these steps:

1. Set the necessary environment variables. For example:

```
export FLASK_APP=main
```

```
export FLASK_ENV=development
```

2. Initialize the database:

```
flask db init
```

3. Apply the database migrations:

```
flask db migrate
```

```
flask db upgrade
```

4. Start the Flask development server:

```
flask run
```

5. Access the website in your browser at `http://localhost:5000`.

## Directory Structure

The directory structure of the KODY website is as follows:

```
KODY/
├── README.md
├── database.db
├── kody_env/
│   ├── bin/
│   ├── include/
│   ├── lib/
│   └── share/
├── main.py
└── website/
    ├── __init__.py
    ├── auth.py
    ├── models.py
    ├── schema.sql
    ├── static/
    │   ├── images/
    │   │   └── ...
    │   ├── scripts/
    │   │   └── ...
    │   └── styles/
    │       └── ...
    ├── templates/
    │   └── ...
    └── views.py
```

- The `main.py` file serves as the entry point of the Flask application.
- The `database.db` file is the SQLite database used by the application.
- The `website/` directory contains all the other files and templates for the website pages and the static files including images and styling files.
- The `schema.py` file contains the database schema and queries (do not run the file, only use for reference).
- The `models.py` file defines the User, Property, Bios, and Images classes, representing the database tables.
- The `auth.py` file creates the user, authenticate users and creates the necessary database tables.

## Database

The KODY website uses an SQLite database managed by Flask SQLAlchemy. The database file `database.db` is included in the project directory. To view the database schema and perform queries, refer to the `schema.py` file.

## Models

The KODY website utilizes the following models (representing database tables):

- `User`: Represents a user of the website, storing user information and authentication details.
- `Property`: Represents a rental property, containing details such as address, price, description, etc.
- `Bios`: Stores additional information about users or agents, including bios and contact information.
- `Images`: Stores images associated with rental properties.

These models are defined in the `models.py` file.

## Contributing

Contributions to the KODY website are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Submit a pull request detailing your changes.

---

## Authors

1. Winfred Kiarie - [Github](https://github.com/epicsociety).
2. Prisca Ndiritu - [Github](https://github.com/ndiritu-prisca).

Thank you for your interest in the KODY website! If you have any further questions or need assistance, please feel free to contact us.
