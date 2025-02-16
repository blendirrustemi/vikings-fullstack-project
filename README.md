# Vikings Fullstack Project

This is a fullstack web application built using Python and Flask that scrapes character data from the show *Vikings* and *Norsemen*. The app stores character details in a database and provides a web interface to view and search for characters by their name and actor.

---

## Features

- Scrapes character names, descriptions, and profile pictures from Wikipedia.
- Stores scraped data in a PostgreSQL database.
- Allows users to search for characters based on name and actor.
- Data updates automatically every 24 hours via a scheduler.
- Error handling for scraping failures and missing data.

---

## Getting Started

### Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.x
- pip (Python package installer)
  
You can install the dependencies using `pip`:
```bash
pip install -r requirements.txt
```

## Initializing and Configuring the Database
- When you first run the app, the database tables will be created automatically if they do not already exist. However, if you want to manually create the tables or initialize the database, you can add the table manually:

```bash
CREATE TABLE IF NOT EXISTS public."character"
(
    id integer NOT NULL DEFAULT nextval('character_id_seq'::regclass),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    actor character varying(150) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    photo_url character varying(500) COLLATE pg_catalog."default",
    character_url character varying(500) COLLATE pg_catalog."default",
    CONSTRAINT character_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."character"
    OWNER to blendirrustemi;
```


- In the config.py file, you'll find the configuration settings for connecting to the database. You’ll need to update the SQLALCHEMY_DATABASE_URI based on your configuration.

## Running the Application
### 1. Activate your virtual environment:

source new_venv/bin/activate  - on MacOS

new_venv\Scripts\activate     - On Windows

### 2. Run the Flask development server:
python3 run.py