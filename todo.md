# Todo List - Admin Login Redirect

- [x] Examine `templates/login.html` to understand the login form structure.
- [x] Examine user models (`django.contrib.auth.models.User` or custom models) to determine how admin status is identified (e.g., `is_staff` flag).
- [x] Implement authentication logic in `admin_panel/views.py`:
    - Handle POST requests.
    - Retrieve username/password.
    - Authenticate using `django.contrib.auth.authenticate` and `django.contrib.auth.login`.
    - Check if the logged-in user is an admin.
    - Redirect admin users to a dashboard URL (e.g., `/admin_panel/dashboard/`).
    - Redirect non-admin users appropriately (or show an error).
    - Handle invalid login credentials.
- [x] Define the dashboard URL pattern in `admin_panel/urls.py`.
- [x] Create a basic dashboard view in `admin_panel/views.py`.
- [x] Create a basic dashboard template (e.g., `templates/admin_dashboard.html`).
- [x] Test the login flow for admin users.
- [x] Test the login flow for non-admin users (if applicable).
- [x] Test invalid login attempts.
- [x] Commit changes to the repository (optional, based on user preference).
- [x] Report completion and provide updated code/instructions.
