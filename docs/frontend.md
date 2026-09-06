# FrontEnd
> This project will use ReactJS (Next.js) as the FrontEnd

## 1. How to set up

Check for the version of `Node.js` first:

```bash
node -v
```

If you don't have `Node.js` - go to the website: `https://nodejs.org/en`

After that, bootstrap a Next.js app with TypeScript + Tailwind:

```bash
npx create-next-app@latest my-react-app --ts --tailwind --eslint --app
```

> The real project lives under `rag-vgu/` at the repo root - treat that as the
> working copy. Names like `my-react-app` below are just placeholders.

## 2. Navigate and Install Dependencies

```bash
cd rag-vgu
npm install
```

## 3. Start the Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view it.

## 4. Adjust and Develop UI for FrontEnd

> We technically develop and adjust in `rag-vgu/app/*` only

Work-tree:

```bash
rag-vgu/
|-- app/
|   |-- globals.css
|   |-- layout.tsx
|   |-- page.tsx
|   |-- lib/
|   |   `-- api.ts
|-- public/
|-- package.json
|-- tsconfig.json
|-- next.config.ts
```

## 5. Connect the Frontend to the Backend

> We technically develop and adjust in `rag-vgu/app/lib/api.ts` only

The frontend talks to the FastAPI backend over HTTP. The base URL is read from
`NEXT_PUBLIC_API_BASE_URL` (empty string means same-origin, e.g. when served
together in production):

```ts
// app/lib/api.ts
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "";
```

During local development run the backend separately and point the frontend at it:

```bash
# .env.local
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

The CORS allow-list on the backend (`app.py`) is configured to accept
`http://localhost:3000` and `http://127.0.0.1:3000` during development.

### Available endpoints

| Method | Endpoint            | Purpose                          |
| ------ | ------------------- | -------------------------------- |
| POST   | `/api/auth/signup`  | Create a new user account        |
| POST   | `/api/auth/login`   | Authenticate an existing user    |
| POST   | `/api/uploader/upload` | Upload a document            |

Both auth endpoints accept `{ "username": string, "password": string }`
(password max length `72`) and return `{ "user_id": string, "username": string }`.

### Calling the API from a page

Add a small typed helper for each endpoint in `app/lib/api.ts`, then use it from
a client component (a file marked `"use client"`). Example already wired up on
the login page (`app/page.tsx`):

```ts
import { login, signup } from "./lib/api";

const result = await login(username, password);
// result -> { user_id, username }
```

## 6. Go Live

The whole stack (frontend, backend, Qdrant) is deployed with Docker Compose from
the repo root:

```bash
docker compose up --build
```

Then open [http://localhost:3000](http://localhost:3000) (frontend) and
[http://localhost:8000](http://localhost:8000) (backend API).
