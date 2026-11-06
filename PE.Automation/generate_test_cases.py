# -*- coding: utf-8 -*-
"""Generate expanded Jira-importable test cases for LaunchPoint, CoreECI, AVR."""
from __future__ import annotations
import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent / "Test_Documents" / "Test_Cases"
OUT.mkdir(parents=True, exist_ok=True)

COLS = [
    "Test Case ID",
    "Feature ID",
    "Application",
    "Module",
    "Subfeature",
    "Test Scenario",
    "Test Case Title",
    "Preconditions",
    "Test Steps",
    "Test Data",
    "Expected Result",
    "Test Type",
    "Priority",
    "Automation Status",
    "Execution Status",
    "Defect ID",
]

rows: list[dict] = []


def add(app, feature, module, sub, scenario, title, pre, steps, data, exp, ttype, pri, auto="Designed", exec_="Not Executed", defect=""):
    n = len([r for r in rows if r["Application"] == app]) + 1
    prefix = {"LaunchPoint": "LP", "CoreECI": "CE", "AVR": "AVR"}[app]
    rows.append({
        "Test Case ID": f"{prefix}-TC-{n:04d}",
        "Feature ID": feature,
        "Application": app,
        "Module": module,
        "Subfeature": sub,
        "Test Scenario": scenario,
        "Test Case Title": title,
        "Preconditions": pre,
        "Test Steps": steps,
        "Test Data": data,
        "Expected Result": exp,
        "Test Type": ttype,
        "Priority": pri,
        "Automation Status": auto,
        "Execution Status": exec_,
        "Defect ID": defect,
    })


# -------- LaunchPoint (aim 80+) --------
auth_cases = [
    ("valid login", "rachel.torres@consilio.com / valid password", "Home loads", "Functional", "P0", "Automated"),
    ("empty username", "username=''", "Validation prevents continue", "Negative", "P1", "Designed"),
    ("empty password", "password=''", "Validation prevents continue", "Negative", "P1", "Designed"),
    ("malformed email", "user@", "Validation/error shown", "Boundary", "P2", "Designed"),
    ("wrong password", "valid user / Wrong!", "Remain on Identity; no LaunchPoint session", "Negative", "P0", "Automated"),
    ("SQL injection username", "' OR 1=1--", "Treated as literal; login fails safely", "Security", "P0", "Designed"),
    ("XSS username", "<script>alert(1)</script>", "No script execution", "Security", "P1", "Designed"),
    ("remember username on", "Remember checked", "Username retained next visit", "Functional", "P2", "Designed"),
    ("remember username off", "Remember unchecked", "Username not retained", "Functional", "P2", "Designed"),
    ("direct home without auth", "clear cookies; /home", "Redirect/sign-in gate", "Security", "P0", "Designed"),
]
for title, data, exp, ttype, pri, auto in auth_cases:
    add("LaunchPoint", "FE557", "Authentication", "Sign In", "Sign-in variations", f"FE557 {title}", "Identity reachable", "1. Open Identity 2. Enter data 3. Continue", data, exp, ttype, pri, auto)

for title in ["Sign out from profile", "Sign out then protected URL blocked", "Sign out clears CoreECI access", "Multi-tab sign out", "Sign out then re-login"]:
    add("LaunchPoint", "—", "Authentication", "Sign Out", "Logout", title, "Authenticated", "1. Open profile 2. Sign Out 3. Verify", "user_cookie present then cleared", "Session ended; apps gated", "Functional", "P1", "Designed")

for i, title in enumerate([
    "Home heading visible", "User email visible in profile", "Open AVR tile", "Open Aurora Command Center", "Theme toggle light/dark",
    "Pulse filter News", "Pulse filter Insight", "Pulse filter Release", "Give Feedback visible", "GDPR footer links visible",
    "Refresh home retains session", "Browser back after navigation", "Deep link /home authenticated", "Concurrent tab home", "Home stats regions/projects render"
], 1):
    add("LaunchPoint", "FE588", "Home Dock", "Home", "Home dock behaviours", f"FE588 {title}", "Signed in", f"1. Open /home 2. Exercise '{title}' 3. Assert", "Rachel Torres session", "UI matches verified LaunchPoint home", "UI", "P1" if i < 5 else "P2", "Automated" if i <= 2 else "Designed")

