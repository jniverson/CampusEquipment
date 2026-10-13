# Campus Equipment Borrowing and Inventory System 

## Paano i-run (Windows)
1. Install Python 3.12+ mula sa python.org 
2. run in terminal
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```
   (Mac/Linux: `python3 -m venv .venv` at `source .venv/bin/activate`)
3. Open http://127.0.0.1:8000/ 

## Mga preview page 
Admin: /dashboard-preview/ /accounts-preview/ /categories-preview/ /catalog-items-preview/
/physical-units-preview/ /request-queue-preview/ /request-details-preview/5/ (pending)
/equipment-release-preview/ /returns-preview/ /maintenance-preview/ /reports-preview/
/settings-preview/ /audit-logs-preview/
User: /user-preview/ /browse-equipment-preview/ /user-new-request-preview/
/my-requests-preview/ /my-loans-preview/


