from django.conf import settings
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

# Fictional demonstration data only
SAMPLE_ACCOUNTS = [
    {
        "id": 1,
        "name": "Juan Dela Cruz",
        "email": "juan@example.com",
        "contact": "09000000001",
        "is_active": True,
        "request_count": 2,
        "history": [
            {
                "id": "REQ-001",
                "date": "2026-10-08",
                "items": "Projector x 1",
                "status": "Approved",
            },
            {
                "id": "REQ-002",
                "date": "2026-10-10",
                "items": "Speaker x 2",
                "status": "Pending",
            },
        ],
    },
    {
        "id": 2,
        "name": "Ana Reyes",
        "email": "ana@example.com",
        "contact": "09000000002",
        "is_active": True,
        "request_count": 2,
        "history": [
            {
                "id": "REQ-003",
                "date": "2026-10-07",
                "items": "Laptop x 1",
                "status": "Returned",
            },
            {
                "id": "REQ-004",
                "date": "2026-10-11",
                "items": "Camera x 1",
                "status": "Pending",
            },
        ],
    },
    {
        "id": 3,
        "name": "Ben Santos",
        "email": "ben@example.com",
        "contact": "",
        "is_active": False,
        "request_count": 0,
        "history": [],
    },
]


def require_preview_mode():
    if not settings.DEBUG:
        raise Http404()


def accounts_preview(request):
    require_preview_mode()

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "all")

    if status_filter not in ("all", "active", "inactive"):
        status_filter = "all"

    accounts = SAMPLE_ACCOUNTS

    if search_query:
        query = search_query.lower()
        accounts = [
            account for account in accounts
            if query in account["name"].lower()
            or query in account["email"].lower()
        ]

    if status_filter == "active":
        accounts = [
            account for account in accounts
            if account["is_active"]
        ]
    elif status_filter == "inactive":
        accounts = [
            account for account in accounts
            if not account["is_active"]
        ]

    paginator = Paginator(accounts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "admin_pages/accounts.html",
        {
            "accounts": page_obj,
            "page_obj": page_obj,
            "search_query": search_query,
            "status_filter": status_filter,
        },
    )


def account_history_preview(request, account_id):
    require_preview_mode()

    account = next(
        (
            user for user in SAMPLE_ACCOUNTS
            if user["id"] == account_id
        ),
        None,
    )

    if account is None:
        raise Http404("Account not found")

    return render(
        request,
        "admin_pages/account_detail.html",
        {
            "account": account,
            "history": account["history"],
        },
    )


# =====================================
# EQUIPMENT CATEGORIES PREVIEW
# =====================================

SAMPLE_CATEGORIES = [
    {
        "id": 1,
        "name": "Audio-Visual",
        "is_active": True,
        "item_count": 2,
    },
    {
        "id": 2,
        "name": "Computing",
        "is_active": True,
        "item_count": 3,
    },
    {
        "id": 3,
        "name": "Laboratory",
        "is_active": True,
        "item_count": 1,
    },
    {
        "id": 4,
        "name": "Old Equipment",
        "is_active": False,
        "item_count": 0,
    },
]


def categories_preview(request):
    require_preview_mode()

    status_filter = request.GET.get("status", "all")

    if status_filter not in ("all", "active", "archived"):
        status_filter = "all"

    categories = SAMPLE_CATEGORIES

    if status_filter == "active":
        categories = [
            c for c in categories if c["is_active"]
        ]

    elif status_filter == "archived":
        categories = [
            c for c in categories if not c["is_active"]
        ]

    return render(
        request,
        "admin_pages/equipment/categories.html",
        {
            "categories": categories,
            "status_filter": status_filter,
        },
    )

# =====================================
# CATALOG ITEMS PREVIEW
# Fictional demonstration data
# =====================================

SAMPLE_CATALOG_ITEMS = [
    {
        "id": 1,
        "name": "Projector",
        "category_id": 1,
        "category_name": "Audio-Visual",
        "description": "Portable multimedia projector.",
        "total_units": 4,
        "serviceable_units": 3,
        "available_units": 2,
        "is_active": True,
        "image": "images/projector.jpg",
    },
    {
        "id": 2,
        "name": "Laptop",
        "category_id": 2,
        "category_name": "Computing",
        "description": "Laptop for academic activities.",
        "total_units": 3,
        "serviceable_units": 3,
        "available_units": 2,
        "is_active": True,
        "image": "images/laptop.jpg",
    },
    {
        "id": 3,
        "name": "Microscope",
        "category_id": 3,
        "category_name": "Laboratory",
        "description": "Laboratory microscope.",
        "total_units": 3,
        "serviceable_units": 2,
        "available_units": 1,
        "is_active": True,
        "image": "images/miscroscope.jpg",
    },
    {
        "id": 4,
        "name": "Camera",
        "category_id": 1,
        "category_name": "Audio-Visual",
        "description": "Digital camera for campus use.",
        "total_units": 3,
        "serviceable_units": 3,
        "available_units": 1,
        "is_active": True,
        "image": "images/camera.jpg",
    },
    {
        "id": 5,
        "name": "Speaker",
        "category_id": 1,
        "category_name": "Audio-Visual",
        "description": "Portable audio speaker.",
        "total_units": 3,
        "serviceable_units": 3,
        "available_units": 2,
        "is_active": True,
        "image": "images/speaker.jpg",
    },
    {
        "id": 6,
        "name": "Tablet",
        "category_id": 2,
        "category_name": "Computing",
        "description": "Tablet for classroom activities.",
        "total_units": 2,
        "serviceable_units": 2,
        "available_units": 2,
        "is_active": False,
        "image": "",
    },
]


