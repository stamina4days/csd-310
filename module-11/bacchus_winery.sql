-- ============================================================================
-- Course: CSD-310 Database Systems
-- Project: Bacchus Winery Database Script (Milestone #5) Version 4
-- Authors: Group C (Neosha Allen, Prince Hubbard, Nicholas Zankl)
-- Description: Complete 3NF relational database schema, tables, and sample 
--              data for Bacchus Winery procurement, production, labor, 
--              and distribution operations.
-- ============================================================================

DROP DATABASE IF EXISTS bacchus_winery;
CREATE DATABASE bacchus_winery;
USE bacchus_winery;

-- ----------------------------------------------------------------------------
-- 1. DEPARTMENTS
-- ----------------------------------------------------------------------------
CREATE TABLE DEPARTMENTS (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(50) NOT NULL UNIQUE
);

-- ----------------------------------------------------------------------------
-- 2. EMPLOYEES
-- ----------------------------------------------------------------------------
CREATE TABLE EMPLOYEES (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department_id INT NOT NULL,
    job_title VARCHAR(50) NOT NULL,
    FOREIGN KEY (department_id) REFERENCES DEPARTMENTS(department_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ----------------------------------------------------------------------------
-- 3. SUPPLIERS
-- ----------------------------------------------------------------------------
CREATE TABLE SUPPLIERS (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact_name VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- ----------------------------------------------------------------------------
-- 4. SUPPLIES
-- ----------------------------------------------------------------------------
CREATE TABLE SUPPLIES (
    supply_id INT AUTO_INCREMENT PRIMARY KEY,
    supply_name VARCHAR(100) NOT NULL,
    supply_type VARCHAR(50) NOT NULL, -- e.g., Bottles, Corks, Labels, Barrels
    unit_measure VARCHAR(20) NOT NULL
);

-- ----------------------------------------------------------------------------
-- 5. SUPPLY_ORDERS (Procurement Subsystem)
-- ----------------------------------------------------------------------------
CREATE TABLE SUPPLY_ORDERS (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT NOT NULL,
    supply_id INT NOT NULL,
    order_date DATE NOT NULL,
    expected_delivery_date DATE NOT NULL,
    actual_delivery_date DATE,
    quantity_ordered INT NOT NULL,
    FOREIGN KEY (supplier_id) REFERENCES SUPPLIERS(supplier_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (supply_id) REFERENCES SUPPLIES(supply_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ----------------------------------------------------------------------------
-- 6. TIMESHEETS (Payroll & Labor Subsystem)
-- ----------------------------------------------------------------------------
CREATE TABLE TIMESHEETS (
    timesheet_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    work_date DATE NOT NULL,
    hours_worked DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES EMPLOYEES(employee_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ----------------------------------------------------------------------------
-- 7. WINES
-- ----------------------------------------------------------------------------
CREATE TABLE WINES (
    wine_id INT AUTO_INCREMENT PRIMARY KEY,
    wine_name VARCHAR(100) NOT NULL,
    vintage YEAR NOT NULL,
    wine_type VARCHAR(50) NOT NULL
);

-- ----------------------------------------------------------------------------
-- 8. RECIPES (Added to match ERD)
-- ----------------------------------------------------------------------------
CREATE TABLE RECIPES (
    recipe_id INT AUTO_INCREMENT PRIMARY KEY,
    wine_id INT NOT NULL,
    supply_id INT NOT NULL,
    quantity_required DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (wine_id) REFERENCES WINES(wine_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (supply_id) REFERENCES SUPPLIES(supply_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ----------------------------------------------------------------------------
-- 9. DISTRIBUTORS
-- ----------------------------------------------------------------------------
CREATE TABLE DISTRIBUTORS (
    distributor_id INT AUTO_INCREMENT PRIMARY KEY,
    distributor_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- ----------------------------------------------------------------------------
-- 10. DISTRIBUTOR_ORDERS (Distribution Subsystem)
-- ----------------------------------------------------------------------------
CREATE TABLE DISTRIBUTOR_ORDERS (
    dist_order_id INT AUTO_INCREMENT PRIMARY KEY,
    distributor_id INT NOT NULL,
    wine_id INT NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE,
    cases_ordered INT NOT NULL,
    order_status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (distributor_id) REFERENCES DISTRIBUTORS(distributor_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (wine_id) REFERENCES WINES(wine_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- SEED DATA INSERTION
-- ============================================================================

-- Populate DEPARTMENTS
INSERT INTO DEPARTMENTS (department_id, department_name) VALUES
(1, 'Executive/Management'),
(2, 'Production'),
(3, 'Sales/Marketing'),
(4, 'Distribution');

-- Populate EMPLOYEES
INSERT INTO EMPLOYEES (employee_id, first_name, last_name, department_id, job_title) VALUES
(1, 'Stan', 'Bacchus', 1, 'Owner & General Manager'),
(2, 'Davis', 'Bacchus', 1, 'Co-Owner & Operations Lead'),
(3, 'Janet', 'Collins', 2, 'Head Winemaker'),
(4, 'Roz', 'Murphy', 3, 'Marketing Director'),
(5, 'Bob', 'Tyler', 4, 'Distribution Logistics Manager');

-- Populate SUPPLIERS
INSERT INTO SUPPLIERS (supplier_id, supplier_name, contact_name, phone, email) VALUES
(1, 'Oak Barrel Co.', 'John Smith', '555-0101', 'jsmith@oakbarrelco.com'),
(2, 'Cork & Closure Supply', 'Sarah Jenkins', '555-0102', 'sjenkins@corkclosure.com'),
(3, 'Glass & Bottle Inc.', 'Michael Brown', '555-0103', 'mbrown@glassbottle.com');

-- Populate SUPPLIES
INSERT INTO SUPPLIES (supply_id, supply_name, supply_type, unit_measure) VALUES
(1, 'French Oak Barrels', 'Barrels', 'Units'),
(2, 'Natural Wine Corks', 'Corks', 'Thousands'),
(3, '750ml Wine Bottles', 'Bottles', 'Cases');

-- Populate SUPPLY_ORDERS (Includes pending order 105 for Report 4 tracker)
INSERT INTO SUPPLY_ORDERS (order_id, supplier_id, supply_id, order_date, expected_delivery_date, actual_delivery_date, quantity_ordered) VALUES
(101, 1, 1, '2026-08-01', '2026-08-10', '2026-08-10', 50),
(102, 3, 3, '2026-08-05', '2026-08-15', '2026-08-18', 500),
(103, 2, 2, '2026-08-12', '2026-08-20', '2026-08-19', 100),
(104, 1, 1, '2026-09-01', '2026-09-10', '2026-09-15', 25),
(105, 3, 3, '2026-10-01', '2026-10-25', NULL, 250);

-- Populate TIMESHEETS
INSERT INTO TIMESHEETS (timesheet_id, employee_id, work_date, hours_worked) VALUES
(1, 1, '2026-07-15', 40.00),
(2, 2, '2026-07-15', 42.50),
(3, 3, '2026-07-15', 45.00),
(4, 4, '2026-07-15', 38.00),
(5, 5, '2026-07-15', 40.00),
(6, 3, '2026-08-15', 50.00),
(7, 5, '2026-08-15', 44.00);

-- Populate WINES
INSERT INTO WINES (wine_id, wine_name, vintage, wine_type) VALUES
(1, 'Bacchus Reserve Cabernet', 2022, 'Red'),
(2, 'Valley Chardonnay', 2023, 'White'),
(3, 'Estate Merlot', 2021, 'Red');

-- Populate RECIPES
INSERT INTO RECIPES (recipe_id, wine_id, supply_id, quantity_required) VALUES
(1, 1, 1, 1.00),
(2, 1, 2, 2.50),
(3, 1, 3, 50.00),
(4, 2, 2, 2.00),
(5, 2, 3, 50.00);

-- Populate DISTRIBUTORS
INSERT INTO DISTRIBUTORS (distributor_id, distributor_name, contact_person, phone, email) VALUES
(1, 'Apex Beverage Distributors', 'David Lee', '555-0201', 'dlee@apexbev.com'),
(2, 'Midwest Wine & Spirits', 'Laura Davis', '555-0202', 'ldavis@midwestwine.com');

-- Populate DISTRIBUTOR_ORDERS
INSERT INTO DISTRIBUTOR_ORDERS (dist_order_id, distributor_id, wine_id, order_date, ship_date, cases_ordered, order_status) VALUES
(501, 1, 1, '2026-08-10', '2026-08-12', 200, 'Shipped'),
(502, 2, 2, '2026-08-14', '2026-08-16', 150, 'Shipped'),
(503, 1, 3, '2026-09-01', NULL, 300, 'Pending');


-- ============================================================================
-- MANAGEMENT REPORTING QUERIES (Addressing Peer Feedback)
-- ============================================================================

-- 1. Supplier Delivery Performance & Variance Report (Michael Benko's feedback)
SELECT 
    s.supplier_name,
    so.order_id,
    su.supply_name,
    so.expected_delivery_date,
    so.actual_delivery_date,
    DATEDIFF(so.actual_delivery_date, so.expected_delivery_date) AS delivery_variance_days,
    CASE 
        WHEN DATEDIFF(so.actual_delivery_date, so.expected_delivery_date) > 0 THEN CONCAT('+', DATEDIFF(so.actual_delivery_date, so.expected_delivery_date), ' Days Late')
        WHEN DATEDIFF(so.actual_delivery_date, so.expected_delivery_date) < 0 THEN CONCAT(DATEDIFF(so.actual_delivery_date, so.expected_delivery_date), ' Days Early')
        ELSE 'On Time'
    END AS variance_status
FROM SUPPLY_ORDERS so
JOIN SUPPLIERS s ON so.supplier_id = s.supplier_id
JOIN SUPPLIES su ON so.supply_id = su.supply_id
WHERE so.actual_delivery_date IS NOT NULL;

-- 2. Pending-Order / Supply Delay Tracker (Brittany Smith's feedback)
SELECT 
    s.supplier_name,
    so.order_id,
    su.supply_name,
    so.order_date,
    so.expected_delivery_date,
    DATEDIFF(CURRENT_DATE(), so.expected_delivery_date) AS days_pending_or_overdue
FROM SUPPLY_ORDERS so
JOIN SUPPLIERS s ON so.supplier_id = s.supplier_id
JOIN SUPPLIES su ON so.supply_id = su.supply_id
WHERE so.actual_delivery_date IS NULL
ORDER BY so.expected_delivery_date ASC;