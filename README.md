# aiph-alpha

## Build & Deployment Guide

This project is a full-stack application with a FastAPI backend and a Vue 3 + Vuetify frontend. Both are containerized using Docker and orchestrated with Docker Compose for local development and production (VPS) deployment.

---

### 1. Project Structure

- `backend/`: FastAPI app (Python)
- `frontend/`: Vue 3 + Vuetify app (Node.js, Vite, Nginx for production)
- `docker-compose.yml`: Main Compose file for local development
- `docker-compose.prod.yml`: Compose file for production (VPS) deployment
- `.env` files: Used for environment-specific configuration

---

### 2. Local Development

#### Backend
- **Dockerfile**: Builds a Python image, installs dependencies, copies code, exposes port 8001, and runs FastAPI with `--reload` for hot-reloading.
- **Volumes**: The backend code is mounted as a volume for live reloading.
- **Environment Variables**: Set in `docker-compose.yml` (e.g., `DATABASE_URL`), can be overridden by a local `.env` file.
- **Port Mapping**: Host port 8001 → container port 8001.

#### Frontend
- **Dockerfile**: Multi-stage build.
  - **Build stage**: Uses Node.js to install dependencies and build the static site.
  - **Production stage**: Uses Nginx to serve the built files.
- **Volumes**: Not used for production build; for local dev, you can mount the code and run Vite dev server.
- **Port Mapping**: Host port 8080 → container port 80 (Nginx).
- **Environment Variables**: No VITE_ envs are required or used. The frontend expects to call the backend via `/api/` and lets Nginx proxy to the backend.

#### Database
- **Service**: Postgres, defined as `db` in the main Compose file. There is no longer a `database/` folder or separate compose file.
- **Port Mapping**: Host port 5432 → container port 5432 (if exposed).

#### Running Locally

```bash
docker-compose up --build
```
- The frontend will be available at [http://localhost:8080](http://localhost:8080)
- The backend API at [http://localhost:8001](http://localhost:8001)
- The database at `localhost:5432` (if exposed)

---

### 3. Production (VPS) Deployment

#### Images
- **CI/CD**: Typically, images are built and pushed to a registry (e.g., Docker Hub, GitHub Container Registry).
- **Compose**: `docker-compose.prod.yml` uses pre-built images via `image: ${BACKEND_IMAGE_NAME}` and `image: ${FRONTEND_IMAGE_NAME}`.

#### Environment Variables
- **Backend**: All secrets and config (e.g., `DATABASE_URL`, `SECRET_KEY`, etc.) are injected via the VPS `.env` file.
- **Frontend**: Nginx server name and API URLs are set via environment variables and config templates. The frontend always uses `/api/` as the backend proxy path, and Nginx will forward requests to the backend service.

#### Nginx & Entrypoint
- The frontend container uses an `entrypoint.sh` script to substitute environment variables (like `NGINX_SERVER_NAME`) into the Nginx config at container startup.
- The Nginx config proxies `/api/` requests to the backend service (`http://backend:8001/`).

#### Running on VPS

1. Set up your `.env` file with all required variables (see `backend/.env.example` and Compose files for reference).
2. Pull or build images as needed.
3. Start services:

```bash
docker-compose -f docker-compose.prod.yml --env-file .env up -d
```

---

### 4. Environment Variables & Configuration

#### Backend
- `.env.example` lists required variables (e.g., `OPENAI_API_KEY`, `SECRET_KEY`, etc.).
- `DATABASE_URL` is constructed from Compose or `.env` values.

#### Frontend
- No VITE_ envs are used. For all environments, the frontend calls `/api/` and relies on Nginx to proxy to the backend.

#### Nginx
- `nginx.conf.template` is processed by `entrypoint.sh` to inject the server name and proxy settings.

---

### 5. Key Differences: Local vs. VPS Deployment

| Aspect         | Local Development                                 | VPS/Production Deployment                        |
|----------------|---------------------------------------------------|--------------------------------------------------|
| **Images**     | Built locally via Dockerfile                      | Pulled from registry (built by CI/CD)            |
| **Compose**    | `docker-compose.yml`                              | `docker-compose.prod.yml`                        |
| **Volumes**    | Code mounted for live reload (backend)            | No code mounts; images are self-contained         |
| **Frontend**   | Vite dev server (optional), or Nginx static serve | Nginx static serve only                          |
| **Env Vars**   | Set in Compose or `.env` (local)                  | Set in VPS `.env` and injected at runtime        |
| **Database**   | Local Postgres (as `db` service)                  | Usually managed separately or as a Compose service |
| **Entrypoint** | Not always used                                   | Used to template Nginx config with env vars      |
| **API URL**    | Frontend uses `/api/` and Nginx proxies           | Frontend uses `/api/` and Nginx proxies          |

---

### 6. Build & Deployment Dependencies

- **Docker**: Required for all environments.
- **Docker Compose**: For orchestration.
- **Node.js & pnpm**: For frontend build (in Dockerfile).
- **Python**: For backend (in Dockerfile).
- **Nginx**: For serving frontend in production.
- **Postgres**: As the database.

---

### 7. Example: Setting Up for Local Development

1. Copy `.env.example` to `.env` in `backend/` and fill in secrets.
2. Start services:

```bash
docker-compose up --build
```

---

### 8. Example: Deploying to VPS

1. Build and push images (or use CI/CD).
2. Create a `.env` file on the VPS with all required variables.
3. Run:

```bash
docker-compose -f docker-compose.prod.yml --env-file .env up -d
```

---

### 9. Troubleshooting

- **Environment Variables**: Ensure all required variables are set in `.env` files.
- **Port Conflicts**: Make sure host ports (8001, 8080, 5432) are available.
- **API Calls**: If frontend can't reach backend, check Nginx proxy config. The frontend always uses `/api/`.
- **CORS**: If you see CORS errors, ensure the frontend is using `/api/` and Nginx is proxying to the backend.
- **Database**: For production, use a managed Postgres or secure the Compose service.

---

### 10. References

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Vite Env Variables](https://vitejs.dev/guide/env-and-mode.html)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vuetify Docs](https://vuetifyjs.com/)