def catalog_items_preview(request):
    require_preview_mode()

    selected_category = request.GET.get("category", "all")
    selected_item = request.GET.get("item", "all")
    status_filter = request.GET.get("status", "all")

    if status_filter not in ("all", "active", "archived"):
        status_filter = "all"

    valid_category_ids = {
        str(c["id"]) for c in SAMPLE_CATEGORIES
    }
    valid_item_ids = {
        str(i["id"]) for i in SAMPLE_CATALOG_ITEMS
    }

    if selected_category not in valid_category_ids:
        selected_category = "all"

    if selected_item not in valid_item_ids:
        selected_item = "all"

    items = SAMPLE_CATALOG_ITEMS

    if selected_category != "all":
        items = [
            i for i in items
            if str(i["category_id"]) == selected_category
        ]

    if selected_item != "all":
        items = [
            i for i in items
            if str(i["id"]) == selected_item
        ]

    if status_filter == "active":
        items = [
            i for i in items if i["is_active"]
        ]
    elif status_filter == "archived":
        items = [
            i for i in items if not i["is_active"]
        ]

    return render(
        request,
        "admin_pages/equipment/catalog_items.html",
        {
            "items": items,
            "all_items": SAMPLE_CATALOG_ITEMS,
            "categories": SAMPLE_CATEGORIES,
            "selected_category": selected_category,
            "selected_item": selected_item,
            "status_filter": status_filter,
        },
    )

# =====================================
# PHYSICAL UNITS PREVIEW DATA
# =====================================

SAMPLE_PHYSICAL_UNITS = [
    {
        "id": 1,
        "asset_code": "PRJ-001",
        "item_id": 1,
        "item_name": "Projector",
        "category_id": 1,
        "category_name": "Audio-Visual",
        "condition": "Good",
        "acquired": "2025-08-01",
        "acquired_iso": "2025-08-01",
        "status": "Available",
    },
    {
        "id": 2,
        "asset_code": "PRJ-002",
        "item_id": 1,
        "item_name": "Projector",
        "category_id": 1,
        "category_name": "Audio-Visual",
        "condition": "Good",
        "acquired": "2025-08-01",
        "acquired_iso": "2025-08-01",
        "status": "Available",
    },
    {
        "id": 3,
        "asset_code": "LAP-001",
        "item_id": 2,
        "item_name": "Laptop",
        "category_id": 2,
        "category_name": "Computing",
        "condition": "Good",
        "acquired": "2025-08-01",
        "acquired_iso": "2025-08-01",
        "status": "Issued",
    },
    {
        "id": 4,
        "asset_code": "LAP-002",
        "item_id": 2,
        "item_name": "Laptop",
        "category_id": 2,
        "category_name": "Computing",
        "condition": "Good",
        "acquired": "2025-08-01",
        "acquired_iso": "2025-08-01",
        "status": "Reserved",
    },
    {
        "id": 5,
        "asset_code": "MIC-001",
        "item_id": 3,
        "item_name": "Microscope",
        "category_id": 3,
        "category_name": "Laboratory",
        "condition": "Damaged",
        "acquired": "2025-08-01",
        "acquired_iso": "2025-08-01",
        "status": "Maintenance",
    },
    {
        "id": 6,
        "asset_code": "CAM-001",
        "item_id": 4,
        "item_name": "Camera",
        "category_id": 1,
        "category_name": "Audio-Visual",
        "condition": "Good",
        "acquired": "2025-08-01",
        "acquired_iso": "2025-08-01",
        "status": "Available",
    },
    {
        "id": 7,
        "asset_code": "CAM-002",
        "item_id": 4,
        "item_name": "Camera",
        "category_id": 1,
        "category_name": "Audio-Visual",
        "condition": "Fair",
        "acquired": "2025-08-01",
        "acquired_iso": "2025-08-01",
        "status": "Retired",
    },
]

INVENTORY_STATUSES = [
    "Available",
    "Reserved",
    "Issued",
    "Maintenance",
    "Retired",
]


