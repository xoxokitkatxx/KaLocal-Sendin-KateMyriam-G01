# KaLocal 

KaLocal is a web-based local product directory for barangays in Cebu City. It empowers residents to discover fresh goods, cooked food, and trusted sari-sari stores right in their own neighborhood.

## Current State of the Project (Phase 2)

This repository reflects Phase 2 of development. The codebase successfully implements the foundational **Account Feature** and our vertical slice **Core Feature**. Active features include:

- **Product Catalog Management (Core Feature):** Vendors can fully manage their catalog (Create, Read, Update, Delete product listings).
- Secure Registration and Login/Logout workflows.
- Profile viewing, editing, and account deletion.
- Role-based dashboards (Vendor and Consumer).
- Barangay-filtered product browsing. 
  *(Note: Text search, category chips, and consumer-to-vendor interaction buttons like "View Store" or "Message Vendor" are currently UI placeholders slated for upcoming phases).*

The user interface is fully responsive, built with **Bootstrap 5** (via CDN) and styled with a custom Filipino theme. 

## Core Feature: Product Catalog Management
The core functionality of KaLocal is the localized product directory. This vertical slice allows authorized **Vendors** to manage their digital storefronts through complete CRUD operations. 
* **Create:** Vendors can add new products (with names, prices, categories, and optional images).
* **Read:** Products dynamically render on the vendor's dashboard and the consumer's barangay directory.
* **Update:** Vendors can edit existing product details to keep inventory accurate.
* **Delete:** Vendors can permanently remove products from their catalog (with a safeguard confirmation step).
All data strictly persists to a PostgreSQL database, ensuring products are always tied directly to the vendor's assigned barangay.

## User Roles

1. **Local Vendor / Merchant (VENDOR):** Can create, read, update, and delete their own product listings. They can view their assigned barangay hub, manage their profile, and securely delete their account.
2. **Consumer (CONSUMER):** Can browse the directory, filter available products by specific barangays, manage their profile, and delete their account.

## Technology Stack

* **Backend & Frontend:** Full-Stack Django 6.1.3 (Django Templates for server-rendered UI)
* **Database:** PostgreSQL (Configured for local use by default, with Supabase support)
* **Styling:** Bootstrap 5 (CDN) + Custom CSS
* **Language:** Python 3.12+

## User Roles

1. **Local Vendor / Merchant (VENDOR):** Can view their product listings and assigned barangay, and manage their profile.
2. **Consumer (CONSUMER):** Can browse the directory and filter available products by barangay.

## Local Setup Instructions

Follow these steps to run the KaLocal project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/xoxokitkatxx/KaLocal-Sendin-KateMyriam-G01.git
cd KaLocal-Sendin-KateMyriam-G01
```

### 2. Set Up the Virtual Environment

Create and activate an isolated Python environment:

```bash
python -m venv venv

# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install all required packages from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

This project uses PostgreSQL and requires connection details to run. It defaults to a local PostgreSQL connection but can be easily pointed to a remote host like Supabase.

1. Create a new file in the root folder named `.env`.
2. Configure your database by providing the following `DB_*` environment variables:

```ini
SECRET_KEY=your-django-secret-key
DEBUG=True

# PostgreSQL Connection Variables
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost # Or your Supabase host URL
DB_PORT=5432
```

*(Note: Never commit your `.env` file to version control).*

### 5. Run Database Migrations

Apply the schema to your PostgreSQL database:

```bash
python manage.py migrate
```

### 6. Add Locations and Seed Mock Data

The seeding script requires existing barangays in the database to attach vendors and products to.

1. **Add Barangays:** Start the server, create a superuser (`python manage.py createsuperuser`), and log in to the Django Admin panel to manually create a few `Location` records (e.g., "Apas", "Lahug").
2. **Seed Data:** Once locations exist, run the seeding script:

```bash
python manage.py seed_data
```

*Note: This command generates mock vendors and products for **existing** locations. If the database has no locations, the script will exit with an error. For the new vendor accounts automatically created by this command, you can log in using the generated username (e.g., `vendor_apas`) and the password `KalocalVendor123!`. This password does not apply to any previously existing user accounts.*

### 7. Run the Development Server

Start the Django local server:

```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/` to access the application!
