## Goal Description
This phase implements **Layer 4: The BI Presentation Layer**. We are completely ditching boring, standard Power BI dashboards. Instead, we are building a bespoke, high-performance web application that serves as the crown jewel of your portfolio. 

Leveraging the premium skills we installed (Framer Motion, Tailwind UI, React Hooks), this app will feature an elegant Burgundy and Cream color palette. It will present recruiters with a buttery-smooth Welcome Screen that transitions into a multi-tiered data experience (Tier 1 for Executives, Tier 2 for Managers, Tier 3 for Engineers). 

To ensure this can be hosted 100% free on GitHub Pages, we will write a Python bridge script that extracts the exact metrics from our dbt Semantic Layer and bakes them into the website as ultra-fast static JSON files.

## User Review Required
> [!IMPORTANT]
> Please review the exact tech stack and UI component architecture below. Once you hit **Proceed**, I will automatically generate the React app, install the animation libraries, and write the custom data visualization components!

## Proposed Changes

---

### 1. The Data Bridge (DuckDB to JSON)
We need to extract the "Single Source of Truth" from our semantic layer so the frontend can read it instantly.
#### [NEW] `C:\Users\Public\data_analyst_portfolio\presentation_layer\export_kpis.py`
A script that queries the `saas_metrics.duckdb` file to extract MRR, Churn, and Active Subscribers, and saves them directly into the React app's `public/data/` folder as `metrics.json`.

---

### 2. Frontend Framework & Dependencies
We will initialize a modern React environment optimized for premium animations and charting.
#### [NEW] `presentation_layer/package.json`
Key libraries installed:
*   `react` & `react-dom` (Core framework)
*   `tailwindcss` (For premium, utility-first styling)
*   `framer-motion` (For insane, buttery-smooth page transitions)
*   `recharts` (For the customized Green/Red profit & loss charts)
*   `lucide-react` (For premium iconography)

---

### 3. UI Component Architecture
We will build modular React components to manage the specific user journey you requested.

#### [NEW] `src/App.jsx`
The main routing engine that manages the state (Welcome Screen -> Tier Selection -> Data Views).
#### [NEW] `src/components/WelcomeScreen.jsx`
*   **Design:** Deep Burgundy background (`#800020`), Cream typography (`#FFFDD0`).
*   **Interaction:** A smooth fade-in welcome message and a pulsing entry button.
#### [NEW] `src/components/TierSelector.jsx`
*   Three distinct, beautifully animated cards (Tier 1: Execs, Tier 2: Managers, Tier 3: Engineers).
#### [NEW] `src/components/Tier1View.jsx`
*   **Focus:** Pure financial impact. Large, readable numbers.
*   **Charts:** Conditional formatting applied to `recharts`. If MRR is increasing, the chart fills with vibrant green; if churning, it alerts in red.
#### [NEW] `src/components/Tier2View.jsx`
*   **Focus:** Operational metrics (Active subscribers, cohort breakdowns). Minimal technical jargon.
#### [NEW] `src/components/Tier3View.jsx`
*   **Focus:** Deep dive. Shows the data alongside an explanation of the dbt Semantic Layer that generated it, proving your full-stack data capabilities.

## Verification Plan
### Automated Execution
Once approved, I will run the terminal commands to:
1. Initialize the Vite/React project in `presentation_layer`.
2. Run the `export_kpis.py` script.
3. Install `tailwindcss`, `framer-motion`, and `recharts`.
4. Write all the custom JSX component files.

### Manual Verification
I will start the local development server (`npm run dev`). You will be able to open `http://localhost:5173` in your browser to interact with the premium motions and verify the Burgundy/Cream aesthetics before we eventually deploy it to GitHub!