def physical_units_preview(request):
    require_preview_mode()

    selected_category = request.GET.get(
        "category", "all"
    )
    selected_item = request.GET.get(
        "item", "all"
    )
    status_filter = request.GET.get(
        "status", "all"
    )

    valid_categories = {
        str(c["id"]) for c in SAMPLE_CATEGORIES
    }
    valid_items = {
        str(i["id"]) for i in SAMPLE_CATALOG_ITEMS
    }

    if selected_category not in valid_categories:
        selected_category = "all"

    if selected_item not in valid_items:
        selected_item = "all"

    if status_filter not in INVENTORY_STATUSES:
        status_filter = "all"

    units = SAMPLE_PHYSICAL_UNITS

    if selected_category != "all":
        units = [
            u for u in units
            if str(u["category_id"]) == selected_category
        ]

    if selected_item != "all":
        units = [
            u for u in units
            if str(u["item_id"]) == selected_item
        ]

    if status_filter != "all":
        units = [
            u for u in units
            if u["status"] == status_filter
        ]

    return render(
        request,
        "admin_pages/equipment/physical_units.html",
        {
            "units": units,
            "categories": SAMPLE_CATEGORIES,
            "catalog_items": SAMPLE_CATALOG_ITEMS,
            "inventory_statuses": INVENTORY_STATUSES,
            "selected_category": selected_category,
            "selected_item": selected_item,
            "status_filter": status_filter,
        },
    )


# ==========================================
# A3 - REQUEST REVIEW & APPROVAL PREVIEW
# Fictional demonstration data only
# ==========================================

SAMPLE_BORROW_REQUESTS = [
    {
        "id": 1,
        "code": "R-001",
        "borrower": "Juan Dela Cruz",
        "request_date": "2026-10-10",
        "return_date": "2026-10-16",
        "status": "Pending",
        "purpose": "Classroom presentation.",
        "items": [
            {
                "id": 1,
                "name": "Projector",
                "quantity": 1,
                "available": 2,
                "units": [
                    {
                        "code": "PRJ-001",
                        "condition": "Good",
                    },
                    {
                        "code": "PRJ-002",
                        "condition": "Good",
                    },
                ],
                "allocated_codes": [],
            },
            {
                "id": 2,
                "name": "Speaker",
                "quantity": 2,
                "available": 3,
                "units": [
                    {
                        "code": "SPK-001",
                        "condition": "Good",
                    },
                    {
                        "code": "SPK-002",
                        "condition": "Good",
                    },
                    {
                        "code": "SPK-003",
                        "condition": "New",
                    },
                ],
                "allocated_codes": [],
            },
        ],
        "decision_date": "",
        "decision_reason": "",
        "reviewed_by": "",
    },
    {
        "id": 2,
        "code": "R-002",
        "borrower": "Ana Reyes",
        "request_date": "2026-10-09",
        "return_date": "2026-10-14",
        "status": "Approved",
        "purpose": "Campus seminar.",
        "items": [
            {
                "id": 3,
                "name": "Laptop",
                "quantity": 1,
                "available": 1,
                "units": [],
                "allocated_codes": ["LAP-002"],
            },
        ],
        "decision_date": "2026-10-09",
        "decision_reason": "Approved for academic use.",
        "reviewed_by": "Demo Admin",
    },
    {
        "id": 3,
        "code": "R-003",
        "borrower": "Ben Santos",
        "request_date": "2026-10-08",
        "return_date": "2026-10-13",
        "status": "Issued",
        "purpose": "Research activity.",
        "items": [
            {
                "id": 4,
                "name": "Microscope",
                "quantity": 1,
                "available": 0,
                "units": [],
                "allocated_codes": ["MIC-002"],
            },
        ],
        "decision_date": "2026-10-08",
        "decision_reason": "Approved for research.",
        "reviewed_by": "Demo Admin",
        "loan": {
            "issued_at": "2026-10-09",
            "released_by": "Demo Admin",
            "due_date": "2026-10-13",
        },
    },
    {
        "id": 4,
        "code": "R-004",
        "borrower": "Juan Dela Cruz",
        "request_date": "2026-10-07",
        "return_date": "2026-10-12",
        "status": "Rejected",
        "purpose": "Outdoor event.",
        "items": [
            {
                "id": 5,
                "name": "Camera",
                "quantity": 2,
                "available": 1,
                "units": [],
                "allocated_codes": [],
            },
        ],
        "decision_date": "2026-10-07",
        "decision_reason": "Insufficient available units.",
        "reviewed_by": "Demo Admin",
    },
    {
        "id": 5,
        "code": "R-005",
        "borrower": "Ana Reyes",
        "request_date": "2026-10-11",
        "return_date": "2026-10-17",
        "status": "Pending",
        "purpose": "Classroom activity and campus project.",
        "items": [
            {
                "id": 6,
                "name": "Laptop",
                "quantity": 1,
                "available": 1,
                "units": [
                    {
                        "code": "LAP-003",
                        "condition": "Good",
                    },
                ],
                "allocated_codes": [],
            },
        ],
        "decision_date": "",
        "decision_reason": "",
        "reviewed_by": "",
    },
    {
        "id": 6,
        "code": "R-006",
        "borrower": "Ben Santos",
        "request_date": "2026-10-06",
        "return_date": "2026-10-12",
        "status": "Cancelled",
        "purpose": "Laboratory exercise.",
        "items": [
            {
                "id": 7,
                "name": "Projector",
                "quantity": 1,
                "available": 2,
                "units": [],
                "allocated_codes": [],
            },
        ],
        "decision_date": "",
        "decision_reason": "Cancelled by borrower.",
        "reviewed_by": "",
    },
    {
        "id": 7,
        "code": "R-007",
        "borrower": "Maria Garcia",
        "request_date": "2026-10-05",
        "return_date": "2026-10-11",
        "status": "Partially Returned",
        "purpose": "School event.",
        "items": [
            {
                "id": 8,
                "name": "Speaker",
                "quantity": 2,
                "available": 0,
                "units": [],
                "allocated_codes": [
                    "SPK-004",
                    "SPK-005",
                ],
                "return_records": [
                    {
                        "asset_code": "SPK-004",
                        "returned_at": "2026-10-10",
                        "condition": "Good",
                    },
                    {
                        "asset_code": "SPK-005",
                        "returned_at": "",
                        "condition": "",
                    },
                ],
            },
        ],
        "decision_date": "2026-10-05",
        "decision_reason": "Approved for school event.",
        "reviewed_by": "Demo Admin",
        "loan": {
            "issued_at": "2026-10-06",
            "released_by": "Demo Admin",
            "due_date": "2026-10-11",
        },
    },
    {
        "id": 8,
        "code": "R-008",
        "borrower": "Maria Garcia",
        "request_date": "2026-10-01",
        "return_date": "2026-10-06",
        "status": "Returned",
        "purpose": "Academic presentation.",
        "items": [
            {
                "id": 9,
                "name": "Projector",
                "quantity": 1,
                "available": 2,
                "units": [],
                "allocated_codes": ["PRJ-003"],
                "return_records": [
                    {
                        "asset_code": "PRJ-003",
                        "returned_at": "2026-10-06",
                        "condition": "Good",
                    },
                ],
            },
        ],
        "decision_date": "2026-10-01",
        "decision_reason": "Approved for presentation.",
        "reviewed_by": "Demo Admin",
        "loan": {
            "issued_at": "2026-10-02",
            "released_by": "Demo Admin",
            "due_date": "2026-10-06",
        },
    },
]


