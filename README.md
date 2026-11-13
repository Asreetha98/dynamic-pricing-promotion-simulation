# Dynamic Pricing and Promotion Simulation System

A full-stack data-driven pricing and promotion simulation platform that analyses product costs, demand, inventory levels, and competitor prices to recommend profitable selling prices and evaluate promotional strategies while maintaining minimum profit margin constraints.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Project Objectives](#project-objectives)
- [Key Features](#key-features)
- [System Workflow](#system-workflow)
- [Technology Stack](#technology-stack)
- [Business Rules and Calculations](#business-rules-and-calculations)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Database Design](#database-design)
- [Core Modules](#core-modules)
- [Expected Outcomes](#expected-outcomes)

---

## Project Overview

The **Dynamic Pricing and Promotion Simulation System** is designed to help businesses make informed pricing decisions by considering multiple business factors, including product cost, customer demand, available inventory, competitor pricing, and promotional discounts.

Instead of relying on fixed pricing strategies, the system simulates different pricing scenarios and evaluates their potential impact on revenue, profitability, and inventory performance.

The platform provides a centralized interface to manage products, monitor inventory, record competitor prices, configure promotions, simulate pricing decisions, and analyse historical results.

The system is intended as a decision-support and simulation platform. It recommends and evaluates pricing strategies rather than automatically changing prices on external marketplaces.

---

## Problem Statement

Businesses frequently face challenges in determining competitive product prices while maintaining profitability.

Setting prices too high may reduce demand and sales, whereas setting prices too low may negatively affect profit margins. Promotional discounts can increase sales but may also result in losses when pricing constraints are not properly considered.

The proposed system addresses these challenges by combining demand analysis, inventory information, competitor observations, cost data, and promotion rules into a unified pricing simulation process.

---

## Project Objectives

- Develop a centralized product and pricing management system.
- Analyse demand and inventory information for pricing decisions.
- Compare internal product prices with competitor observations.
- Calculate minimum permissible selling prices based on margin requirements.
- Simulate promotional discounts and evaluate their profitability.
- Detect invalid pricing decisions and promotion rule violations.
- Maintain historical pricing decisions for traceability.
- Generate analytical reports to evaluate revenue and profitability.

---

## Key Features

### 1. User Authentication and Access

- Login and registration interfaces.
- Secure password handling.
- User account management.
- Access to relevant application modules based on user roles.

### 2. Product Management

- Add, update, view, and manage products.
- Maintain SKU, category, cost, and selling price information.
- Track product-level pricing information.

### 3. Inventory Management

- Maintain available stock information.
- Monitor stock levels.
- Identify low-stock and excess-stock products.
- Use inventory information during pricing simulations.

### 4. Competitor Price Analysis

- Record competitor product prices.
- Compare competitor prices with internal selling prices.
- Identify price differences.
- Consider the freshness of competitor observations before using them.

### 5. Dynamic Pricing Engine

- Calculate recommended selling prices.
- Consider product cost and minimum margin requirements.
- Evaluate competitor prices and demand conditions.
- Identify prices that violate profitability constraints.

### 6. Promotion Management

- Create and manage promotional campaigns.
- Configure discount percentages and validity periods.
- Define promotion eligibility and stacking restrictions.
- Evaluate the impact of discounts on final selling prices and profit margins.

### 7. Pricing Simulation

- Select a product and simulate different pricing scenarios.
- Apply promotional discounts.
- Calculate final selling price and expected profit margin.
- Generate a decision status: Approved, Rejected, or Manual Review.

### 8. Decision History

- Store historical pricing decisions.
- Maintain recommended prices and applied promotions.
- Record decision status and reasons.
- Support comparison of previous simulation results.

### 9. Dashboard and Analytics

- Display key business performance indicators.
- Analyse revenue and gross profit.
- Monitor average selling price and discount rates.
- Visualize inventory and pricing trends.
- Evaluate promotion performance and pricing compliance.

---

## System Workflow

1. Product and cost information is maintained in the database.
2. Inventory snapshots and competitor observations are recorded.
3. The system retrieves relevant product information.
4. Demand, stock availability, and competitor prices are analysed.
5. The pricing engine calculates a candidate selling price.
6. The promotion engine evaluates applicable discounts and promotion rules.
7. The decision engine checks minimum margin and other business constraints.
8. The system generates an Approved, Rejected, or Manual Review result.
9. The decision and its explanation are stored in the database.
10. Dashboard and reports display the simulation results.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, Vite, JavaScript, CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Processing | Pandas, NumPy |
| Data Generation | Python, Faker |
| Data Visualization | Recharts |
| API Testing | Postman, Swagger UI |
| Development Environment | Visual Studio Code |
| Version Control | Git and GitHub |

---

## Business Rules and Calculations

The system uses the following pricing calculations to evaluate profitability.

**1. Profit**

`Profit = Selling Price - Product Cost`

**2. Profit Margin**

`Profit Margin = (Profit / Selling Price) × 100`

**3. Minimum Permissible Selling Price**

`Minimum Price = Product Cost / (1 - Required Margin)`

**4. Discounted Selling Price**

`Discounted Price = Original Price × (1 - Discount Rate)`

**5. Revenue**

`Revenue = Selling Price × Quantity Sold`

**6. Gross Profit**

`Gross Profit = Revenue - Cost of Goods Sold`

### Pricing Decision Rules

| Condition | Decision |
|---|---|
| Final margin meets the minimum requirement | Eligible for approval |
| Price falls below the minimum permissible price | Rejected |
| Promotion stacking violates configured rules | Rejected |
| Competitor observation is outdated | Manual Review |
| Required pricing information is missing | Manual Review |
| Pricing decision does not contain a valid reason | Manual Review |

All profit margin checks must be performed using the final price after applying eligible discounts.

---

## Project Structure

The project is organized into three independent folders to support modular development and easier integration.

```text
Dynamic-Pricing-Simulation/
│
├── Frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
├── Backend/
│   ├── app/
│   │   ├── config/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   ├── generator/
│   ├── tests/
│   ├── requirements.txt
│   └── .env
│
├── Database/
│   ├── schema/
│   ├── seed/
│   ├── sample_data/
│   └── migrations/
│
├── docs/
│   ├── project-overview.md
│   ├── system-workflow.md
│   └── architecture.md
│
├── .gitignore
└── README.md
```

---

## Installation and Setup

### Prerequisites

Install the following tools before running the project:

| Tool | Purpose |
|---|---|
| Python 3.12+ | Backend development |
| Node.js and npm | Frontend development |
| PostgreSQL | Database management |
| Git | Version control |
| Visual Studio Code | Development environment |

Check the installed versions:

```bash
python3 --version
node --version
npm --version
psql --version
git --version
```

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Asreetha98/dynamic-pricing-promotion-simulation.git

cd dynamic-pricing-promotion-simulation
```

### Step 2 — Set Up the Database

Create the PostgreSQL database:

```sql
CREATE DATABASE dynamic_pricing_db;
```

Execute the SQL schema files from the `Database/schema/` directory in the appropriate dependency order.

Configure the database connection string in the backend environment file.

Example:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/dynamic_pricing_db
```

Replace the example password with your local PostgreSQL password.

### Step 3 — Set Up the Backend

```bash
cd Backend

python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

### Step 4 — Set Up the Frontend

Open another terminal:

```bash
cd Frontend

npm install

npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

### Step 5 — Run the Application

Ensure PostgreSQL, the backend API, and the frontend development server are running.

Open the frontend URL in your browser to access the application.

---

## Database Design

The database is designed to maintain product information, pricing records, inventory details, competitor observations, promotions, and simulation decisions.

| Table | Purpose |
|---|---|
| Products | Stores product details |
| CostRecords | Maintains product cost information |
| PriceHistory | Stores historical selling prices |
| InventorySnapshots | Maintains stock-level records |
| CompetitorObservations | Stores observed competitor prices |
| Promotions | Stores promotional campaign details |
| PromotionRules | Defines promotion conditions and restrictions |
| Orders | Stores order information |
| OrderItems | Stores individual products associated with orders |
| PricingDecisions | Maintains pricing simulation results |
| DecisionPromotions | Maps promotions applied to pricing decisions |

The database uses primary keys, foreign keys, constraints, and relationships to maintain data consistency and historical traceability.

---

## Core Modules

| Module | Responsibility |
|---|---|
| Authentication Module | User login and access management |
| Product Module | Product and cost information |
| Inventory Module | Stock-level management |
| Competitor Analysis Module | Competitor price comparison |
| Demand Analysis Module | Demand-related analysis |
| Pricing Engine | Candidate price calculation |
| Promotion Engine | Discount and promotion validation |
| Decision Engine | Approval, rejection, and exception handling |
| Analytics Module | Business performance reporting |
| Data Generator | Generation of synthetic business data |

---

## Expected Outcomes

The proposed system aims to:

- Improve pricing decision-making through data analysis.
- Maintain profitability using minimum margin constraints.
- Evaluate promotional strategies before implementation.
- Identify pricing exceptions and invalid discount combinations.
- Improve visibility into inventory and competitor pricing.
- Maintain a traceable history of pricing simulations.
- Support business decisions through interactive dashboards and reports.
