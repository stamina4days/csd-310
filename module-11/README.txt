Bacchus Winery Project v4 README

1. (Included Files)
(a) Python Script: bacchus_reports.py — Automates secure database connection and generates terminal management reports. 
(b) SQL Script: bacchus_winery.sql — Contains the complete 3NF relational database schema, table creation DDL statements, and initial seed data. 
(c) PowerPoint Presentation: Group_C_Milestone_5_Presentation.pptx — The final presentation deck complete with speaker notes and structured summaries. 
(d) MySQL Workbench Model File: milestone5.mwb — The model archive file that allows you to skip straight to running the database and viewing/generating the ERD in your 	          own local MySQL instance. 
(e) PNG Images: fig1.png, fig2.png, fig3.png, fig4.png, fig5.png — High-resolution screenshots of the ERD workbench layout and terminal report outputs used across documentation. 
(f) Modification Document: Group_C_Milestone_5_Modifications.docx — Modification log detailing all structural updates, query refactoring, and peer feedback integration. 

2. (Prerequisites) Before running the scripts or database model, ensure your environment is prepared with the following:
•	MySQL Server / MariaDB: Installed and running locally to host the database. 
•	MySQL Workbench: Installed if you want to open the .mwb model file for ERD generation and visual review. 
•	Python (v3.8+): Installed and accessible via your command-line interface.
•	Python MySQL Connector: Required for the reporting script. Install it via terminal using: pip install mysql-connector-python
•	Project Files: Have all relevant Python and SQL script files handy in your local working directory.

3. (Populating Data via MySQL CLI) To initialize the database schema and populate all normalized tables and seed data using the command-line interface:
•	Open your terminal or command prompt.
•	Log into your MySQL server instance: mysql -u root -p . (NOTE: You HAVE to do this first before the script will be able to pull anything.)
•	Enter your MySQL root password when prompted.
•	Execute the SQL script using the SOURCE command (be sure to update the file path to match your local system): SOURCE /path/to/bacchus_winery.sql; Note: This script 	automatically drops any existing bacchus_winery database, recreates the schema, and populates all initial seed records. 

4.(Running the Python Script & Generating Output) To execute the reporting automation and view output reports:
•	Open your terminal or command prompt and navigate to the directory containing bacchus_reports.py.
•	Run the script using Python: python bacchus_reports.py
•	When prompted in the terminal, securely enter your local MySQL root password: Enter MySQL Root Password: 

5.The script will securely connect to your database, execute multi-table JOIN and aggregate queries, and print the following formatted reports directly to your terminal window: 
•	Report 1: Supplier Delivery Performance Variance (Delivery_Variance_Days). 
•	Report 2: Distributor Wine Shipments & Volume Summary (itemizing case counts and order statuses). 
•	Report 3: Department Quarterly Labor Aggregation (calculating distinct employee counts, total hours, and per-employee averages dynamically via YEAR() and QUARTER() 	functions). 
•	Report 4: Pending-Order & Supply Delay Tracker (monitoring outstanding purchase orders with unrecorded actual delivery dates).