REQUEST_STATUS_OPTIONS = [
    "Pending",
    "Approved",
    "Rejected",
    "Cancelled",
    "Issued",
    "Partially Returned",
    "Returned",
]


def request_queue_preview(request):
    require_preview_mode()

    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "all")
    selected_date = request.GET.get("date", "")

    if status not in REQUEST_STATUS_OPTIONS:
        status = "all"

    records = SAMPLE_BORROW_REQUESTS

    if query:
        text = query.lower()

        records = [
            record for record in records
            if (
                text in record["code"].lower()
                or text in record["borrower"].lower()
                or any(
                    text in item["name"].lower()
                    for item in record["items"]
                )
            )
        ]

    if status != "all":
        records = [
            record for record in records
            if record["status"] == status
        ]

    if selected_date:
        records = [
            record for record in records
            if record["request_date"] == selected_date
        ]

    records = sorted(
        records,
        key=lambda record: record["request_date"],
        reverse=True,
    )

    paginator = Paginator(records, 4)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "admin_pages/request/request_queue.html",
        {
            "requests": page_obj,
            "page_obj": page_obj,
            "search_query": query,
            "status_filter": status,
            "selected_date": selected_date,
            "status_options": REQUEST_STATUS_OPTIONS,
        },
    )


def request_details_preview(request, request_id):
    require_preview_mode()

    borrowing = next(
        (
            record for record in SAMPLE_BORROW_REQUESTS
            if record["id"] == request_id
        ),
        None,
    )

    if borrowing is None:
        raise Http404("Request not found.")

    return render(
        request,
        "admin_pages/request/request_details.html",
        {
            "borrowing": borrowing,
        },
    )

# ==========================================
# A4 - EQUIPMENT RELEASE PREVIEW
# Fictional demonstration data only
# ==========================================

