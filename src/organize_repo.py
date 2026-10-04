import os
import shutil

root_dir = r"C:\Users\Public\data_analyst_portfolio"

# 1. Create target directories
dirs = [
    ".github/workflows",
    "assets",
    "dbt_project",
    "src",
    "queries",
    "docs_and_plans"
]
for d in dirs:
    os.makedirs(os.path.join(root_dir, d.replace('/', os.sep)), exist_ok=True)

# 2. Move source scripts to src/
src_files = [
    (r"raw_data\generate_synthetic_data.py", "generate_synthetic_data.py"),
    (r"clean_data\clean_data.py", "clean_data.py"),
    (r"dbt_semantic_layer\llm_benchmark_simulation.py", "llm_benchmark_simulation.py"),
    ("install_global_skills.py", "install_global_skills.py"),
    ("build_website.py", "build_website.py"),
    ("setup_dbt.py", "setup_dbt.py")
]
for old_rel, new_name in src_files:
    old_path = os.path.join(root_dir, old_rel)
    if os.path.exists(old_path):
        shutil.move(old_path, os.path.join(root_dir, "src", new_name))

# 3. Move dbt project
stars_schema = os.path.join(root_dir, "stars_schema")
if os.path.exists(stars_schema):
    for item in os.listdir(stars_schema):
        shutil.move(os.path.join(stars_schema, item), os.path.join(root_dir, "dbt_project", item))
    os.rmdir(stars_schema)

# 4. Consolidate raw data and markdown notes
os.makedirs(os.path.join(root_dir, "data"), exist_ok=True)
for data_folder in ["raw_data", "clean_data", "dbt_semantic_layer"]:
    folder_path = os.path.join(root_dir, data_folder)
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            s = os.path.join(folder_path, item)
            if os.path.isfile(s) and (s.endswith(".csv") or s.endswith(".parquet") or "Benchmark" in s):
                shutil.move(s, os.path.join(root_dir, "data", item))
        try:
            os.rmdir(folder_path)
        except Exception:
            pass

# 5. Copy artifacts (plans and walkthroughs) from the brain directory
brain_dir = r"C:\Users\dasvo\.gemini\antigravity\brain\959205ce-f5c9-47de-8a34-25b1068a4b49"
dest_docs = os.path.join(root_dir, "docs_and_plans")
if os.path.exists(brain_dir):
    for file in os.listdir(brain_dir):
        if file.endswith(".md"):
            shutil.copy(os.path.join(brain_dir, file), os.path.join(dest_docs, file))

# 6. Create custom .gitignore
gitignore_content = """# Data files
*.parquet
*.csv
*.duckdb
data/

# Environments
.venv/
__pycache__/

# Node
node_modules/
"""
with open(os.path.join(root_dir, ".gitignore"), "w", encoding="utf-8") as f:
    f.write(gitignore_content)

# 7. Create Custom Executive README
readme_content = """# Data Engineering & BI Portfolio

## Executive Summary
This repository contains a full end-to-end data analytics portfolio. It demonstrates the ability to ingest 10M+ rows of messy synthetic data, clean it using Polars and DuckDB, model it via dbt Core, and serve it to an AI Text-to-SQL testbench and a bespoke React web application.

## Repository Taxonomy
* **src/**: Python scripts for data generation, zero-ETL cleaning, and AI benchmarking.
* **dbt_project/**: The Dimensional Star Schema and MetricFlow Semantic Layer.
* **presentation_layer/**: The zero-build React dashboard utilizing Framer Motion and Recharts.
* **queries/**: Analytical SQL queries.
* **docs_and_plans/**: Technical design documents, architecture plans, and walkthroughs.
* **data/**: Ignored directory for local Parquet and CSV files.
"""
with open(os.path.join(root_dir, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_content)

print("Repository successfully reorganized!")
