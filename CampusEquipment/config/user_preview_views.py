
from django.conf import settings
from django.http import Http404
from django.shortcuts import render,redirect
from django.templatetags.static import static
from datetime import timedelta
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import date






def user_home_preview(request):
    if not settings.DEBUG:
        raise Http404()

    return redirect("browse_equipment_preview")






# ==========================================
# BASIC USER - SAMPLE EQUIPMENT DATA
# Preview only; NOT database records
# ==========================================

SAMPLE_USER_EQUIPMENT = [
    {
        "id": 1,
        "name": "Projector",
        "category": "Presentation Equipment",
        "description": (
            "HD projector with HDMI and VGA inputs, "
            "for classrooms and events."
        ),
        "image_url": static("images/projector.jpg"),
        "available_count": 3,
        "serviceable_count": 3,
        "is_active": True,
    },
    {
        "id": 2,
        "name": "Laptop",
        "category": "Computers",
        "description": "14-inch laptop with charger.",
        "image_url": static("images/laptop.jpg"),
        "available_count": 2,
        "serviceable_count": 4,
        "is_active": True,
    },
    {
        "id": 3,
        "name": "DSLR Camera",
        "category": "Photography",
        "description": (
            "DSLR camera with 18–55mm lens and bag."
        ),
        "image_url": static("images/camera.jpg"),
        "available_count": 1,
        "serviceable_count": 2,
        "is_active": True,
    },
    {
        "id": 4,
        "name": "Microscope",
        "category": "Laboratory",
        "description": (
            "Compound microscope (40x–1000x) "
            "for lab sessions."
        ),
        "image_url": static("images/miscroscope.jpg"),
        "available_count": 2,
        "serviceable_count": 2,
        "is_active": True,
    },
    {
        "id": 5,
        "name": "Speaker",
        "category": "Audio Equipment",
        "description": (
            "Audio equipment used for presentations, "
            "classroom activities, and school events."
        ),
        "image_url": static("images/speaker.jpg"),
        "available_count": 3,
        "serviceable_count": 4,
        "is_active": True,
    },
    {
        "id": 6,
        "name": "Wireless Microphone",
        "category": "Audio Equipment",
        "description": (
            "Wireless microphone for classroom "
            "presentations and events."
        ),
        "image_url": "",
        "available_count": 0,
        "serviceable_count": 1,
        "is_active": True,
    },
]





def browse_equipment_preview(request):
    if not settings.DEBUG:
        raise Http404()

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "all")

    if status_filter not in (
        "all",
        "in_stock",
        "out_of_stock",
    ):
        status_filter = "all"

    # Only active catalog items are browseable.
    equipment_items = [
        item.copy()
        for item in SAMPLE_USER_EQUIPMENT
        if item["is_active"]
    ]

    # Search equipment by name or category.
    if search_query:
        q = search_query.lower()

        equipment_items = [
            item
            for item in equipment_items
            if (
                q in item["name"].lower()
                or q in item["category"].lower()
            )
        ]

    # Stock status filtering.
    if status_filter == "in_stock":
        equipment_items = [
            item
            for item in equipment_items
            if item["available_count"] > 0
        ]

    elif status_filter == "out_of_stock":
        equipment_items = [
            item
            for item in equipment_items
            if item["available_count"] == 0
        ]

    # Availability progress percentage.
    for item in equipment_items:
        available = item["available_count"]
        serviceable = item["serviceable_count"]

        if serviceable > 0:
            percent = (available / serviceable) * 100
        else:
            percent = 0

        item["availability_percent"] = round(
            max(0, min(percent, 100))
        )

    return render(
        request,
        "user_pages/browse_equipment.html",
        {
            "equipment_items": equipment_items,
            "search_query": search_query,
            "status_filter": status_filter,
        },
    )



