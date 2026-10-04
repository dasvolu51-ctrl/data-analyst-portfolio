## **1\. The Flagship Project: Enterprise SaaS Revenue Intelligence & AI-Governed Semantic Layer**

This flagship project simulates an end-to-end enterprise deployment. It addresses the industry-wide **Text-to-SQL "production cliff"**—where enterprise LLM accuracy drops from 90% in academic tests to 15–21% on complex, real-world schemas—by demonstrating how modern analytics engineering and semantic layers create trusted data for both human executives and AI agents.

**Raw Multi-Source Data (10M+ Rows)**  
*(Stripe Billing Events, HubSpot CRM, Product Telemetry)*  
↓  
**High-Speed Ingestion & Zero-ETL Querying**  
*(DuckDB for Parquet/CSV \+ Polars Lazy Execution for EDA)*  
↓  
**Analytics Engineering & Transformation Layer**  
*(dbt Core: Star Schema, Data Quality Tests, Model Contracts)*  
↓  
**Governance & Semantic Layer**  
*(dbt Semantic Layer: Centralized Metric Definitions for MRR, Churn, LTV)*  
├── **Executive BI Dashboard** (Power BI DAX / Tableau Public)  
└── **AI Text-to-SQL Guardrail Testbench** (Benchmarking LLM Accuracy Against Semantic Rules)

### **Business Context & Commercial Problem**

* **Scenario:** A mid-market B2B SaaS platform experiences a structural 14% quarterly increase in churn alongside conflicting ARR/MRR numbers reported across sales, finance, and product teams.  
* **Commercial Metrics Tracked:** Monthly Recurring Revenue (MRR), Net Revenue Retention (NRR), Customer Acquisition Cost (CAC), Customer Lifetime Value (CLV), and Cohort Churn Rates.

### **Technical Execution by Layer**

#### **Layer 1: Data Ingestion & Transformation (DuckDB \+ Polars)**

* **Dataset:** 10M+ rows of synthetic/anonymized multi-table transactional event logs, subscription billing histories, and product usage telemetry stored as raw Parquet and CSV files.  
* **Execution:**  
  * Use **DuckDB** for zero-ETL querying directly against raw Parquet files, processing multi-million-row aggregations locally with low memory overhead (\~300 MB RAM).  
  * Use **Polars** with its lazy execution engine (pl.scan\_parquet) to construct optimized transformation pipelines, handling missing data, unnormalized strings, and sessionization across all CPU cores.  
  * *Why this wins:* Proves modern computational literacy over legacy, single-threaded Pandas workflows.

#### **Layer 2: Analytics Engineering & Semantic Modeling (dbt Core)**

* **Architecture:** Build a clean Dimensional Star Schema (Fact: fct\_subscription\_events, Dimensions: dim\_customers, dim\_plans, dim\_feature\_usage).  
* **Testing & Data Hygiene:** Implement schema assertions, primary/foreign key relationship tests, and dbt-expectations to flag anomalous billing records or null user keys.  
* **The dbt Semantic Layer:** Define enterprise KPIs (MRR, Active Subscribers, Churn) directly in YAML code. This ensures metric calculations remain identical whether queried by BI dashboards or generative AI interfaces.

#### **Layer 3: The AI Guardrail & Text-to-SQL Testbench**

* **The Problem Solved:** Enterprise LLMs hallucinate complex JOINs, invent nonexistent columns, and miscalculate business logic when querying raw schemas directly.  
* **Deliverable:** A Python script benchmarking a leading LLM (e.g., GPT-4, Claude) generating SQL queries against your raw database versus generating queries mediated by your **dbt Semantic Layer**.  
* **Documented Finding:** Show how semantic grounding and model contracts eliminate hallucinated JOINs and improve query accuracy from \~20% to \>90%.

#### **Layer 4: Executive BI Presentation (Power BI / Tableau)**