def equipment_release_preview(request):
    require_preview_mode()

    # Find approved requests with complete allocations.
    approved_requests = []

    for borrowing in SAMPLE_BORROW_REQUESTS:

        if borrowing["status"] != "Approved":
            continue

        items = borrowing.get("items", [])

        if not items:
            continue

        fully_allocated = all(
            item["quantity"] > 0
            and len(item.get("allocated_codes", []))
            == item["quantity"]
            for item in items
        )

        # Preview-only cross-check against sample
        # physical-unit inventory, when available.
        allocated_codes = [
            code
            for item in items
            for code in item.get("allocated_codes", [])
        ]

        no_duplicates = (
            len(allocated_codes) == len(set(allocated_codes))
        )

        units_by_code = {
            unit["asset_code"]: unit
            for unit in SAMPLE_PHYSICAL_UNITS
        }

        units_reserved = all(
            units_by_code.get(code, {}).get("status")
            == "Reserved"
            for code in allocated_codes
        )

        if fully_allocated and no_duplicates and units_reserved:
            approved_requests.append(borrowing)

    # Build fictional loan preview records from requests
    # with an existing release history.
    loan_records = []

    for borrowing in SAMPLE_BORROW_REQUESTS:

        if borrowing["status"] not in (
            "Issued",
            "Partially Returned",
            "Returned",
        ):
            continue

        loan = borrowing.get("loan")

        if not loan:
            continue

        loan_records.append({
            "id": borrowing["id"],
            "code": f"L-{borrowing['id']:03d}",
            "request_code": borrowing["code"],
            "borrower": borrowing["borrower"],
            "release_date": loan.get("issued_at", ""),
            "due_date": loan.get("due_date", ""),
            "released_by": loan.get("released_by", ""),
            "status": borrowing["status"],
            "items": borrowing["items"],
        })

    loan_records.sort(
        key=lambda loan: loan["release_date"],
        reverse=True,
    )

    paginator = Paginator(loan_records, 5)

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "admin_pages/release/equipment_release.html",
        {
            "approved_requests": approved_requests,
            "loans": page_obj,
            "page_obj": page_obj,
        },
    )

# ==========================================
# A5 - RETURNS & OVERDUE PREVIEW
# ==========================================

from datetime import date
from django.utils import timezone

SAMPLE_RETURN_LOANS = [
    {
        "id": 1,
        "code": "L-001",
        "borrower": "Juan Dela Cruz",
        "release_date": "2026-10-05",
        "due_date": "2026-10-10",
        "units": [
            {
                "asset_code": "LAP-001",
                "item_name": "Laptop",
                "returned_at": "2026-10-09",
                "condition": "Good",
            },
            {
                "asset_code": "CAM-002",
                "item_name": "Camera",
                "returned_at": "",
                "condition": "",
            },
        ],
    },
    {
        "id": 2,
        "code": "L-002",
        "borrower": "Ana Reyes",
        "release_date": "2026-10-08",
        "due_date": "2026-10-20",
        "units": [
            {
                "asset_code": "PRJ-004",
                "item_name": "Projector",
                "returned_at": "",
                "condition": "",
            },
            {
                "asset_code": "SPK-006",
                "item_name": "Speaker",
                "returned_at": "",
                "condition": "",
            },
        ],
    },
    {
        "id": 3,
        "code": "L-003",
        "borrower": "Ben Santos",
        "release_date": "2026-10-09",
        "due_date": "2026-10-22",
        "units": [
            {
                "asset_code": "MIC-002",
                "item_name": "Microscope",
                "returned_at": "",
                "condition": "",
            },
        ],
    },
    {
        "id": 4,
        "code": "L-004",
        "borrower": "Maria Garcia",
        "release_date": "2026-10-01",
        "due_date": "2026-10-07",
        "units": [
            {
                "asset_code": "LAP-005",
                "item_name": "Laptop",
                "returned_at": "2026-10-06",
                "condition": "Good",
            },
        ],
    },
    {
        "id": 5,
        "code": "L-005",
        "borrower": "Ana Reyes",
        "release_date": "2026-10-10",
        "due_date": "2026-10-25",
        "units": [
            {
                "asset_code": "CAM-004",
                "item_name": "Camera",
                "returned_at": "",
                "condition": "",
            },
        ],
    },
]


RETURN_STATUS_OPTIONS = [
    "Open",
    "Overdue",
    "Returned",
]


def returns_preview(request):
    require_preview_mode()

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "all")

    if status_filter not in RETURN_STATUS_OPTIONS:
        status_filter = "all"

    today = timezone.localdate()
    records = []

    for source in SAMPLE_RETURN_LOANS:
        loan = source.copy()

        total_count = len(loan["units"])
        outstanding_count = sum(
            1 for unit in loan["units"]
            if not unit["returned_at"]
        )

        due_date = date.fromisoformat(loan["due_date"])

        if outstanding_count == 0:
            display_status = "Returned"
        elif due_date < today:
            display_status = "Overdue"
        else:
            display_status = "Open"

        loan["total_count"] = total_count
        loan["outstanding_count"] = outstanding_count
        loan["display_status"] = display_status

        records.append(loan)

    if search_query:
        text = search_query.lower()

        records = [
            loan for loan in records
            if text in loan["code"].lower()
            or text in loan["borrower"].lower()
        ]

    if status_filter != "all":
        records = [
            loan for loan in records
            if loan["display_status"] == status_filter
        ]

    records.sort(
        key=lambda loan: loan["release_date"],
        reverse=True,
    )

    paginator = Paginator(records, 5)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "admin_pages/returns/returns.html",
        {
            "loans": page_obj,
            "page_obj": page_obj,
            "search_query": search_query,
            "status_filter": status_filter,
            "status_options": RETURN_STATUS_OPTIONS,
        },
    )

