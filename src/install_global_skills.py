import os

# Define the global skills directory
GLOBAL_SKILLS_DIR = r"C:\Users\dasvo\.gemini\config\skills"
os.makedirs(GLOBAL_SKILLS_DIR, exist_ok=True)

# Define the Top 20 Premium Website Skills
web_skills = {
    "web-accessibility-auditor": "Ensures WCAG AAA compliance, ARIA labels, and semantic HTML for premium accessibility.",
    "web-performance-optimizer": "Optimizes Core Web Vitals (LCP, FID, CLS), lazy loading, and asset minification.",
    "seo-metadata-expert": "Implements advanced JSON-LD schema markup, Open Graph tags, and structured data.",
    "tailwind-ui-architect": "Designs breathtaking, spacing-perfect UIs using advanced Tailwind CSS configurations.",
    "react-hooks-master": "Writes highly optimized custom React hooks to prevent re-renders and manage state.",
    "framer-motion-animator": "Creates buttery-smooth layout transitions and micro-interactions using Framer Motion.",
    "responsive-design-tester": "Guarantees pixel-perfect fluidity from 320px mobile screens to 4K ultrawide displays.",
    "typography-specialist": "Establishes premium typographic scales, fluid font sizing, and elegant font pairing.",
    "color-theory-generator": "Generates accessible, premium color palettes with exact HSL/OKLCH interpolation.",
    "threejs-3d-integrator": "Embeds lightweight WebGL and Three.js 3D models for immersive scrolling experiences.",
    "nextjs-ssr-strategist": "Architects Next.js App Router for optimal Server-Side Rendering and static caching.",
    "webgl-shader-artist": "Writes custom GLSL shaders for premium background distortions and hover effects.",
    "svg-animation-creator": "Builds and animates complex vector graphics that scale infinitely without quality loss.",
    "dark-mode-implementer": "Engineers flashless, system-aware light/dark mode toggles with CSS variables.",
    "stripe-checkout-builder": "Designs frictionless, high-converting Stripe payment flows with premium UI.",
    "auth-flow-designer": "Creates secure, magic-link and OAuth authentication flows with elegant state feedback.",
    "web-security-auditor": "Hardens websites against XSS, CSRF, and enforces strict Content Security Policies.",
    "microcopy-writer": "Drafts premium, brand-aligned UX writing for buttons, tooltips, and empty states.",
    "custom-cursor-designer": "Implements physics-based custom cursors that react to DOM elements on hover.",
    "loading-state-architect": "Designs skeleton loaders and staggered entrance animations for zero-latency feel."
}

# Define the Top 20 Data Analyst Skills
data_skills = {
    "dbt-semantic-layer-expert": "Defines enterprise KPIs (MRR, Churn) perfectly via MetricFlow and dbt YAML.",
    "duckdb-zero-etl": "Writes blazing fast zero-ETL SQL queries directly against raw Parquet and CSV files.",
    "polars-pipeline-builder": "Constructs lazy-executed Polars dataframes to process gigabytes of data instantly.",
    "sql-query-optimizer": "Refactors slow SQL using CTEs, window functions, and indexing strategies.",
    "tableau-dashboard-designer": "Designs executive-level Tableau visualizations with high data-ink ratios.",
    "powerbi-dax-master": "Calculates complex time-intelligence metrics using advanced DAX expressions.",
    "statistical-significance-tester": "Validates A/B test results using T-tests, Z-scores, and p-value analysis.",
    "anomaly-detection-engineer": "Builds statistical algorithms (Isolation Forests, Z-scores) to flag bad data.",
    "data-storytelling-guide": "Transforms raw metrics into compelling, executive-ready narrative structures.",
    "snowflake-cost-optimizer": "Analyzes query profiles to reduce Snowflake compute costs and warehouse sizing.",
    "pandas-memory-manager": "Optimizes Pandas data types and chunks to prevent out-of-memory crashes.",
    "time-series-forecaster": "Predicts future revenue and traffic using ARIMA, Prophet, and moving averages.",
    "churn-prediction-modeler": "Applies survival analysis and logistic regression to identify at-risk customers.",
    "cohort-analysis-builder": "Constructs triangulated retention matrixes and cohort drop-off curves.",
    "funnel-conversion-tracker": "Analyzes multi-step user journeys to pinpoint exact UX friction points.",
    "mrr-financial-auditor": "Calculates strict SaaS financial metrics (Expansion, Contraction, Reactivation).",
    "data-catalog-documenter": "Maintains meticulous data dictionaries and column-level lineage metadata.",
    "geospatial-data-mapper": "Maps customer density and spatial clustering using PostGIS and Kepler.gl.",
    "graph-network-analyst": "Analyzes user relationships and node centrality using NetworkX and graph theory.",
    "data-cleaning-specialist": "Uses advanced Regex and imputation techniques to scrub highly corrupted datasets."
}

def create_skill(name, description, category):
    skill_dir = os.path.join(GLOBAL_SKILLS_DIR, name)
    os.makedirs(skill_dir, exist_ok=True)
    
    content = f"""---
name: {name}
description: {description}
---

# {name.replace('-', ' ').title()}

## Role Definition
You are an expert in {name.replace('-', ' ')}. When this skill is invoked, you must apply the highest industry standards to achieve premium, enterprise-grade results.

## Execution Guidelines
1. **Understand Context:** Always analyze the user's current codebase or dataset before executing.
2. **Apply Best Practices:** Do not take shortcuts. Use production-ready logic (e.g., error handling, accessibility, statistical rigor).
3. **Document Results:** Clearly explain your methodology, assumptions, and why your solution is optimal.

*This is a globally installed `{category}` skill, allowing you to utilize these capabilities across any workspace or project.*
"""
    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(content)

# Generate all 40 global skills
print("Installing Top 20 Premium Website Skills...")
for name, desc in web_skills.items():
    create_skill(name, desc, "Web Development")
    print(f" [OK] Installed: {name}")

print("\nInstalling Top 20 Data Analyst Skills...")
for name, desc in data_skills.items():
    create_skill(name, desc, "Data Analytics")
    print(f" [OK] Installed: {name}")

print("\nAll 40 premium skills have been successfully installed to the global Antigravity configuration directory!")
