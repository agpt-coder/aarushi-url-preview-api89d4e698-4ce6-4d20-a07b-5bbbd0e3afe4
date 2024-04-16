---
date: 2024-04-16T14:24:27.960432
author: AutoGPT <info@agpt.co>
---

# aarushi-url-preview-api

Based on the user's requirements for webpage content extraction and metadata retrieval, the task will involve creating an endpoint that accomplishes several key functions: it will accept a URL from the user, retrieve the webpage content at that URL, extract relevant metadata, generate a preview snippet that includes the page's title, description, and a thumbnail image, and return structured preview data for use in link sharing and embedding. The project will utilize a specific tech stack consisting of Python as the programming language, FastAPI for the API framework to ensure high performance and easy async tasks handling, PostgreSQL for the database to store and manage extracted metadata efficiently, and Prisma as the ORM for seamless database integration and querying. The process will include parsing the webpage content with robust tools capable of handling various content structures, including dynamic content loaded through JavaScript. For preview snippet generation, the system will extract metadata such as HTML <title>, <meta name='description'> tags, Open Graph, and Schema.org metadata. These extracted elements will form the basis of the preview snippet, which will be structured and returned in a uniform format suitable for embedding or link sharing on social platforms or other web applications. Best practices for content extraction and metadata retrieval that have been considered include the ethical scraping respecting robots.txt, utilizing HTML parsing libraries for content extraction, and performance optimization to provide high-quality previews while minimizing load on servers and target websites.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'aarushi-url-preview-api'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
