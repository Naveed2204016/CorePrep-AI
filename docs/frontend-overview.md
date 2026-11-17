# Frontend Overview

## Purpose
The CorePrep AI frontend provides the user interface for authentication, learning roadmaps, assessments, company-specific interview practice, CV review, and profile information.

## Technology
- React 19
- TypeScript
- Vite
- React Router 7
- Tailwind CSS 4
- Framer Motion
- Lucide React

## Documented source layout

The project README describes the following frontend structure:

```text
frontend/
├── public/
├── src/
│   ├── assets/
│   ├── components/
│   │   ├── auth/
│   │   ├── layout/
│   │   └── ui/
│   ├── features/
│   │   └── company-prep/
│   │       └── data/
│   ├── pages/
│   ├── services/
│   ├── types/
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── package.json
├── .env.example
├── vite.config.ts
└── vercel.json
```

## Responsibilities
- `components/`: reusable interface elements and layout components.
- `features/`: feature-specific UI and data.
- `pages/`: route-level screens.
- `services/`: frontend communication with backend APIs.
- `types/`: shared TypeScript types.

The exact contents of each folder may evolve. Check the source tree before adding imports or assuming a component exists.

## Local development
From the `frontend` directory:

```bash
npm install
```

Create a local `.env` from `.env.example`, then configure the API base URL and authentication mode as required by your environment.

```bash
npm run dev
```

The README documents the development URL as `http://localhost:5173`.

## Contribution checklist
- Keep components focused and reusable.
- Use the existing styling and routing conventions.
- Avoid placing secrets in frontend source code.
- Verify the application with the scripts defined in `frontend/package.json`.