for title in [
    "List regions", "Open Aurora US", "Search enclaves", "Client directory search", "Filter clients by domain",
    "Filter clients by tier", "Sort clients", "Grid vs list view", "Open client 300671 projects", "Open project A30020",
    "CoreECI Enabled badge", "Project Profile modal", "View Details storage modal", "Intake Audit modal", "Processing Summary modal",
    "AVR workspace list 11 records", "Filter AVR by instance", "Filter AVR by client", "Search workspace A30022", "Launch Workspace modal fields",
    "Launch Workspace Connecting state", "Launch opens AVR", "Back to Home breadcrumb", "Unauthorized direct project URL", "Pagination page size 25/50/100"
]:
    add("LaunchPoint", "—", "Aurora Gateway", "Navigation", "Aurora/LP gateway", title, "Signed in System Admin", f"1. Navigate 2. {title} 3. Verify", "aurora-us / A30022", "Verified navigation behaviour", "UI", "P2", "Designed")

# -------- CoreECI (aim 80+) --------
for title, data, exp, auto in [
    ("Unauthenticated gate", "no cookies", "You are not signed in", "Automated"),
    ("Authenticated no project gate", "LP session only", "No project selected", "Automated"),
    ("Back to LaunchPoint from gate", "no project gate", "Returns to LP", "Designed"),
    ("Go to LaunchPoint CTA", "unauth gate", "Identity/LP flow", "Designed"),
    ("Deep link /project/A30022 without handoff", "path only", "Still gated", "Designed"),
    ("Query project param ignored without handoff", "?project=A30022", "Still gated", "Designed"),
]:
    add("CoreECI", "—", "Access", "Project Gate", "Access gates", title, "As specified", "1. Open CoreECI 2. Observe gate", data, exp, "Functional", "P0", auto)

for fid, module, titles in [
    ("FE137", "Search Term Reports", [
        "Open reports list", "Create report valid terms", "Create report empty name", "Create report empty terms",
        "Report name max length", "Report name over max", "Special chars in report name", "Unicode report name",
        "Injection in search terms", "Scope=load", "Execute report", "Re-execute report", "Delete report",
        "Filter reports by status", "Sort by execution date", "DocumentsMatched vs TotalMatches", "Open report detail",
        "Manage tags from report", "Cancel create report", "Concurrent create"
    ]),
    ("FE163", "Hit List", [
        "Hit list shows matched docs", "Empty hit list", "Open doc from hit", "Snippet highlight", "Hit list pagination",
        "Hit list sort", "Hit list filter custodian", "No-result messaging", "Large hit set performance smoke", "Refresh retains hits"
    ]),
    ("FE239", "Document Tagging", [
        "Apply Relativity tag", "Apply AVR tag", "Apply privilege tag", "Apply trade secret tag", "Remove tag",
        "Unknown tag rejected", "Tag persists after refresh", "Multi-tag document", "Tag color chip", "Category grouping"
    ]),
    ("FE278", "Export Creation", [
        "Open exports list", "Create Relativity export", "Create AVR export", "Empty document set rejected",
        "Filter exports", "Sort exports", "Export status badge", "Switch project context", "Export volume display", "Notes field special chars"
    ]),
    ("FE297", "Package Manifest", [
        "Open manifest for export", "Manifest rows match package", "Empty manifest state", "Manifest columns present",
        "Manifest export CSV if offered", "Manifest search", "Manifest pagination", "Unauthorized manifest access",
        "Manifest after failed export", "Manifest timezone stamps"
    ]),
]:
    for t in titles:
        status = "Designed"
        defect = "DEF-CORE-001" if "Intake" in t else ""
        add("CoreECI", fid, module, t, f"{fid} coverage", f"{fid} {t}", "CoreECI project handoff Verified OR blocked noted", f"1. Launch CoreECI project 2. {t} 3. Assert", "A30022 / Load 1001", "Matches verified/requirements when accessible; else Blocked", "Functional", "P1", status, "Not Executed", defect)

for t in ["Intake Audit shows storage fields (defect)", "Project Profile storage fields", "Most Recent Load Date", "CoreECI Active indicator", "Total Documents metric"]:
    add("CoreECI", "—", "LaunchPoint Telemetry", t, "Telemetry", t, "LP project page", f"1. Open project 2. {t}", "A30022", "Telemetry accurate except known defect", "UI", "P2", "Designed", "Not Executed", "DEF-CORE-001" if "defect" in t else "")