def user_new_request_preview(request):
    if not settings.DEBUG:
        raise Http404()

    # Preview settings only.
    # Backend will eventually read Admin Operational Settings.
    max_items = 3
    max_quantity = 5
    max_loan_days = 15

    today = timezone.localdate()
    latest_date = today + timedelta(days=max_loan_days)

    equipment_options = [
        item for item in SAMPLE_USER_EQUIPMENT
        if item["is_active"] and item["available_count"] > 0
    ]

    equipment_by_id = {
        str(item["id"]): item
        for item in equipment_options
    }

    selected_item_id = request.GET.get("item", "").strip()

    if selected_item_id not in equipment_by_id:
        selected_item_id = ""

    rows = [{
        "item_id": selected_item_id,
        "quantity": "1",
    }]

    return_date = ""
    purpose = ""
    message = ""
    validation_passed = False

    if request.method == "POST":
        action = request.POST.get("action", "validate")

        try:
            row_count = int(request.POST.get("row_count", "1"))
        except (TypeError, ValueError):
            row_count = 1

        # Never accept unlimited rows from a modified POST.
        row_count = max(1, min(row_count, max_items))

        rows = []

        for index in range(row_count):
            rows.append({
                "item_id": request.POST.get(
                    f"equipment_{index}", ""
                ).strip(),
                "quantity": request.POST.get(
                    f"quantity_{index}", "1"
                ).strip(),
            })

        return_date = request.POST.get(
            "desired_return_date", ""
        ).strip()

        purpose = request.POST.get(
            "purpose", ""
        )

        # ADD AN EQUIPMENT ROW
        if action == "add":
            if (
                len(rows) < max_items
                and len(rows) < len(equipment_options)
            ):
                rows.append({
                    "item_id": "",
                    "quantity": "1",
                })
            else:
                message = "Maximum of 3 different items allowed."

        # REMOVE EQUIPMENT ROW
        elif action.startswith("remove_"):
            try:
                remove_index = int(action.split("_", 1)[1])
            except (ValueError, IndexError):
                remove_index = -1

            if len(rows) > 1 and 0 <= remove_index < len(rows):
                rows.pop(remove_index)

        # RESET FORM
        elif action == "reset":
            rows = [{
                "item_id": selected_item_id,
                "quantity": "1",
            }]
            return_date = ""
            purpose = ""

        # VALIDATE SUBMISSION
        elif action == "validate":
            errors = []

            selected_ids = [
                row["item_id"]
                for row in rows
            ]

            if any(not item_id for item_id in selected_ids):
                errors.append(
                    "Select equipment for every item."
                )

            if len(set(selected_ids)) != len(selected_ids):
                errors.append(
                    "Each equipment item must be different."
                )

            for row in rows:
                item = equipment_by_id.get(row["item_id"])

                if item is None:
                    errors.append(
                        "One or more selected items are unavailable."
                    )
                    continue

                try:
                    quantity = int(row["quantity"])
                except (TypeError, ValueError):
                    errors.append(
                        "Enter a valid equipment quantity."
                    )
                    continue

                allowed = min(
                    max_quantity,
                    item["available_count"],
                )

                if quantity < 1 or quantity > allowed:
                    errors.append(
                        f"{item['name']}: choose 1 to "
                        f"{allowed} unit(s)."
                    )

            if not return_date:
                errors.append(
                    "Please select a desired return date."
                )
            else:
                try:
                    from datetime import date

                    chosen_date = date.fromisoformat(return_date)

                    if not today <= chosen_date <= latest_date:
                        errors.append(
                            "Return date must be within "
                            f"{max_loan_days} days from today."
                        )
                except ValueError:
                    errors.append(
                        "Please enter a valid return date."
                    )

            if not purpose.strip():
                errors.append(
                    "Please enter the borrowing purpose."
                )
            elif len(purpose.strip()) > 500:
                errors.append(
                    "Purpose must not exceed 500 characters."
                )

            if errors:
                message = " ".join(errors)
            else:
                validation_passed = True
                message = (
                    "Validation passed. This is a frontend "
                    "preview only. No borrowing request "
                    "has been saved or submitted."
                )

    return render(
        request,
        "user_pages/new_request.html",
        {
            "rows": rows,
            "equipment_options": equipment_options,
            "quantity_choices": range(1, max_quantity + 1),
            "max_quantity": max_quantity,
            "max_loan_days": max_loan_days,
            "min_date": today.isoformat(),
            "max_date": latest_date.isoformat(),
            "return_date": return_date,
            "purpose": purpose,
            "message": message,
            "validation_passed": validation_passed,
        },
    )

# ==========================================
# BASIC USER - MY REQUESTS PREVIEW
# Sample records only, NOT database records
# ==========================================

