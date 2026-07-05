# NovaCart - Supabase Shopping Site

A modern shopping experience built with React, Vite, and Supabase.

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd withsupabase
```

### 2. Install dependencies
```bash
npm install
```

### 3. Configure environment variables
Copy `.env.example` to `.env` and add your Supabase credentials:
```bash
cp .env.example .env
```

Then edit `.env` and add:
```env
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 4. Run locally
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Deploy to GitHub Pages

### 1. Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Add Supabase secrets to GitHub
In your GitHub repository:
- Go to **Settings** → **Secrets and variables** → **Actions**
- Click **New repository secret**
- Add `VITE_SUPABASE_URL` (paste your Supabase URL)
- Add `VITE_SUPABASE_ANON_KEY` (paste your anon key)

### 3. Enable GitHub Pages
- Go to **Settings** → **Pages**
- Under "Build and deployment":
  - Source: **Deploy from a branch**
  - Branch: **gh-pages** (created automatically by the workflow)
  - Folder: **/ (root)**
- Click **Save**

### 4. Deploy
The app automatically builds and deploys when you push to `main` branch.

Your site will be live at: `https://<your-username>.github.io/withsupabase/`

## Features

- Authentication (sign up, sign in, logout)
- Product catalog from Supabase
- Shopping cart
- Responsive design

## Technologies

- React 18
- Vite
- TypeScript
- Supabase
- Tailwind CSS
