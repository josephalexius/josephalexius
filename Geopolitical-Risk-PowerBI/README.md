# Geopolitical Conflict Intelligence Pipeline & Enterprise Data Model
### Domain: Geopolitical Risk Intelligence & Market Volatility Modeling
### Data Source: Armed Conflict Location & Event Data Project (ACLED)

## 📌 Interactive Visual Dashboard (Master Executive View)
Below is the unified master interface engineered to analyze global crisis indicators, resource disruptions, humanitarian impacts, and multi-stream macro-metrics simultaneously using verified ACLED historical data feeds:

![Crisis Overview Power BI Dashboard](Overall-Dashboard.png)

---

## 📐 Data Architecture & Schema Topology (Master ERD View)
Below is the comprehensive architectural blueprint of the operational database, demonstrating relational integrity across a multi-dimensional normalized structure:

![Data Model Schema View](Overall-Snowflake-Schema.png)

---

## 📐 Data Warehousing Strategy: Normalized Snowflake Schema
To minimize data redundancy, optimize storage footprints, and strictly enforce relational hierarchy across complex geospatial data, this production architecture utilizes a highly scalable **Snowflake Schema** design. 

### 1. Centralized Fact Layer (Cross-Functional Data Streams)
To simulate an enterprise Agile data warehouse environment, individual team members acted as decentralized stream owners. Disparate transactional feeds from ACLED were isolated into five optimized Fact Tables to track independent business indicators, unified via a centralized relational mapping matrix:
* **`Joseph - FACT Conflict Events`:** Captures discrete event records, global actors, operational methods, and localized intensity vectors.
* **`Hisham - FACT Economic Impact`:** Tracks quantifiable macroeconomic damage, trade disruptions, property loss, and systemic financial costs.
* **`Rayan - FACT Humanitarian Impact`:** Quantifies human-cost metrics, casualties, media coverage indicators, and internal displacement data.
* **`Hala - FACT International Response`:** Registers external diplomatic interventions, responding organizations, aid delivery streams, and service impacts.
* **`Youssra - FACT Infrastructure Damage`:** Identifies structural destruction, critical asset impacts, and damage assessment classifications.

### 2. Normalized Dimension Layer (Sub-Dimensional Relationships)
Unlike a basic flat Star Schema, this architecture explicitly normalizes low-cardinality attributes into lookup tables (sub-dimensions) to achieve a clean **Snowflake** topology:
* **Temporal Tracking (`Dim_Time`):** A unified date and time dimension serving as the core baseline for cross-functional trend analysis.
* **Geographic Topography (`Dim_Location`):** Standardizes geospatial coordinates and national/regional boundaries to maintain zero data variance across streams.
* **Target Contexts (`Dim_Actor`, `Dim_Conflict_Methods`, `Dim_Media_Coverage`):** Normalizes qualitative threat characteristics, political entities, and operational vectors across all active processing channels.

### ⚙️ Relational Integrity & Filter Control
* **Cardinality Constraints:** All primary-to-foreign key joins are strictly set to **1-to-Many (1:*)**, eliminating risks of data duplication or structural inflation at runtime.
* **Directional Filtering:** Configured with **Single-Directional Filter Propagation** flowing directly from Dimension tables to Fact tables. This protects tabular engine memory performance and prevents circular cross-filtering dependency errors.

---

## 🛠️ Data Lifecycle & Engineering
* **BI Platform Architecture:** Microsoft Power BI Desktop
* **Data Wrangling Layer:** Power Query (M Language) utilized for structural pivoting, relational column mapping, and database normalization.
* **Calculation Automation Layer:** Implemented an isolated measures container (`Measure` folder) to aggregate cross-table KPIs natively without bloating transactional rows.

## 📂 Project Artifacts Included
* `Geopolitical-Risk.pbix` - Complete Power BI production file containing active transactional schema maps.
* `Overall-Dashboard.png` - Master executive interface visualization.
* `Overall-Snowflake-Schema.png` - Complete Entity-Relationship Diagram (ERD) topology visualization.