* **Layout:** Strict 3-tier visual hierarchy:  
  1. *Top Tier:* Executive KPI summary cards (MRR, Churn Rate %, NRR %, Quick Ratio).  
  2. *Middle Tier:* Interactive cohort retention heatmaps and ARR waterfall charts powered by custom DAX/LOD calculations.  
  3. *Bottom Tier:* Dimensional drill-downs isolating churn risk by customer industry, plan tier, and feature engagement.

## **2\. The Complete Three-Project Taxonomy**

To satisfy recruiter checklists in under ten seconds, pair the flagship project with two complementary, focused assets:

| Project | Archetype | Core Tech Stack | Primary Commercial Deliverable |
| :---- | :---- | :---- | :---- |
| **Project 1 (Flagship)** | **End-to-End Business Case & MDS** | DuckDB, Polars, dbt Core, Power BI/Tableau, LLM API | Production-grade SaaS retention model, semantic metrics repository, and AI Text-to-SQL validation bench. |
| **Project 2 (Advanced SQL)** | **Temporal Cohort & Financial Forensics** | PostgreSQL, Advanced SQL (CTEs, Window Functions) | Multi-table relational analysis using LEAD(), LAG(), and ROW\_NUMBER() to detect customer retention degradation and revenue leakage. |
| **Project 3 (Live Pipeline)** | **Automated Public API Dashboard** | Python, GitHub Actions, Public REST API, Tableau Public / Power BI Service | A continuously auto-refreshing public dashboard (e.g., energy grid demand, open logistics transit, or commodity pricing) demonstrating cloud pipeline maintenance. |

## **3\. GitHub Repository Hygiene & The Executive README**

Chaotic GitHub repositories with undocumented scripts trigger immediate disqualification. Organize each repository using a production-grade directory taxonomy:

├── .github/workflows/      \# CI/CD automated dbt testing or data refresh scripts  
├── assets/                 \# High-resolution dashboard screenshots & architecture diagrams  
├── dbt\_project/            \# dbt models, schema tests, and semantic layer metric YAMLs  
├── src/                    \# Modular, documented Python/Polars extraction scripts  
├── queries/                \# Formatted SQL queries with window functions and CTEs  
├── .gitignore              \# Ignores large raw files, local DuckDB instances, and credentials  
└── README.md               \# Executive Briefing Document

### **The 4-Part Executive README Template**

Format the README.md to be fully digested in 30 seconds:

1. **Business Problem:** Two concise sentences defining the commercial bottleneck and financial stakes.  
2. **Executive Findings:** Three bullet points summarizing key operational insights (supported by an embedded dashboard GIF or screenshot).  
3. **Architecture & Methodology:** A concise diagram detailing data flow through DuckDB, Polars, dbt, and the BI layer.  
4. **Actionable Recommendations:** Quantified strategic guidance (e.g., *"Reallocating customer success interventions to Tier-2 accounts at Month 3 reduces annual revenue churn by 3.2%, recovering \~\$180,000 in ARR"*).

## **4\. ATS Optimization Playbook**

To pass automated screening on platforms like Greenhouse, Workday, and Lever, apply strict layout and semantic rules:

* **Formatting Rules:** Use a single-column, clean layout without tables, graphic progress bars, or nested text boxes. Place the portfolio URL and GitHub profile link prominently in the top header.  
* **Mandatory Semantic Keywords:** Explicitly include exact skill keywords throughout the experience and project sections: dbt Core, DuckDB, Polars, Advanced SQL, Window Functions, Star Schema, Semantic Layer, Power BI (DAX), Data Governance, and Cohort Analysis.  
* **Impact Formula:** Structure bullet points as **\[Action Verb\] \+ \[Specific Modern Stack Tool\] \+ \[Measurable Business Metric/Scale\]**:  
  * *Example:* "Architected an automated dbt and DuckDB transformation pipeline across 12M+ transaction records, reducing daily query execution time by 65% and establishing a centralized semantic layer for enterprise churn reporting".