SAMPLE_MY_REQUESTS = [
    {
        "id": 1,
        "code": "R-001",
        "borrower_id": 1,
        "requested_date": "2026-10-04",
        "return_date": "2026-10-15",
        "status": "Approved",
        "purpose": "For classroom presentation.",
        "items": [
            {"name": "DSLR Camera", "quantity": 1},
        ],
        "reason": "",
    },
    {
        "id": 2,
        "code": "R-002",
        "borrower_id": 1,
        "requested_date": "2026-10-05",
        "return_date": "2026-10-18",
        "status": "Pending",
        "purpose": "Equipment for an academic activity.",
        "items": [
            {"name": "Projector", "quantity": 2},
            {"name": "Speaker", "quantity": 1},
        ],
        "reason": "",
    },
    {
        "id": 3,
        "code": "R-003",
        "borrower_id": 1,
        "requested_date": "2026-10-02",
        "return_date": "2026-10-10",
        "status": "Returned",
        "purpose": "For research and documentation.",
        "items": [
            {"name": "Laptop", "quantity": 1},
        ],
        "reason": "",
    },
    {
        "id": 4,
        "code": "R-004",
        "borrower_id": 1,
        "requested_date": "2026-10-02",
        "return_date": "2026-10-12",
        "status": "Cancelled",
        "purpose": "For laboratory demonstration.",
        "items": [
            {"name": "Microscope", "quantity": 1},
        ],
        "reason": "",
    },
    {
        "id": 5,
        "code": "R-005",
        "borrower_id": 1,
        "requested_date": "2026-10-03",
        "return_date": "2026-10-09",
        "status": "Rejected",
        "purpose": "For a school event.",
        "items": [
            {"name": "Speaker", "quantity": 1},
        ],
        "reason": "Insufficient available units for the requested period.",
    },
    {
        "id": 6,
        "code": "R-006",
        "borrower_id": 1,
        "requested_date": "2026-10-06",
        "return_date": "2026-10-20",
        "status": "Issued",
        "purpose": "For classroom activities.",
        "items": [
            {"name": "Projector", "quantity": 1},
        ],
        "reason": "",
    },
    {
        "id": 7,
        "code": "R-007",
        "borrower_id": 1,
        "requested_date": "2026-10-07",
        "return_date": "2026-10-21",
        "status": "Partially Returned",
        "purpose": "For a multimedia presentation.",
        "items": [
            {"name": "Laptop", "quantity": 1},
            {"name": "Projector", "quantity": 1},
            {"name": "Speaker", "quantity": 1},
        ],
        "reason": "",
    },
]

MY_REQUEST_STATUS_OPTIONS = [
    "Pending",
    "Approved",
    "Rejected",
    "Cancelled",
    "Issued",
    "Partially Returned",
    "Returned",
]


def my_requests_preview(request):
    if not settings.DEBUG:
        raise Http404()

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "all")

    if status_filter not in MY_REQUEST_STATUS_OPTIONS:
        status_filter = "all"

    # Preview: records belong to one fictional Basic User.
    # Final backend MUST query request.user,
    # not accept a borrower ID from the browser.
    demo_user_id = 1

    records = [
        record.copy()
        for record in SAMPLE_MY_REQUESTS
        if record["borrower_id"] == demo_user_id
    ]

    for record in records:
        record["can_cancel"] = record["status"] in (
            "Pending",
            "Approved",
        )

    if search_query:
        query = search_query.lower()

        records = [
            record
            for record in records
            if (
                query in record["code"].lower()
                or any(
                    query in item["name"].lower()
                    for item in record["items"]
                )
            )
        ]

    if status_filter != "all":
        records = [
            record
            for record in records
            if record["status"] == status_filter
        ]

    records.sort(
        key=lambda record: (
            record["requested_date"],
            record["id"],
        ),
        reverse=True,
    )

    paginator = Paginator(records, 5)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "user_pages/my_requests.html",
        {
            "page_obj": page_obj,
            "search_query": search_query,
            "status_filter": status_filter,
            "status_options": MY_REQUEST_STATUS_OPTIONS,
        },
    )

# ==========================================
# BASIC USER - MY LOANS PREVIEW
# Fictional data only
# ==========================================

SAMPLE_MY_LOANS = [
    {
        "id": 1,
        "code": "L-001",
        "request_code": "R-006",
        "borrower_id": 1,
        "release_date": date(2026, 10, 10),
        "due_date": date(2026, 10, 20),
        "units": [
            {
                "asset_code": "PRJ-003",
                "item_name": "Projector",
                "returned_date": None,
                "return_condition": "",
            },
        ],
    },
    {
        "id": 2,
        "code": "L-002",
        "request_code": "R-002",
        "borrower_id": 1,
        "release_date": date(2026, 10, 5),
        "due_date": date(2026, 10, 8),
        "units": [
            {
                "asset_code": "PRJ-004",
                "item_name": "Projector",
                "returned_date": date(2026, 10, 7),
                "return_condition": "Good",
            },
            {
                "asset_code": "PRJ-005",
                "item_name": "Projector",
                "returned_date": None,
                "return_condition": "",
            },
        ],
    },
    {
        "id": 3,
        "code": "L-003",
        "request_code": "R-003",
        "borrower_id": 1,
        "release_date": date(2026, 10, 9),
        "due_date": date(2026, 10, 11),
        "units": [
            {
                "asset_code": "LAP-005",
                "item_name": "Laptop",
                "returned_date": date(2026, 10, 10),
                "return_condition": "Good",
            },
        ],
    },
    {
        "id": 4,
        "code": "L-004",
        "request_code": "R-007",
        "borrower_id": 1,
        "release_date": date(2026, 10, 8),
        "due_date": date(2026, 10, 21),
        "units": [
            {
                "asset_code": "LAP-006",
                "item_name": "Laptop",
                "returned_date": date(2026, 10, 12),
                "return_condition": "Good",
            },
            {
                "asset_code": "SPK-007",
                "item_name": "Speaker",
                "returned_date": None,
                "return_condition": "",
            },
        ],
    },
]