# ==========================================
# A6 - EQUIPMENT MAINTENANCE PREVIEW
# ==========================================

SAMPLE_MAINTENANCE_RECORDS = [
    {
        "id": 1,
        "asset_code": "MIC-001",
        "item_name": "Microscope",
        "problem": "Damaged adjustment mechanism.",
        "opened_at": "2026-10-09",
        "opened_by": "Demo Admin",
        "closed_at": "",
        "closed_by": "",
        "action_taken": "",
        "final_condition": "",
        "final_status": "",
        "status": "Open",
    },
    {
        "id": 2,
        "asset_code": "LAP-004",
        "item_name": "Laptop",
        "problem": "Keyboard not responding properly.",
        "opened_at": "2026-09-28",
        "opened_by": "Demo Admin",
        "closed_at": "2026-10-02",
        "closed_by": "Demo Admin",
        "action_taken": "Replaced defective keyboard and tested all keys.",
        "final_condition": "Good",
        "final_status": "Available",
        "status": "Closed",
    },
    {
        "id": 3,
        "asset_code": "PRJ-005",
        "item_name": "Projector",
        "problem": "Projector won't turn on.",
        "opened_at": "2026-09-25",
        "opened_by": "Demo Admin",
        "closed_at": "2026-09-30",
        "closed_by": "Demo Admin",
        "action_taken": "Replaced power supply and confirmed normal operation.",
        "final_condition": "Good",
        "final_status": "Available",
        "status": "Closed",
    },
    {
        "id": 4,
        "asset_code": "CAM-003",
        "item_name": "Camera",
        "problem": "Lens mechanism damaged beyond repair.",
        "opened_at": "2026-09-21",
        "opened_by": "Demo Admin",
        "closed_at": "2026-09-27",
        "closed_by": "Demo Admin",
        "action_taken": "Inspection confirmed replacement was not economical.",
        "final_condition": "Damaged",
        "final_status": "Retired",
        "status": "Closed",
    },
]


def maintenance_preview(request):
    require_preview_mode()

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "all")

    if status_filter not in ("all", "Open", "Closed"):
        status_filter = "all"

    # Counts derived from A2 preview physical units.
    statuses = (
        "Available",
        "Reserved",
        "Issued",
        "Maintenance",
        "Retired",
    )

    stats = {
        status.lower(): sum(
            1 for unit in SAMPLE_PHYSICAL_UNITS
            if unit["status"] == status
        )
        for status in statuses
    }

    stats["total"] = len(SAMPLE_PHYSICAL_UNITS)

    # Demo candidates: available units that do not
    # have an open maintenance record.
    open_codes = {
        record["asset_code"]
        for record in SAMPLE_MAINTENANCE_RECORDS
        if record["status"] == "Open"
    }

    eligible_units = [
        unit
        for unit in SAMPLE_PHYSICAL_UNITS
        if unit["status"] == "Available"
        and unit["asset_code"] not in open_codes
    ]

    records = list(SAMPLE_MAINTENANCE_RECORDS)

    if search_query:
        text = search_query.lower()

        records = [
            record for record in records
            if text in record["asset_code"].lower()
            or text in record["item_name"].lower()
            or text in record["problem"].lower()
        ]

    if status_filter != "all":
        records = [
            record for record in records
            if record["status"] == status_filter
        ]

    records.sort(
        key=lambda record: record["opened_at"],
        reverse=True,
    )

    total_records = len(records)

    paginator = Paginator(records, 5)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "admin_pages/maintenance/maintenance.html",
        {
            "records": page_obj,
            "page_obj": page_obj,
            "stats": stats,
            "eligible_units": eligible_units,
            "search_query": search_query,
            "status_filter": status_filter,
            "total_records": total_records,
        },
    )

# ==========================================
# A7 - REPORTS PREVIEW
# Fictional records, not database data
# ==========================================

import csv
from datetime import date

from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone


