# TechM4India Frontend Setup Guide

## Quick Start

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API URL:
   ```
   VITE_API_URL=http://localhost:4000/api
   ```
   
   For production, use your production API URL.

4. **Start development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

## Project Overview

This is a complete frontend implementation for TechM4India with:

- ✅ **30 Pages** covering all content requirements
- ✅ **Responsive Design** for mobile, tablet, and desktop
- ✅ **Modern UI** with Tailwind CSS
- ✅ **TypeScript** for type safety
- ✅ **React Router** for navigation
- ✅ **JWT-based Auth** via backend API
- ✅ **SEO Optimized** pages

## Page Structure

### Main Pages
- `/` - Home
- `/about` - About Us
- `/why-techm4india` - Why Choose TechM4India
- `/divisions` - Divisions Overview

### Division Pages
- `/divisions/schools` - TechM4Schools About
- `/divisions/schools/programs` - Schools Programs
- `/divisions/schools/benefits` - Schools Benefits
- `/divisions/engineering` - TechM4Engineering About
- `/divisions/engineering/programs` - Engineering Programs
- `/divisions/engineering/benefits` - Engineering Benefits
- `/divisions/solutions` - TechM4Solutions About
- `/divisions/solutions/offerings` - Solutions Offerings
- `/divisions/solutions/benefits` - Solutions Benefits
- `/divisions/space` - TechM4Space About
- `/divisions/space/programs` - Space Programs
- `/divisions/space/benefits` - Space Benefits

### Services Pages
- `/programs-services` - Programs & Services Overview
- `/services/schools` - Services for Schools
- `/services/colleges` - Services for Colleges
- `/services/enterprises` - Services for Enterprises

### Other Pages
- `/research-innovation` - Research & Innovation
- `/global-partnerships` - Global Partnerships
- `/tech-stack/frontend` - Frontend Tech Stack
- `/tech-stack/backend` - Backend Tech Stack
- `/tech-stack/ai-ml` - AI/ML Tech Stack
- `/tech-stack/cloud` - Cloud Deployment
- `/tech-stack/devops` - DevOps & Security
- `/roadmap` - Vision 2037 Roadmap
- `/careers` - Careers
- `/contact` - Contact & FAQ

## Features Implemented

### Navigation
- Responsive header with mobile menu
- Dropdown navigation for divisions
- Active route highlighting
- Smooth scrolling

### Components
- **Hero** - Page hero sections with CTAs
- **FeatureCard** - Reusable feature display cards
- **CTA** - Call-to-action buttons
- **Header** - Main navigation header
- **Footer** - Site footer with links and contact info

### Authentication
- JWT-based authentication via backend API
- Protected routes (ready for implementation)
- User session management with localStorage

### Styling
- Tailwind CSS with custom color scheme
- Responsive grid layouts
- Gradient backgrounds
- Hover effects and transitions
- Custom scrollbar styling

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` folder.

## Deployment

### Vercel (Recommended)
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow the prompts

### Netlify
1. Build the project: `npm run build`
2. Deploy the `dist` folder to Netlify

### AWS S3 + CloudFront
1. Build the project: `npm run build`
2. Upload `dist` folder contents to S3 bucket
3. Configure CloudFront distribution

## Environment Variables

Required environment variables:
- `VITE_API_URL` - Your backend API URL (default: `http://localhost:4000/api`)

## Backend Integration

The frontend is configured to proxy API requests to the backend:
- Development: `http://localhost:4000`
- Configure in `vite.config.ts` for production

## Support

For issues or questions, contact:
- Email: techm4india@gmail.com
- Phone: +91 6301814246

