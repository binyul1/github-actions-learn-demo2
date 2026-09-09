# Flask and MySQL Docker Demo

A small Flask REST API backed by MySQL. The project is intended to demonstrate a containerized backend, database initialization, automated tests, and a starting point for GitHub Actions CI/CD.

## Project Structure

```text
.
├── backend/
│   ├── app.py                 # Flask application and API routes
│   ├── Dockerfile             # Backend container image
│   ├── requirements.txt       # Python dependencies
│   └── test/test_app.py       # Flask endpoint tests
├── db-init/init.sql           # MySQL schema and seed data
├── docker-compose.yaml        # Backend and MySQL services
└── .github/workflows/         # GitHub Actions workflow files
```

## Requirements

- Docker Engine
- Docker Compose v2 (`docker compose`)
- Git
- Python 3.12 or newer (only needed to run tests outside Docker)

Check the installed tools with:

```bash
docker --version
docker compose version
python3 --version
```

## Services

Docker Compose defines two services:

| Service | Image/build | Port | Purpose |
| --- | --- | --- | --- |
| `backend` | Built from `backend/Dockerfile` | `5000` | Flask HTTP API |
| `db` | `mysql:8.0` | `3306` | MySQL database |

The database is initialized with the `users` table and seed users from `db-init/init.sql`. MySQL initialization scripts run only when the database data directory is created for the first time.

## Configuration

The backend uses these environment variables:

| Variable | Default in `app.py` | Description |
| --- | --- | --- |
| `DB_HOST` | `db` | MySQL hostname or service name |
| `DB_USER` | `appuser` | MySQL application user |
| `DB_PASS` | `apppassword` | MySQL application password |
| `DB_NAME` | `mydb` | Database name |

The Compose file also configures MySQL with:

```text
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=mydb
MYSQL_USER=appuser
MYSQL_PASSWORD=apppassword
```

These credentials are for local development only. Do not reuse them in a production deployment.

## Running With Docker Compose

After correcting the known setup issues described below, start both services from the repository root:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up -d --build
```

View service status and logs:

```bash
docker compose ps
docker compose logs -f backend
docker compose logs -f db
```

Stop the services:

```bash
docker compose down
```

To remove the MySQL volume and force database initialization on the next start:

```bash
docker compose down -v
```

## API

Once the backend is running, the base URL is `http://localhost:5000`.

### Health or welcome page

```bash
curl http://localhost:5000/
```

### List users

```bash
curl http://localhost:5000/api/users
```

Expected response format:

```json
["Alice", "Bob", "Charlie"]
```

### Add a user

```bash
curl -X POST http://localhost:5000/api/users \
	-H "Content-Type: application/json" \
	-d '{"name":"NewStudent"}'
```

Successful response:

```json
{
	"message": "User NewStudent added successfully!"
}
```

The endpoint returns HTTP `400` when `name` is missing or empty:

```json
{
	"error": "Name is required"
}
```

## Running Tests Locally

Create and activate a virtual environment from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt pytest
```

Run the tests:

```bash
pytest -q backend/test
```

The tests use Flask's test client and mock database operations, so a running MySQL container is not required for this test suite.

## Database Notes

The application reads users from:

```sql
SELECT name FROM users;
```

New users are inserted with a parameterized SQL statement. The `users` table has an auto-incrementing `id` and a required `name` column with a maximum length of 100 characters.

For a fresh database after changing `db-init/init.sql`, remove the Compose volume with `docker compose down -v` and start the services again.

## Known Setup Issues

The current checked-in files require these fixes before the documented Docker startup command can succeed:

1. `backend/Dockerfile` is built with `./backend` as its context, but its `COPY` commands refer to `backend/requirements.txt` and `backend/app.py`. Either build from the repository root or change the Dockerfile copies to `requirements.txt` and `app.py`.
2. `docker-compose.yaml` sets `DB_PASSWORD`, while `backend/app.py` reads `DB_PASS`. The variable names must match.
3. `db-init/init.sql` has a trailing comma after the `name` column and needs a statement terminator after the `CREATE TABLE` statement.
4. The backend starts immediately after the database container starts. A production-ready setup should add a database health check and make the backend wait until MySQL accepts connections.

Until these are corrected, local Python tests can still be run independently with the command in [Running Tests Locally](#running-tests-locally).

## Development Workflow

1. Make a focused change in `backend/`, `db-init/`, or `docker-compose.yaml`.
2. Run `pytest -q backend/test`.
3. Rebuild the containers when Docker-related files change:

	 ```bash
	 docker compose up --build
	 ```

4. Exercise the API with the `curl` commands above.
5. Review logs with `docker compose logs` before opening a pull request.

## License

No license has been specified for this repository. Add a license file before distributing the project outside its intended learning environment.