# -------- AVR (aim 100+) --------
for fid, module, titles in [
    ("FE749", "Reviewer Management", [
        "Open assignments", "Create assignment required name", "Create with description", "Create disabled until name",
        "Cancel create", "Custom keyword group add", "Security group select", "Series colour select", "Duplicate assignment name", "XSS in assignment name"
    ]),
    ("FE750", "Reviewer Management", [
        "Select one reviewer", "Select multiple reviewers", "Search reviewers", "Deselect reviewer", "No reviewer selected",
        "Reviewer email visible", "Reviewer checkbox persistence on cancel", "Add reviewer on edit", "Remove reviewer on edit", "Max reviewers boundary"
    ]),
    ("FE751", "Reviewer Management", [
        "View reviewer count on list", "Open Manage Reviewers", "Assigned reviewers for 88259553", "Filter assignments Open",
        "Filter In Review", "Filter Completed", "Filter Suspended", "Search assignment by ID", "Edit assignment", "Pagination rows 10/25/50"
    ]),
    ("FE437", "Document Allocation", [
        "Search with empty keyword", "Search keyword shipment", "Empty state before search", "Custodian filter", "Batch filter unassigned",
        "Responsiveness filter", "Privilege filter", "File type filter", "Clear filters", "Keyword group selector"
    ]),
    ("FE443", "Document Allocation", [
        "Select this page", "Allocate selected enabled", "Allocate selected disabled at 0", "Unallocate selected", "Select single row",
        "Select across page", "Allocate to assignment", "Allocate without assignment blocked", "Rapid multi-select", "Selection count badge"
    ]),
    ("FE448", "Document Allocation", ["Choose assignment in reviews", "Switch assignment dropdown", "Assignment protocol instructions", "Invalid assignment id", "Assignment persists on refresh"]),
    ("FE449", "Document Allocation", ["Reviewer shown on pending doc", "Choose reviewer during allocate", "Unassigned reviewer state", "Reviewer filter", "Reviewer mismatch warning"]),
    ("FE457", "Document Allocation", ["Open pending doc in Reviews", "Open from documents grid", "Prev/Next document controls", "Native view", "Text view"]),
    ("FE394", "Review Documents", ["Set Responsive", "Set Not Responsive", "Set Technical Issue", "Required responsiveness", "Change responsiveness before save"]),
    ("FE395", "Review Documents", ["Set Confidential", "Set Not Confidential", "Required confidentiality", "Toggle confidentiality", "Save draft keeps value"]),
    ("FE396", "Review Documents", ["Set Privileged", "Set Not Privileged", "Required privilege", "Toggle privilege", "Save draft keeps value"]),
    ("FE747", "Review Documents", ["Save Draft", "Complete Review enabled after required", "Complete Review blocked missing required", "Hot Doc checkbox", "Remarks optional"]),
    ("FE531", "Production", ["Open production module", "New production package visible", "Search packages", "Status filter Draft", "Status filter Released"]),
    ("FE533", "Production", ["Find production documents expand", "Search by doc id", "Search by custodian", "Select docs for package", "Empty selection"]),
    ("FE538", "Production", ["Eligibility messaging", "Failed validation status", "Validated status", "Open package", "Manifest button state"]),
]:
    for t in titles:
        add("AVR", fid, module, t, f"{fid} coverage", f"{fid} {t}", "AVR A30022 launched as System Admin", f"1. Open module 2. {t} 3. Assert", "A30022 / Workspace 539", "Matches verified AVR UI behaviour", "Functional", "P1", "Automated" if t in ["Open assignments", "Search with empty keyword", "Open production module", "Set Responsive", "Create assignment required name"] else "Designed")

# write per-app csv
by_app = {}
for r in rows:
    by_app.setdefault(r["Application"], []).append(r)

for app, items in by_app.items():
    path = OUT / f"{app}_TestCases.csv"
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(items)
    print(app, len(items), "->", path.name)

# combined
with (OUT / "All_Applications_TestCases.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS)
    w.writeheader()
    w.writerows(rows)
print("TOTAL", len(rows))
