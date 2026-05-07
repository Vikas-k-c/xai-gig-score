# XAI Gig Score - AI-Powered Credit Scoring for Gig Workers

An explainable AI (XAI) credit scoring system designed specifically for gig economy workers. This platform leverages machine learning and SHAP (SHapley Additive exPlanations) to provide transparent, fair credit scores based on gig work activity, income patterns, and financial behavior.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-green)
![React](https://img.shields.io/badge/React-19.0+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

**XAI Gig Score** is a credit scoring platform that addresses the challenges of evaluating creditworthiness for gig economy workers who lack traditional employment histories. Using XAI techniques, it provides:

- **Transparent Credit Scores**: Understand exactly why a credit score was assigned
- **Fair Assessment**: Considers gig-specific metrics like task completion rates, platform tenure, and income stability
- **Real-time Scoring**: Instant credit assessment based on connected platform data
- **Explainability**: SHAP-based feature importance for each prediction

## Features

### Core Features
- **User Authentication**: Secure registration and login system
- **Multi-Platform Integration**: Connect data from multiple gig platforms (Uber, Upwork, TaskRabbit, etc.)
- **PAN (Permanent Account Number) Verification**: India-specific tax/identity verification
- **Credit Score Calculation**: XGBoost-based ML model for credit scoring (300-900 scale)
- **Risk Assessment**: Automatic risk level classification (Low/Medium/High)
- **Loan Management**: Track and manage user loans
- **Explainability Dashboard**: SHAP-based feature importance visualization
- **Admin Dashboard**: Monitor users, predictions, and platform data

### ML/AI Features
- **Feature Engineering**: Comprehensive feature extraction from platform data
  - Income metrics (average income, volatility, growth trends)
  - Activity metrics (active days, hours worked, task completion rate)
  - Financial stability (wallet transactions, savings ratio)
  - Platform tenure and user ratings
- **SHAP Explanations**: Understand model predictions at feature level
- **Model Artifacts**: Pre-trained XGBoost models with metrics and thresholds

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Database**: PostgreSQL + SQLAlchemy ORM
- **Authentication**: JWT + bcrypt
- **ML/AI**: scikit-learn, XGBoost, SHAP, joblib
- **Validation**: Pydantic

### Frontend
- **Framework**: React 19
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router v7
- **Icons**: Lucide React
- **Animations**: Motion

### ML Pipeline
- **Data Processing**: Pandas, NumPy
- **Model Training**: scikit-learn, XGBoost
- **Explainability**: SHAP
- **Visualization**: Matplotlib, Seaborn

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  - Dashboard, Login, Loan Management, Predictions       │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────┐
│              Backend (FastAPI)                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Routes: Auth, PAN, Platform, Predict, Loans    │   │
│  │  Services: Scoring, Explaining, Feature Eng.    │   │
│  │  Models: User, Prediction, Loan, PlatformData   │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────┐        ┌────────▼───────┐
│ PostgreSQL   │        │  ML Pipeline   │
│ Database     │        │  (Trained      │
│              │        │   Models)      │
└──────────────┘        └────────────────┘
```

## Project Structure

```
xai-gig-score/
├── backend/                          # FastAPI backend application
│   ├── app/
│   │   ├── main.py                  # FastAPI app initialization
│   │   ├── config.py                # Configuration settings
│   │   ├── database.py              # Database setup & connection
│   │   ├── deps.py                  # Dependency injection
│   │   ├── models/                  # SQLAlchemy ORM models
│   │   │   ├── user.py
│   │   │   ├── loan.py
│   │   │   ├── pan.py
│   │   │   ├── platform.py
│   │   │   ├── prediction.py
│   │   │   └── __init__.py
│   │   ├── routes/                  # API routes/endpoints
│   │   │   ├── auth.py              # Authentication endpoints
│   │   │   ├── loans.py             # Loan management
│   │   │   ├── pan.py               # PAN verification
│   │   │   ├── platform.py          # Platform data endpoints
│   │   │   ├── predict.py           # Credit scoring predictions
│   │   │   ├── dashboard.py         # Dashboard data
│   │   │   └── __init__.py
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── services/                # Business logic services
│   │   │   ├── scoring_service.py   # Credit score calculation
│   │   │   ├── explain_service.py   # SHAP explanations
│   │   │   ├── model_service.py     # ML model inference
│   │   │   ├── feature_engineering.py
│   │   │   └── mock_data.py
│   │   └── utils/                   # Utility functions
│   │       ├── constants.py
│   │       ├── security.py          # JWT & auth utilities
│   │       └── validators.py
│   └── requirements.txt              # Python dependencies
│
├── frontend/                         # React frontend application
│   └── front_m-main/
│       ├── src/
│       │   ├── App.jsx
│       │   ├── main.jsx
│       │   ├── components/           # React components
│       │   │   ├── AuthGuard.jsx
│       │   │   ├── DashboardLayout.jsx
│       │   │   ├── Header.jsx
│       │   │   └── Sidebar.jsx
│       │   ├── pages/                # Page components
│       │   │   ├── Login.jsx
│       │   │   ├── Register.jsx
│       │   │   ├── Dashboard.jsx
│       │   │   ├── Loans.jsx
│       │   │   ├── Predict.jsx
│       │   │   ├── PAN.jsx
│       │   │   ├── Connect.jsx
│       │   │   └── Landing.jsx
│       │   ├── lib/                  # Utility libraries
│       │   │   ├── api.js            # API client
│       │   │   ├── auth.js           # Auth utilities
│       │   │   └── utils.js
│       │   └── index.css
│       ├── package.json
│       ├── vite.config.ts
│       └── tsconfig.json
│
├── ml/                               # Machine learning pipeline
│   ├── src/
│   │   ├── train.py                 # Model training script
│   │   ├── evaluate.py              # Model evaluation
│   │   ├── scoring.py               # Scoring logic
│   │   ├── shap_explainer.py        # SHAP explanations
│   │   ├── feature_engineering.py   # Feature extraction & processing
│   │   ├── generate_dataset.py      # Synthetic data generation
│   │   └── utils.py
│   ├── data/
│   │   └── final_dataset.csv        # Training dataset
│   ├── artifacts/                   # Pre-trained models & configs
│   │   ├── metrics.json             # Model performance metrics
│   │   └── thresholds.json          # Decision thresholds
│   └── requirements.txt              # ML dependencies
│
├── docker/
│   └── docker-compose.yml            # Docker compose configuration
│
├── Readme.md                         # This file
└── md.ipynb                          # Jupyter notebook documentation
```

## Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker & Docker Compose (optional)
- PostgreSQL 15+ (or use Docker)

### 1. Clone Repository
```bash
git clone https://github.com/KaranSJ22/xai-gig-score.git
cd xai-gig-score
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend/front_m-main

# Install dependencies
npm install
# or
pnpm install
```

### 4. ML Pipeline Setup
```bash
cd ml

# Install ML dependencies
pip install -r requirements.txt
```

### 5. Database Setup

#### Using Docker Compose (Recommended)
```bash
cd docker
docker-compose up -d
```

#### Manual PostgreSQL Setup
```bash
# Create database
createdb gig_credit

# Update database URL in backend/app/config.py if needed
```

## Quick Start

### 1. Start Backend
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

API documentation: http://localhost:8000/docs

### 2. Start Frontend
```bash
cd frontend/front_m-main
npm run dev
# or
pnpm dev
```

Frontend will be available at: http://localhost:3000

### 3. Train ML Model (Optional)
```bash
cd ml

# Generate synthetic dataset
python src/generate_dataset.py

# Train model
python src/train.py

# Evaluate model
python src/evaluate.py
```

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Platform Data
- `GET /platform/` - Get connected platforms
- `POST /platform/connect` - Connect new platform
- `DELETE /platform/{id}` - Disconnect platform

### PAN Verification
- `POST /pan/verify` - Verify PAN details
- `GET /pan/{user_id}` - Get PAN details

### Predictions & Scoring
- `POST /predict/score` - Generate credit score
- `GET /predict/{prediction_id}` - Get prediction details
- `GET /predict/{prediction_id}/explain` - Get SHAP explanations

### Loans
- `GET /loans/` - List user loans
- `POST /loans/apply` - Apply for loan
- `GET /loans/{loan_id}` - Get loan details

### Dashboard
- `GET /dashboard/` - Get dashboard metrics
- `GET /dashboard/user-stats` - User statistics

## Development

### Running Tests
```bash
cd backend
pytest
```

### Code Style & Linting
```bash
# Backend
cd backend
black app/
flake8 app/

# Frontend
cd frontend/front_m-main
npm run lint
```

### Environment Variables

Create `.env` files in appropriate directories:

**backend/.env**
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/gig_credit
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**frontend/.env**
```
VITE_API_URL=http://localhost:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## Key Services

### Scoring Service
Calculates credit scores (300-900 scale) based on:
- Default probability prediction from ML model
- User's platform data and activity history
- Risk level classification

### Explain Service
Provides SHAP-based feature importance explanations:
- Individual feature contributions to predictions
- Feature labels and interpretability
- Visual explanations for end users

### Feature Engineering Service
Extracts and processes features:
- Income metrics (average, volatility, growth)
- Activity metrics (completion rate, tenure)
- Financial behavior (wallet transactions, savings)
- Platform engagement scores

### Model Service
Loads and uses pre-trained models:
- Default probability prediction
- Model artifacts management
- Batch prediction capabilities

## Model Details

**Algorithm**: XGBoost with SHAP for explainability

**Target Variable**: Default prediction (binary classification)

**Score Range**: 300-900 (higher is better)

**Risk Levels**:
- **Low Risk**: Score ≥ 750
- **Medium Risk**: Score 600-749
- **High Risk**: Score < 600

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- **Karan SJ** - Project Lead

## Acknowledgments

- SHAP library for explainability framework
- FastAPI for modern web framework
- React for frontend framework
- XGBoost for powerful ML model

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check documentation in `md.ipynb`
- Review API docs at `/docs` endpoint

---

**Last Updated**: May 2026
