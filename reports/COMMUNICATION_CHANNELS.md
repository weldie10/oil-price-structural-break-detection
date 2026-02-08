# Communication Channels and Formats by Stakeholder Group

## Structured Event Dataset

We have compiled a **concrete structured event dataset** in CSV format (`data/raw/oil_market_events.csv`) containing **22 major oil market events** (2001-2023), exceeding the minimum requirement of 10-15 events. 

### Dataset Structure

The CSV file includes the following columns:
- **event_date**: Precise dates for each event (YYYY-MM-DD format)
- **event_type**: Categorization (OPEC, Geopolitical, Economic, Natural Disaster, Market, etc.)
- **event_description**: Detailed descriptions of each event
- **impact_type**: Supply Shock, Demand Shock, Market, Geopolitical
- **severity**: High, Very High, Medium classifications
- **source_notes**: Additional context for each event

### Event Coverage

The dataset covers major market-moving events including:
- OPEC production decisions (9 events)
- Geopolitical events including wars and conflicts (6 events)
- Economic shocks including financial crises and pandemics (3 events)
- Natural disasters (1 event)
- Market events (2 events)
- Other significant events (1 event)

This structured dataset enables systematic correlation analysis between detected structural breaks and historical events.

---

## Communication Channels by Stakeholder Group

### 1. Investors

#### Primary Formats

**Executive Dashboard** (Interactive web-based, updated weekly)
- Real-time visualization of detected change points
- Risk heat maps showing volatility regimes
- Portfolio impact assessment tools
- Format: Interactive Plotly/Streamlit dashboard
- Delivery: Secure investor portal, email notifications

**Investment Brief** (2-3 pages, monthly)
- Key change points identified in the past month
- Regime transition probabilities
- Expected price range scenarios
- Trading strategy implications
- Format: PDF report with executive summary
- Delivery: Email distribution, investor portal

**Quarterly Investment Report** (15-20 pages)
- Comprehensive analysis of all detected breaks
- Historical event correlations
- Forward-looking regime probabilities
- Risk-adjusted return implications
- Format: Detailed PDF report with appendices
- Delivery: Email distribution, quarterly webinars

#### Key Messages for Investors

- **Timing of structural breaks** for entry/exit decisions
- **Volatility regime changes** affecting portfolio risk
- **Event-driven price movement patterns** for trading strategies
- **Uncertainty intervals** for risk management
- **Correlation vs. causation caveats** for investment decisions

#### Delivery Channels
- Email distribution lists
- Secure investor portal
- Quarterly webinars with Q&A sessions
- One-on-one consultations for high-value clients

---

### 2. Policymakers

#### Primary Formats

**Policy Brief** (3-5 pages, quarterly)
- Summary of structural breaks and associated events
- Policy intervention timing analysis
- Market stability assessment
- Energy security implications
- Format: PDF policy brief with visualizations
- Delivery: Official policy briefings, government portals

**Technical Appendix** (20-30 pages, annual)
- Complete methodology documentation
- Statistical validation of detected breaks
- Event correlation analysis
- Limitations and caveats (especially correlation vs. causation)
- Format: Comprehensive technical document
- Delivery: Government portals, official documentation

**Policy Presentation** (30-45 minutes)
- Slide deck for policy briefings
- Visual timeline of events and breaks
- Policy response effectiveness analysis
- Format: PowerPoint/PDF presentation
- Delivery: In-person briefings, parliamentary committees

#### Key Messages for Policymakers

- **Timing of structural breaks** relative to policy decisions
- **Market response** to policy interventions
- **Energy security risk periods** requiring attention
- **Correlation between geopolitical events** and price breaks
- **Critical**: Clear distinction between correlation and causation
- **Policy recommendation timing** based on regime transitions

#### Delivery Channels
- Official policy briefings
- Government portals and documentation systems
- Annual energy security reports
- Parliamentary committee presentations
- Inter-agency coordination meetings

---

### 3. Energy Companies

#### Primary Formats

**Strategic Planning Report** (10-15 pages, quarterly)
- Detected structural breaks and regime characteristics
- Production planning implications
- Supply chain risk assessment
- Capital allocation recommendations
- Format: PDF report with executive summary
- Delivery: Internal company portals, executive briefings

**Operational Dashboard** (Interactive, real-time)
- Current price regime identification
- Volatility forecasting
- Event impact assessment
- Supply/demand balance indicators
- Format: Web-based dashboard (Plotly/Streamlit)
- Delivery: Internal company portals, mobile access

**Risk Management Brief** (5-7 pages, monthly)
- Volatility regime changes
- Event-driven risk scenarios
- Hedging strategy recommendations
- Format: PDF brief with risk matrices
- Delivery: Risk management teams, executive summaries

**Technical Analysis Report** (20-25 pages, semi-annual)
- Detailed methodology and results
- Model diagnostics and validation
- Comparative analysis across different time periods
- Format: Comprehensive technical document
- Delivery: Technical teams, research departments

#### Key Messages for Energy Companies

- **Production planning** based on regime transitions
- **Supply chain risk** during high-volatility periods
- **Event-driven price shock probabilities** for operational planning
- **Optimal timing** for capital investments
- **Hedging strategy adjustments** based on detected breaks
- **Correlation patterns** for operational planning

#### Delivery Channels
- Internal company portals
- Executive briefings and board presentations
- Operational planning meetings
- Risk management committees
- Technical research departments

---

## Common Communication Formats

### 1. Executive Summary (1-2 pages)
- High-level overview for quick decision-making
- Key change points and regime characteristics
- Visual timeline of events and breaks
- Risk assessment summary
- **Format**: PDF, suitable for all stakeholders

### 2. Interactive Visualizations
- Time series plots with overlaid change points
- Event timeline visualizations
- Regime comparison charts
- Interactive dashboards (Plotly, Streamlit)
- **Format**: Web-based, accessible to all stakeholders

### 3. Jupyter Notebooks (for technical audiences)
- Reproducible analysis notebooks
- Step-by-step methodology
- Code and results together
- **Format**: Interactive notebooks, suitable for analysts and technical teams

### 4. Technical Reports
- Detailed methodology and model specifications
- Statistical results and diagnostics
- Model comparison and validation
- Full results tables and figures
- **Format**: PDF, comprehensive documentation

---

## Key Messages to Communicate (All Stakeholders)

1. **Change Point Locations**: When structural breaks occurred (with uncertainty intervals)
2. **Regime Characteristics**: How different periods differ (mean, volatility, trends)
3. **Event Associations**: Which events correlate with detected breaks
4. **Uncertainty Quantification**: Confidence levels in detected breaks
5. **Practical Implications**: What this means for decision-making
6. **Limitations**: **Clear statement that correlations do not prove causation** - critical for all stakeholders

---

## Communication Schedule

- **Weekly**: Interactive dashboards updated
- **Monthly**: Investment briefs, risk management briefs
- **Quarterly**: Policy briefs, strategic planning reports
- **Semi-Annual**: Technical analysis reports
- **Annual**: Comprehensive technical documentation

---

## Notes

- All communications emphasize the distinction between correlation and causation
- Uncertainty intervals are always included with change point estimates
- Event correlations are presented as associations, not causal relationships
- Technical details are provided in appendices for interested stakeholders
- Visualizations are prioritized for executive-level communications
