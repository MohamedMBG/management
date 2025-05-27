# Management System Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Database Models](#database-models)
4. [User Roles](#user-roles)
5. [Admin Panel](#admin-panel)
6. [Client Panel](#client-panel)
7. [Supervisor Panel](#supervisor-panel)
8. [Technical Implementation](#technical-implementation)
9. [Workflow Diagrams](#workflow-diagrams)

## Project Overview

The Management System is a comprehensive web application built with Django that facilitates inventory management, sales tracking, and user role management. The system is designed with three distinct user roles:

1. **Administrators**: Manage products, suppliers, supervisors, and view sales data
2. **Clients**: Browse products, make purchases, and view their purchase history
3. **Supervisors**: Monitor inventory levels, generate reports, and oversee client activities

This application provides a complete solution for businesses that need to track inventory, manage sales, and maintain different levels of access for various stakeholders.

## Project Structure

The project follows a standard Django structure with multiple apps, each responsible for specific functionality:

```
management/
├── admin_panel/         # Handles administrator functionality
├── client_panel/        # Handles client functionality
├── supervisor_panel/    # Handles supervisor functionality
├── stock/               # Main project settings and configuration
├── static/              # Static files (CSS, JavaScript, images)
├── media/               # User-uploaded files (product images)
├── templates/           # Shared templates
└── manage.py            # Django command-line utility
```

### Main Components

1. **stock**: The main Django project containing settings, URL configurations, and WSGI/ASGI configurations.

2. **admin_panel**: Manages administrator views, including product management, supplier management, and supervisor management.

3. **client_panel**: Handles client registration, product browsing, and purchase functionality.

4. **supervisor_panel**: Provides supervisors with tools to monitor inventory and generate reports.

5. **static**: Contains all static assets including CSS, JavaScript, and images used throughout the application.

6. **media**: Stores user-uploaded files, primarily product images.

## Database Models

The application uses several interconnected models to represent its data:

### Admin Panel Models

1. **Administrateur**: Links to Django's built-in User model to represent administrators.
   ```
   - user (OneToOneField to User)
   ```

2. **Fournisseur** (Supplier): Stores information about product suppliers.
   ```
   - nom (name)
   - telephone
   - email
   - adresse (address)
   ```

3. **Produit** (Product): Represents products in the inventory.
   ```
   - designation (name)
   - prix_unitaire (unit price)
   - quantite (quantity)
   - alert_quantite (alert threshold)
   - fournisseur (foreign key to Supplier)
   - image
   ```

4. **Achat** (Purchase): Records client purchases.
   ```
   - quantite (quantity)
   - client (foreign key to Client)
   - produit (foreign key to Product)
   - created_at (purchase date)
   ```

### Client Panel Models

1. **Client**: Extends the User model with additional client information.
   ```
   - user (OneToOneField to User)
   - email
   - telephone
   - adresse (address)
   ```

### Supervisor Panel Models

1. **Superviseur**: Extends the User model with supervisor-specific information.
   ```
   - user (OneToOneField to User)
   - telephone
   - adresse (address)
   - date_ajout (date added)
   ```

## User Roles

The system implements three distinct user roles, each with specific permissions and interfaces:

### Administrator

Administrators have the highest level of access and can:
- Manage products (add, edit, delete)
- Manage suppliers (add, edit, delete)
- Manage supervisors (add, edit, delete)
- View purchase records
- Monitor inventory levels

### Client

Clients are the end-users who can:
- Browse available products
- Make purchases
- View their purchase history
- Manage their profile information

### Supervisor

Supervisors have oversight capabilities and can:
- Monitor inventory levels
- Generate reports on sales and inventory
- View client purchase activities
- Track product performance

## Admin Panel

The Admin Panel provides administrators with a comprehensive interface to manage all aspects of the system.

### Key Features

1. **Dashboard**
   - Overview of system status
   - Low stock alerts
   - Recent purchase activity
   - Quick access to main functions

2. **Product Management**
   - Add new products with details and images
   - Edit existing product information
   - Delete products
   - View product details including stock levels

3. **Supplier Management**
   - Add new suppliers
   - Edit supplier information
   - View supplier details and associated products

4. **Supervisor Management**
   - Create supervisor accounts
   - Edit supervisor information
   - Delete supervisor accounts
   - View supervisor details

5. **Purchase Records**
   - View all purchases made by clients
   - Filter purchases by date, product, or client
   - View detailed purchase information

### Admin Workflow

1. Administrator logs in through the admin login page
2. Upon successful authentication, they are redirected to the admin dashboard
3. From the dashboard, they can navigate to different sections using the sidebar menu
4. They can perform CRUD operations on products, suppliers, and supervisors
5. They can view purchase records and monitor inventory levels

## Client Panel

The Client Panel provides a user-friendly interface for clients to browse products and make purchases.

### Key Features

1. **User Registration and Authentication**
   - Sign up for a new account
   - Log in to existing account
   - Update profile information

2. **Product Browsing**
   - View all available products
   - Filter products by various criteria
   - View detailed product information

3. **Purchase Functionality**
   - Add products to cart
   - Complete purchase process
   - View purchase confirmation

4. **Purchase History**
   - View history of all purchases
   - See details of past purchases

### Client Workflow

1. Client registers for an account or logs in to an existing account
2. They browse available products on the products page
3. They select products to purchase
4. They complete the purchase process
5. They can view their purchase history and account details

## Supervisor Panel

The Supervisor Panel provides tools for supervisors to monitor inventory and generate reports.

### Key Features

1. **Dashboard**
   - Overview of system status
   - Low stock alerts
   - Recent purchase activity

2. **Inventory Monitoring**
   - View current inventory levels
   - Identify products below alert threshold
   - Track inventory changes over time

3. **Reporting Tools**
   - Generate sales reports
   - Export data in various formats
   - Analyze sales trends

### Supervisor Workflow

1. Supervisor logs in through the supervisor login page
2. Upon successful authentication, they are redirected to the supervisor dashboard
3. From the dashboard, they can monitor inventory levels and purchase activity
4. They can generate reports on sales and inventory

## Technical Implementation

The Management System is built using the Django web framework, which follows the Model-View-Template (MVT) architectural pattern.

### Key Technologies

1. **Backend**
   - Django (Python web framework)
   - SQLite database (default)

2. **Frontend**
   - HTML/CSS
   - JavaScript
   - Bootstrap for responsive design

3. **Authentication**
   - Django's built-in authentication system
   - Custom user roles and permissions

### URL Structure

The application uses Django's URL routing system to direct requests to the appropriate views:

- `/admin_panel/` - Routes to administrator views
- `/client_panel/` - Routes to client views
- `/supervisor_panel/` - Routes to supervisor views

### Templates

The application uses Django's template system to render HTML pages:

1. **Admin Panel Templates**
   - Master page template for consistent layout
   - Dashboard template
   - Product management templates
   - Supplier management templates
   - Supervisor management templates
   - Purchase record templates

2. **Client Panel Templates**
   - Base template for consistent layout
   - Dashboard template
   - Product browsing templates
   - Purchase templates
   - Account management templates

3. **Supervisor Panel Templates**
   - Base template for consistent layout
   - Dashboard template
   - Reporting templates

## Workflow Diagrams

### User Authentication Flow

1. User navigates to login page
2. User enters credentials
3. System validates credentials
4. If valid, user is redirected to appropriate dashboard based on role
5. If invalid, error message is displayed

### Product Management Flow (Admin)

1. Admin navigates to product management page
2. Admin can view list of all products
3. Admin can add new product with details and image
4. Admin can edit existing product information
5. Admin can delete products
6. System updates inventory accordingly

### Purchase Flow (Client)

1. Client browses available products
2. Client selects products to purchase
3. Client confirms purchase
4. System records purchase and updates inventory
5. Client receives purchase confirmation

### Reporting Flow (Supervisor)

1. Supervisor navigates to reporting section
2. Supervisor selects report type and parameters
3. System generates report based on selected criteria
4. Supervisor can view report on screen or export it

## Conclusion

The Management System provides a comprehensive solution for inventory management, sales tracking, and user role management. With its three distinct user interfaces (Admin, Client, and Supervisor), it caters to the needs of different stakeholders while maintaining data integrity and security.

The system's modular design allows for easy maintenance and future expansion, making it a scalable solution for businesses of various sizes.
