# Leave Management - Business Requirements

Owner: People Operations (Product Owner: Hannah Reyes)
Version: 1.2 - Status: Approved for build

## 1. Purpose
Acme employees currently request time off by email and spreadsheet. This service lets employees
request leave, lets managers decide on it, and lets HR see the whole picture.

## 2. Roles
- **Employee** - requests and cancels their own leave.
- **Manager** - an employee who also decides on requests from their direct reports.
- **HR Administrator** - has read access to all leave data and can search it.

## 3. Requirements

**LR-1** Users sign in with their company email and password and receive a bearer token for
subsequent calls.

**LR-2** The system supports three leave types: annual, sick and unpaid.

**LR-3** Each employee has a leave balance per leave type per calendar year. New employees start
with 25 annual days and 10 sick days. Unpaid leave has no balance limit.

**LR-4** An employee can submit a leave request with a leave type, a start date, an end date and an
optional free-text reason. The end date must not be before the start date.

**LR-5** The number of days in a request is the number of working days (Monday to Friday) from the
start date to the end date, including both dates. A request with no working days is rejected.

**LR-6** A request for annual or sick leave is refused if the employee's remaining balance for that
type is lower than the number of days requested.

**LR-7** A new request has the status `pending`. A pending request can become `approved` or
`rejected`; a pending or approved request can become `cancelled`.

**LR-8** Only the employee's direct manager can approve or reject a request. A manager must never
approve or reject their own request.

**LR-9** Approving a request deducts its working days from the employee's balance for the leave type.

**LR-10** An employee can cancel their own request only while the leave has not yet started.
Rejected and already-cancelled requests cannot be cancelled.

**LR-11** Cancelling an approved request restores its working days to the employee's balance.

**LR-12** Employees can see their own requests and balances. A manager can additionally see
requests of their direct reports and a list of requests awaiting their decision.

**LR-13** HR Administrators can see all leave requests and can search them by employee name and sort
the results.

**LR-14** Free-text reasons may contain personal information, in particular for sick leave, and
must be handled in line with the company data protection policy.

**LR-15** Access tokens must expire and must be signed with a secret that is configured per
environment.

## 4. Out of scope (this release)
Email notifications, calendar integration, a user interface.