def build_reports_preview(request):
    """
    Return loan and overdue report data for the
    selected release-date range.

    Uses SAMPLE_RETURN_LOANS from the A5 preview.
    """

    today = timezone.localdate()

    default_from = date(2026, 7, 1)

    # Keep the demo default valid even if today's
    # date is earlier than July 2026.
    if default_from > today:
        default_from = today

    date_from = request.GET.get(
        "from", default_from.isoformat()
    )

    date_to = request.GET.get(
        "to", today.isoformat()
    )

    try:
        start_date = date.fromisoformat(date_from)
        end_date = date.fromisoformat(date_to)
    except (ValueError, TypeError):
        return {
            "error": "Please enter valid dates.",
            "date_from": date_from,
            "date_to": date_to,
            "loan_report": [],
            "overdue_report": [],
        }

    if start_date > end_date:
        return {
            "error": "The From date cannot be later than the To date.",
            "date_from": date_from,
            "date_to": date_to,
            "loan_report": [],
            "overdue_report": [],
        }

    loan_report = []
    overdue_report = []

    for source in SAMPLE_RETURN_LOANS:

        release_date = date.fromisoformat(
            source["release_date"]
        )

        due_date = date.fromisoformat(
            source["due_date"]
        )

        # Both reports use release date as the
        # date-range filtering basis.
        if not (start_date <= release_date <= end_date):
            continue

        units = source.get("units", [])

        outstanding_units = [
            unit for unit in units
            if not unit.get("returned_at")
        ]

        outstanding_codes = [
            unit["asset_code"]
            for unit in outstanding_units
        ]

        total_units = len(units)
        outstanding_count = len(outstanding_units)

        if outstanding_count == 0:
            status = "Closed"
        elif outstanding_count < total_units:
            status = "Partially Returned"
        else:
            status = "Open"

        # Main loan report
        loan_report.append({
            "code": source["code"],
            "borrower": source["borrower"],
            "release_date": source["release_date"],
            "due_date": source["due_date"],
            "total_units": total_units,
            "status": status,
        })

        # Only currently overdue loans
        # with outstanding units.
        if outstanding_count > 0 and due_date < today:
            overdue_report.append({
                "code": source["code"],
                "borrower": source["borrower"],
                "due_date": source["due_date"],
                "days_late": (today - due_date).days,
                "outstanding_codes": outstanding_codes,
            })

    loan_report.sort(
        key=lambda loan: loan["release_date"],
        reverse=True,
    )

    overdue_report.sort(
        key=lambda loan: loan["days_late"],
        reverse=True,
    )

    return {
        "error": "",
        "date_from": date_from,
        "date_to": date_to,
        "loan_report": loan_report,
        "overdue_report": overdue_report,
    }


def reports_preview(request):
    require_preview_mode()

    report_data = build_reports_preview(request)

    return render(
        request,
        "admin_pages/reports/reports.html",
        {
            "date_from": report_data["date_from"],
            "date_to": report_data["date_to"],
            "date_error": report_data["error"],
            "loan_report": report_data["loan_report"],
            "overdue_report": report_data["overdue_report"],
            "loan_count": len(report_data["loan_report"]),
            "overdue_count": len(report_data["overdue_report"]),
        },
    )


def reports_export_preview(request, report_type):
    require_preview_mode()

    if report_type not in ("loans", "overdue"):
        raise Http404("Invalid report type.")

    report_data = build_reports_preview(request)

    if report_data["error"]:
        return HttpResponseBadRequest(
            report_data["error"]
        )

    response = HttpResponse(
        content_type="text/csv; charset=utf-8"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{report_type}_report.csv"'
    )

    writer = csv.writer(response)

    # Prevent spreadsheet formula injection in
    # CSV fields originating from external input.
    def safe_csv(value):
        text = str(value)

        if text.lstrip().startswith(("=", "+", "-", "@")):
            return "'" + text

        return text

    if report_type == "loans":

        writer.writerow([
            "Loan No.",
            "Borrower",
            "Release Date",
            "Due Date",
            "Units",
            "Status",
        ])

        for loan in report_data["loan_report"]:
            writer.writerow([
                safe_csv(loan["code"]),
                safe_csv(loan["borrower"]),
                loan["release_date"],
                loan["due_date"],
                loan["total_units"],
                loan["status"],
            ])

    else:

        writer.writerow([
            "Loan No.",
            "Borrower",
            "Due Date",
            "Days Late",
            "Outstanding Units",
        ])

        for loan in report_data["overdue_report"]:
            writer.writerow([
                safe_csv(loan["code"]),
                safe_csv(loan["borrower"]),
                loan["due_date"],
                loan["days_late"],
                safe_csv(
                    ", ".join(loan["outstanding_codes"])
                ),
            ])

    return response

# ==========================================
# A8 - OPERATIONAL SETTINGS PREVIEW
# Fictional settings data only
# ==========================================

SAMPLE_OPERATIONAL_SETTINGS = {
    "max_loan_duration": 15,
    "max_request_quantity": 5,
}


def operational_settings_preview(request):
    require_preview_mode()

    return render(
        request,
        "admin_pages/settings/settings.html",
        {
            "settings_data": SAMPLE_OPERATIONAL_SETTINGS,
        },
    )


# ==========================================
# A8 - AUDIT LOGS PREVIEW
# Fictional data only
# ==========================================

