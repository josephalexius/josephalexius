# Enterprise Investor Suitability Engine & Machine Learning Risk Platform
### Phase 1: SDLC System Automation | Phase 2: Predictive XGBoost Analytics Optimization

💻 **Tech Stack:** Python 3.9+ | Streamlit Cloud | GitHub CI/CD  
🌐 **Live App Instance:** [Launch Live Streamlit Analytics Application](https://streamlit.app)  
📂 **Repository Source:** [View GitHub Folder (/invqtoolv2)](https://github.com)

---

## 📌 Executive Summary & Business Case

### The Problem
Traditional wealth management client onboarding relies heavily on manual, paper-based questionnaires to evaluate subjective **"Risk Tolerance"** (how a client feels about losing money). This reliance on human intuition introduces significant cognitive bias, advisory calculation variance, and operational latency (processing backlogs). Furthermore, it fails to evaluate a client’s objective **"Risk Capacity"** (their actual statistical ability to afford a loss).

### The Solution
This platform bridges the gap by delivering a **two-layered investor suitability validation engine**:
1. **Phase 1 (Workflow Automation):** Digitizes client intake, reducing manual application processing times by **50%** through a structured, zero-defect calculation layer.
2. **Phase 2 (Predictive Reality Check):** Deploys an advanced **XGBoost Machine Learning Classifier** trained on empirical peer data to provide an unbiased, data-backed baseline for portfolio managers.

---

## 📉 Gap Analysis (Current State vs. Future State)


| Core Workflow Lifecycle | Current State (Manual Process) | Future State (Automated ML Platform) |
| :--- | :--- | :--- |
| **Intake Efficiency** | Physical paper forms processed face-to-face; manual data entry. | 100% digital client-facing browser instance; **50% reduction in processing time**. |
| **Scoring Integrity** | Advisors manually sum point sheets, introducing human error risks. | Algorithmic point-weight calculations executed instantaneously at runtime. |
| **Suitability Validation** | Portfolio allocation is based purely on subjective, client-reported metrics. | **XGBoost predictive layer** flags discrepancies between client feelings and empirical peer benchmarks. |
| **System Interoperability** | Paper applications batched and handcoded into systems at end-of-day. | Automated data persistent engine dumps normalized profiles straight to downstream **CSV schemas**. |

---

## 📋 System Requirements & Functional Specifications

The platform architecture was executed against formal corporate compliance requirements:
* **`BR-001`:** Build a responsive digital discovery questionnaire to capture investor goals.
* **`BR-002`:** Map a rigorous numerical point-weight matrix to answers to calculate runtime metrics.
* **`BR-003`:** Automatically categorize risk parameters (**Conservative, Moderate, Aggressive**).
* **`BR-004`:** Persist client state configurations directly to a downstream CSV schema for legacy core banking system ingestion.
* **`BR-ML-005`:** Construct a secondary predictive engine to serve as a decision-making guardrail for compliance audits.

---

## 📊 Data Engineering & Data Science Lifecycle (CRISP-DM)

### 1. Data Source & Dimensionality
The predictive engine utilizes the **USA Survey of Consumer Finances (SCF)**, a triennial cross-sectional financial study conducted by the **Federal Reserve Board**.
* **Dataset Scale:** 22,795 rows | 357 transactional feature columns.
* **Data Focus:** Household balance sheets, objective net worth, debt structures, income streams, and demographic metrics.

### 2. Preprocessing & Feature Engineering Pipelines
To handle real-world data imperfections, the ingestion pipeline executed the following steps:
* **Data Cleaning:** Resolved duplicate tracking IDs and handled missing data fields within pension/asset categories.
* **Class Imbalance Management:** Handled high dimensionality and category skewing through algorithmic alignment.
* **Outlier Detection:** Managed extreme net-worth values to insulate models from training distortion.
* **Feature Categorization:** Binned complex features (e.g., binning raw age into standard industry age clusters, `AGECL` 1–6) and encoded categorical arrays (occupation, family structures).

### 3. Model Training & Execution
An optimized **XGBoost Classifier** was deployed to analyze demographic and financial vectors, mapping empirical peer traits to objective target risk profiles. This provides a transparent, data-backed rationale for asset allocation to meet strict **Know Your Client (KYC)** regulatory standards.

---

## 🧪 Quality Assurance & Test Case Matrix

```text
┌───────────┬──────────────────────────────────┬─────────────────────────────────┬────────┐
│ Test ID   │ Functional Condition Checked     │ Expected Output Result          │ Status │
├───────────┼──────────────────────────────────┼─────────────────────────────────┼────────┤
│ TC-BA-001 │ Ingest low-score profile metrics │ System triggers 'Conservative'  │ PASSED │
│ TC-BA-002 │ Ingest mid-score profile metrics │ System triggers 'Moderate'      │ PASSED │
│ TC-BA-003 │ Ingest high-score profile metrics│ System triggers 'Aggressive'    │ PASSED │
│ TC-DA-004 │ Trigger CSV Persistence Pipeline │ Write clean, raw data schema    │ PASSED │
│ TC-ML-005 │ Ingest multi-dim demographic file│ XGBoost fires reality benchmark │ PASSED │
└───────────┴──────────────────────────────────┴─────────────────────────────────┴────────┘
```

---

## ☁️ Continuous Integration & Cloud Deployment
The deployment pipeline bridges version control directly with local application execution layers:
1. **Codebase Synchronization:** Developed and maintained files natively within the production-tracked `/invqtoolv2` folder.
2. **Infrastructure Dependency Isolation:** Orchestrated a custom `requirements.txt` manifest within the folder root to ensure deterministic library compilation (Pandas, NumPy, Streamlit, XGBoost).
3. **SaaS Continuous Delivery:** Integrated repository webhooks with the **Streamlit Community Cloud** platform to compile, host, and push software updates to the web production application instance on every master git commit.

---
*Developed as an advanced technical deliverable combining Software Engineering (SDLC) and Applied Data Science (CRISP-DM) principles at Algonquin College (2025-2026).*
