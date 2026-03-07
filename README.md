# Library Service API

A RESTful API for managing a library: books, borrowings, and returns.  
Built with **Django REST Framework** and **JWT authentication**.

---

## Features

### Books
- Create / Read / Update / Delete books
- Fields: `title`, `author`, `cover` (`HARD`/`SOFT`), `inventory`, `daily_fee` (USD, Decimal)
- Permissions:
  - **Read** (GET list/retrieve): public
  - **Write** (POST/PUT/PATCH/DELETE): admin only

### Users & Auth (JWT)
- User registration
- JWT token obtain / refresh / verify
- `/me/` endpoint to view/update current user profile

### Borrowings
- Create borrowing (**decreases book inventory by 1**; not allowed if inventory is 0)
- List + detail endpoints
- Filters:
  - `?is_active=true|false`
  - `?user_id=<id>` (admin only)
- Return endpoint: `POST /borrowings/{id}/return/`
  - Sets `actual_return_date`
  - **Increases book inventory by 1**
  - Prevents double return

### Pagination
- Pagination enabled for list endpoints (e.g. books and borrowings)

### API Documentation
- Swagger / OpenAPI documentation available

---

## Run locally

```bash
git clone https://github.com/anastasiiaoshega513/library-service-api.git
cd library-service-api

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Get token
`POST /api/user/token/`
```json
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```
