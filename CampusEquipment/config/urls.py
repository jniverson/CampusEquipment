
from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView


# ==========================================
# MAIN URLS
# ==========================================

urlpatterns = [

    # LOGIN
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login.html"
        ),
        name="login",
    ),

    # REGISTER
    path(
        "register/",
        TemplateView.as_view(
            template_name="authentication/register.html"
        ),
        name="register",
    ),

    # LOGOUT
    path(
        "logout/",
        LogoutView.as_view(
            next_page="/"
        ),
        name="logout",
    ),

]


# ==========================================
# FRONTEND PREVIEW URLS
# DEBUG MODE ONLY
# ==========================================

if settings.DEBUG:

    from config.preview_views import (
        accounts_preview,
        account_history_preview,
        categories_preview,
        catalog_items_preview,
        physical_units_preview,
        request_queue_preview,
        request_details_preview,
        equipment_release_preview,
        returns_preview,
        maintenance_preview,
        reports_preview,
        reports_export_preview,
        operational_settings_preview,
        audit_logs_preview,
        dashboard_preview,

    )
    # BASIC USER PREVIEW VIEWS
    from config.user_preview_views import (
        user_home_preview,
        browse_equipment_preview,
        user_new_request_preview,
        my_requests_preview,
        my_loans_preview,
        user_profile_preview
    )

    urlpatterns += [

        # DASHBOARD
        path(
            "dashboard-preview/",
            dashboard_preview,
            name="dashboard_preview",
        ),

        # ACCOUNT MANAGEMENT
        path(
            "accounts-preview/",
            accounts_preview,
            name="accounts_preview",
        ),

        path(
            "accounts-preview/<int:account_id>/",
            account_history_preview,
            name="account_history_preview",
        ),

        # EQUIPMENT CATEGORIES
        path(
            "categories-preview/",
            categories_preview,
            name="categories_preview",
        ),

        # CATALOG ITEMS
        path(
            "catalog-items-preview/",
            catalog_items_preview,
            name="catalog_items_preview",
        ),

        # PHYSICAL UNITS
        path(
            "physical-units-preview/",
            physical_units_preview,
            name="physical_units_preview",
        ),

        # REQUEST QUEUE
        path(
            "request-queue-preview/",
            request_queue_preview,
            name="request_queue_preview",
        ),

        # REQUEST DETAILS
        path(
            "request-details-preview/<int:request_id>/",
            request_details_preview,
            name="request_details_preview",
        ),

        # EQUIPMENT RELEASE
        path(
            "equipment-release-preview/",
            equipment_release_preview,
            name="equipment_release_preview",
        ),

        # RETURNS & OVERDUE
        path(
            "returns-preview/",
            returns_preview,
            name="returns_preview",
        ),

        # EQUIPMENT MAINTENANCE
        path(
            "maintenance-preview/",
            maintenance_preview,
            name="maintenance_preview",
        ),

        # REPORTS
        path(
            "reports-preview/",
            reports_preview,
            name="reports_preview",
        ),

        # EXPORT REPORTS
        path(
            "reports-preview/export/<str:report_type>/",
            reports_export_preview,
            name="reports_export_preview",
        ),

        # OPERATIONAL SETTINGS
        path(
            "settings-preview/",
            operational_settings_preview,
            name="operational_settings_preview",
        ),

        # AUDIT LOGS
        path(
            "audit-logs-preview/",
            audit_logs_preview,
            name="audit_logs_preview",
        ),
        path(
            "user-preview/",
            user_home_preview,
            name="user_home_preview",
        ),

        # BASIC USER - BROWSE EQUIPMENT
        path(
            "browse-equipment-preview/",
            browse_equipment_preview,
            name="browse_equipment_preview",
        ),

        # BASIC USER - NEW REQUEST TEMPORARY PAGE
        path(
            "user-new-request-preview/",
            user_new_request_preview,
            name="user_new_request_preview",
        ),
        # BASIC USER - MY REQUESTS
        path(
            "my-requests-preview/",
            my_requests_preview,
            name="my_requests_preview",
        ),

        # BASIC USER - MY LOANS
        path(
            "my-loans-preview/",
            my_loans_preview,
            name="my_loans_preview",
        ),

        # BASIC USER - PROFILE
        path(
            "user-profile-preview/",
            user_profile_preview,
            name="user_profile_preview",
        ),

    ]