def my_loans_preview(request):
    if not settings.DEBUG:
        raise Http404()

    today = timezone.localdate()

    status_options = [
        "Open",
        "Overdue",
        "Returned",
    ]

    status_filter = request.GET.get("status", "all")

    if status_filter not in status_options:
        status_filter = "all"

    # Demo user only.
    # Final backend: filter by authenticated user.
    demo_user_id = 1

    loans = []

    for sample in SAMPLE_MY_LOANS:
        if sample["borrower_id"] != demo_user_id:
            continue

        loan = sample.copy()

        # Count return and outstanding physical units.
        total_units = len(loan["units"])

        returned_count = sum(
            1
            for unit in loan["units"]
            if unit["returned_date"] is not None
        )

        outstanding_count = total_units - returned_count

        # Derive loan status from actual unit returns
        # and the current local date.
        if outstanding_count == 0:
            status = "Returned"

        elif loan["due_date"] < today:
            status = "Overdue"

        else:
            status = "Open"

        days_late = (
            max((today - loan["due_date"]).days, 0)
            if outstanding_count > 0
            else 0
        )

        # Aggregate physical units by equipment name.
        item_counts = {}

        for unit in loan["units"]:
            name = unit["item_name"]

            item_counts[name] = (
                item_counts.get(name, 0) + 1
            )

        items = [
            {
                "name": name,
                "quantity": quantity,
            }
            for name, quantity in item_counts.items()
        ]

        loan.update({
            "items": items,
            "total_units": total_units,
            "returned_count": returned_count,
            "outstanding_count": outstanding_count,
            "status": status,
            "days_late": days_late,
        })

        loans.append(loan)

    # Summary cards count the complete demo dataset,
    # not just the filtered/paginated table.
    stats = {
        "active": sum(
            1 for loan in loans
            if loan["status"] == "Open"
        ),
        "overdue": sum(
            1 for loan in loans
            if loan["status"] == "Overdue"
        ),
    }

    if status_filter != "all":
        loans = [
            loan
            for loan in loans
            if loan["status"] == status_filter
        ]

    # Newest released loans first.
    loans.sort(
        key=lambda loan: (
            loan["release_date"],
            loan["id"],
        ),
        reverse=True,
    )

    paginator = Paginator(loans, 5)

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "user_pages/my_loans.html",
        {
            "page_obj": page_obj,
            "stats": stats,
            "status_filter": status_filter,
            "status_options": status_options,
        },
    )

# ==========================================
# BASIC USER - PROFILE PREVIEW
# Fictional account data only
# ==========================================

SAMPLE_USER_PROFILE = {
    "full_name": "Ana Reyes",
    "contact_number": "09737237488",
    "email": "anareyes@gmail.com",
    "role": "Basic User",
    "account_status": "Active",
}


def user_profile_preview(request):
    if not settings.DEBUG:
        raise Http404()

    # Copy data so the preview source stays unchanged.
    profile = SAMPLE_USER_PROFILE.copy()

    message = ""
    validation_passed = False

    if request.method == "POST":
        full_name = request.POST.get(
            "full_name", ""
        ).strip()

        contact_number = request.POST.get(
            "contact_number", ""
        ).strip()

        # Show entered values again after POST.
        profile["full_name"] = full_name
        profile["contact_number"] = contact_number

        errors = []

        if not full_name:
            errors.append("Full name is required.")

        elif len(full_name) > 150:
            errors.append(
                "Full name must not exceed 150 characters."
            )

        # Contact number is optional in this preview.
        if contact_number:
            if (
                len(contact_number) != 11
                or not contact_number.startswith("09")
                or not contact_number.isascii()
                or not contact_number.isdigit()
            ):
                errors.append(
                    "Contact number must be an 11-digit "
                    "Philippine mobile number starting with 09."
                )

        if errors:
            message = " ".join(errors)

        else:
            validation_passed = True
            message = (
                "Profile information is valid. "
                "This is a frontend preview only. "
                "No changes have been saved to the database."
            )

    return render(
        request,
        "user_pages/profile.html",
        {
            "profile": profile,
            "message": message,
            "validation_passed": validation_passed,
        },
    )