SAMPLE_AUDIT_LOGS = [
    {
        "id": 1,
        "timestamp": "2026-10-13 09:15",
        "actor": "Admin",
        "role": "Admin",
        "action": "Request Approved",
        "reference": "R-005",
        "description": "Approved borrowing request R-005 and allocated equipment units.",
    },
    {
        "id": 2,
        "timestamp": "2026-10-13 08:42",
        "actor": "Admin",
        "role": "Admin",
        "action": "Settings Updated",
        "reference": "SETTINGS",
        "description": "Updated maximum loan duration and maximum requested quantity.",
    },
    {
        "id": 3,
        "timestamp": "2026-10-12 14:32",
        "actor": "Admin",
        "role": "Admin",
        "action": "Equipment Issued",
        "reference": "L-003",
        "description": "Released equipment to the borrower and recorded the loan.",
    },
    {
        "id": 4,
        "timestamp": "2026-10-12 11:20",
        "actor": "Juan Dela Cruz",
        "role": "Basic User",
        "action": "Request Submitted",
        "reference": "R-006",
        "description": "Submitted a borrowing request.",
    },
    {
        "id": 5,
        "timestamp": "2026-10-11 16:10",
        "actor": "Admin",
        "role": "Admin",
        "action": "Equipment Returned",
        "reference": "L-001",
        "description": "Recorded the return of a physical equipment unit.",
    },
    {
        "id": 6,
        "timestamp": "2026-10-11 10:05",
        "actor": "Admin",
        "role": "Admin",
        "action": "Maintenance Opened",
        "reference": "MIC-001",
        "description": "Opened a maintenance record for a damaged microscope.",
    },
    {
        "id": 7,
        "timestamp": "2026-10-10 15:30",
        "actor": "Admin",
        "role": "Admin",
        "action": "Account Deactivated",
        "reference": "ACC-003",
        "description": "Deactivated an account while preserving its transaction history.",
    },
    {
        "id": 8,
        "timestamp": "2026-10-10 09:00",
        "actor": "Ana Reyes",
        "role": "Basic User",
        "action": "Request Submitted",
        "reference": "R-005",
        "description": "Submitted a request containing equipment for academic use.",
    },
]

AUDIT_ACTION_OPTIONS = sorted({
    log["action"]
    for log in SAMPLE_AUDIT_LOGS
})


def audit_logs_preview(request):
    require_preview_mode()

    search_query = request.GET.get("q", "").strip()
    action_filter = request.GET.get("action", "all")
    role_filter = request.GET.get("role", "all")

    if action_filter not in AUDIT_ACTION_OPTIONS:
        action_filter = "all"

    if role_filter not in ("all", "Admin", "Basic User"):
        role_filter = "all"

    # Summary cards reflect all preview logs.
    stats = {
        "total": len(SAMPLE_AUDIT_LOGS),
        "admin": sum(
            1 for log in SAMPLE_AUDIT_LOGS
            if log["role"] == "Admin"
        ),
        "user": sum(
            1 for log in SAMPLE_AUDIT_LOGS
            if log["role"] == "Basic User"
        ),
    }

    records = SAMPLE_AUDIT_LOGS

    if search_query:
        q = search_query.lower()

        records = [
            log for log in records
            if q in log["actor"].lower()
            or q in log["action"].lower()
            or q in log["reference"].lower()
            or q in log["description"].lower()
        ]

    if action_filter != "all":
        records = [
            log for log in records
            if log["action"] == action_filter
        ]

    if role_filter != "all":
        records = [
            log for log in records
            if log["role"] == role_filter
        ]

    records = sorted(
        records,
        key=lambda log: log["timestamp"],
        reverse=True,
    )

    paginator = Paginator(records, 5)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "admin_pages/audit/audit_logs.html",
        {
            "logs": page_obj,
            "page_obj": page_obj,
            "stats": stats,
            "search_query": search_query,
            "action_filter": action_filter,
            "role_filter": role_filter,
            "action_options": AUDIT_ACTION_OPTIONS,
        },
    )




# ==========================================
# A7 - DASHBOARD PREVIEW
# Fictional data only
# ==========================================

def _chart_rows(pairs):
    peak = max((count for _, count in pairs), default=0) or 1
    return [
        {"label": label, "count": count, "percent": round(count / peak * 100)}
        for label, count in pairs
    ]


def dashboard_preview(request):
    require_preview_mode()

    return render(
        request,
        "admin_pages/dashboard.html",
        {
            "available_units": 11,
            "pending_requests": 4,
            "active_loans": 6,
            "overdue_loans": 2,
            "monthly_chart": _chart_rows([
                ("May", 3), ("Jun", 5), ("Jul", 4),
                ("Aug", 8), ("Sep", 6), ("Oct", 7),
            ]),
            "category_chart": _chart_rows([
                ("Audio-Visual", 12), ("Computing", 9), ("Lab Tools", 5),
            ]),
        },
    )
