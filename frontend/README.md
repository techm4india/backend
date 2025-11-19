# TechM4India Frontend

Modern, responsive frontend for TechM4India - India's First Experiential Learning Ecosystem.

## Tech Stack

- **React 18** - Modern UI library
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Backend API** - REST API integration via environment variables
- **Lucide React** - Beautiful icons
- **Framer Motion** - Smooth animations

## Features

✅ Complete 30-page website covering all content requirements
✅ Responsive design for all devices
✅ Modern UI with Tailwind CSS
✅ JWT-based authentication via backend API
✅ SEO-optimized pages
✅ Accessible components
✅ Fast performance with Vite

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Add your API URL to `.env`:
```
VITE_API_URL=http://localhost:4000/api
```

For production, update this to your production API URL.

4. Start development server:
```bash
npm run dev
```

5. Build for production:
```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── contexts/         # React contexts (Auth, etc.)
│   ├── pages/            # Page components
│   │   ├── divisions/    # Division-specific pages
│   │   ├── services/     # Service pages
│   │   └── techstack/    # Tech stack pages
│   ├── App.tsx           # Main app component
│   └── main.tsx         # Entry point
├── public/               # Static assets
└── index.html           # HTML template
```

## Pages

All 30 pages from the content document are implemented:

1. Home
2. About Us
3. Why TechM4India
4. Divisions Overview
5-16. Division-specific pages (Schools, Engineering, Solutions, Space)
17-20. Programs & Services pages
21. Research & Innovation
22. Global Partnerships
23-27. Tech Stack pages
28. Roadmap
29. Careers
30. Contact & FAQ

## Development

- Development server runs on `http://localhost:3000`
- Backend API proxy configured for `/api` routes
- Hot module replacement enabled
- TypeScript strict mode enabled

## Deployment

Build the project:
```bash
npm run build
```

The `dist/` folder contains the production-ready files.

Deploy to:
- Vercel (recommended)
- Netlify
- AWS S3 + CloudFront
- Any static hosting service

## License

Copyright © 2024 TechM4India

