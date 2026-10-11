"""
Title: Bacchus Winery Management Reports v4
Assignment: CSD-310 Module 11.2 Milestone #5
Group: Group C
Authors: Neosha Allen, Prince Hubbard, and Nicholas Zankl
Date: October 11, 2026

This program connects to the Bacchus Winery MySQL/MariaDB database and
produces reports used to support purchasing, distribution, and labor
decisions, including supplier variance tracking and pending order monitoring.
"""

import getpass
import mysql.connector
from mysql.connector import Error

def main():
    print("==================================================")
    print("   Bacchus Winery - Management Reporting System   ")
    print("==================================================")
    
    # Prompt for MySQL root password securely
    db_password = getpass.getpass(prompt="Enter MySQL Root Password: ")

    # Database Connection Configuration
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': db_password,
        'database': 'bacchus_winery'
    }

    try:
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            print("\n[+] Successfully connected to Bacchus Winery Database.\n")
            
            cursor = conn.cursor()

            # -------------------------------------------------------------
            # REPORT 1: Supplier Delivery Performance Variance
            # -------------------------------------------------------------
            print("=====================================================================================================")
            print(" Report 1: Supplier Delivery Performance Variance")
            print("=====================================================================================================")
            query_report_1 = """
                SELECT 
                    s.supplier_name,
                    so.order_id,
                    so.order_date,
                    so.expected_delivery_date,
                    so.actual_delivery_date,
                    DATEDIFF(so.actual_delivery_date, so.expected_delivery_date) AS Delivery_Variance_Days,
                    CASE 
                        WHEN DATEDIFF(so.actual_delivery_date, so.expected_delivery_date) > 0 THEN CONCAT('+', DATEDIFF(so.actual_delivery_date, so.expected_delivery_date), ' Days Late')
                        WHEN DATEDIFF(so.actual_delivery_date, so.expected_delivery_date) < 0 THEN CONCAT(DATEDIFF(so.actual_delivery_date, so.expected_delivery_date), ' Days Early')
                        ELSE 'On Time'
                    END AS Variance_Status
                FROM supply_orders so
                JOIN suppliers s ON so.supplier_id = s.supplier_id
                WHERE so.actual_delivery_date IS NOT NULL
                ORDER BY so.order_date DESC;
            """
            cursor.execute(query_report_1)
            results_1 = cursor.fetchall()
            
            print(f"{'Supplier Name':<22} | {'Order ID':<8} | {'Order Date':<10} | {'Expected':<10} | {'Actual':<10} | {'Variance Status'}")
            print("-" * 101)
            for row in results_1:
                print(f"{str(row[0]):<22} | {str(row[1]):<8} | {str(row[2]):<10} | {str(row[3]):<10} | {str(row[4]):<10} | {str(row[6]):<18}")
            print("\n")

            # -------------------------------------------------------------
            # REPORT 2: Distributor Wine Shipments & Volume Summary
            # -------------------------------------------------------------
            print("=====================================================================================================")
            print(" Report 2: Distributor Wine Shipments & Volume Summary")
            print("=====================================================================================================")
            query_report_2 = """
                SELECT 
                    d.distributor_name,
                    do.dist_order_id,
                    do.ship_date,
                    w.wine_name,
                    do.cases_ordered,
                    do.order_status
                FROM distributor_orders do
                JOIN distributors d ON do.distributor_id = d.distributor_id
                JOIN wines w ON do.wine_id = w.wine_id
                ORDER BY do.ship_date DESC, d.distributor_name;
            """
            cursor.execute(query_report_2)
            results_2 = cursor.fetchall()

            print(f"{'Distributor Name':<25} | {'Order ID':<11} | {'Ship Date':<10} | {'Wine Type':<25} | {'Cases':<6} | {'Status'}")
            print("-" * 101)
            for row in results_2:
                # Fixed: display '-' instead of repeating 'Pending' in the Ship Date column
                ship_display = str(row[2]) if row[2] is not None else "-"
                print(f"{str(row[0]):<25} | {str(row[1]):<11} | {ship_display:<10} | {str(row[3]):<25} | {str(row[4]):<6} | {str(row[5]):<12}")
            print("\n")

            # -------------------------------------------------------------
            # REPORT 3: Department Quarterly Labor Aggregation (3NF Normalized)
            # -------------------------------------------------------------
            print("=====================================================================================================")
            print(" Report 3: Department Quarterly Labor Aggregation")
            print("=====================================================================================================")
            query_report_3 = """
                SELECT 
                    dept.department_name,
                    YEAR(t.work_date) AS work_year,
                    QUARTER(t.work_date) AS quarter_number,
                    COUNT(DISTINCT e.employee_id) AS total_employees,
                    SUM(t.hours_worked) AS total_hours_worked,
                    ROUND(SUM(t.hours_worked) / COUNT(DISTINCT e.employee_id), 2) AS avg_hours_per_employee
                FROM timesheets t
                JOIN employees e ON t.employee_id = e.employee_id
                JOIN departments dept ON e.department_id = dept.department_id
                GROUP BY dept.department_name, YEAR(t.work_date), QUARTER(t.work_date)
                ORDER BY dept.department_name, work_year DESC, quarter_number ASC;
            """
            cursor.execute(query_report_3)
            results_3 = cursor.fetchall()

            print(f"{'Department Name':<25} | {'Year':<6} | {'Quarter':<8} | {'Employees':<10} | {'Total Hours':<12} | {'Avg Hours'}")
            print("-" * 101)
            for row in results_3:
                print(f"{str(row[0]):<25} | {str(row[1]):<6} | {str(row[2]):<8} | {str(row[3]):<10} | {str(row[4]):<12} | {str(row[5]):<10}")
            print("\n")

            # -------------------------------------------------------------
            # REPORT 4: Pending-Order / Supply Delay Tracker
            # -------------------------------------------------------------
            print("=====================================================================================================")
            print(" Report 4: Pending-Order & Supply Delay Tracker")
            print("=====================================================================================================")
            query_report_4 = """
                SELECT 
                    s.supplier_name,
                    so.order_id,
                    su.supply_name,
                    so.expected_delivery_date
                FROM supply_orders so
                JOIN suppliers s ON so.supplier_id = s.supplier_id
                JOIN supplies su ON so.supply_id = su.supply_id
                WHERE so.actual_delivery_date IS NULL
                ORDER BY so.expected_delivery_date ASC;
            """
            cursor.execute(query_report_4)
            results_4 = cursor.fetchall()

            print(f"{'Supplier Name':<25} | {'Order ID':<8} | {'Supply Name':<25} | {'Expected Delivery'}")
            print("-" * 101)
            if results_4:
                for row in results_4:
                    print(f"{str(row[0]):<25} | {str(row[1]):<8} | {str(row[2]):<25} | {str(row[3]):<16}")
            else:
                print("No pending orders currently tracked.")
            print("\n")

            # Clean up connections
            cursor.close()
            conn.close()
            print("[+] Database connection closed successfully.")

    except Error as e:
        print(f"\nDatabase error: {e}")

if __name__ == "__main__":
    main()
