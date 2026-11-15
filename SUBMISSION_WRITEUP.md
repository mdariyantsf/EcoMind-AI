# EcoMind AI

**Track:** Climate
**Team:** Ariyan Tausif (solo participant)

# The problem

Households in Dhaka, Bangladesh that use solar panels with a battery have to decide how much energy to use when the next day's sunshine is uncertain. Cloud cover, humidity and the monsoon change how much solar radiation reaches the ground from one day to the next. A household battery manager has no simple way to see a data-based estimate of tomorrow's solar resource before planning battery use.

# What we built

EcoMind AI is a Streamlit application for Dhaka.

- **Input:** today's solar radiation, temperature, cloud amount and relative humidity (NASA POWER daily data, or values typed in by the user).
- **Output:** a forecast of tomorrow's solar radiation (kWh/m²/day) and a low-solar alert if the forecast is below a threshold.
- **User:** a household solar-battery manager in Dhaka, who uses the alert as an extra signal when deciding whether to review the battery-use plan for the next day.

The app does not predict the electricity a specific panel produces and does not control batteries.

# What we added

We started from the suggested project "Next-day solar energy forecast" and added:

1. **Our own user and place:** a Dhaka household battery manager, with a decision the forecast supports.
2. **Our own questions:** does the forecast work differently in the monsoon (June to September) than in other months, and can a low-solar alert (25th percentile of training targets) catch low-sun days better than a simple persistence alert?
3. **Failure analysis:** the five largest forecast errors in the test year.

# How it works

**Data:** NASA POWER daily API for Dhaka (23.8103 N, 90.4125 E), 2015-01-01 to 2025-12-31. Variables: ALLSKY_SFC_SW_DWN, T2M, CLOUD_AMT, RH2M. Missing values (-999) are set to missing, not zero. Every calendar day is kept, so "tomorrow" is always the next calendar day.

**Split:** chronological. All target years before the last year are used for training. The most recent target year is the test set. Days are never shuffled.

**Models:** persistence baseline (tomorrow = today), Linear Regression, and Random Forest (250 trees, max depth 12). The low-solar threshold is calculated from training targets only.

# Results

Test-set results were produced by the application on the held-out test year. Baseline: persistence (tomorrow = today). Metrics: MAE and RMSE in kWh/m²/day.

<!-- PASTE THE REAL RESULTS FROM THE APP HERE (see instructions in chat): model table, baseline vs best model, seasonal MAE, low-solar alert precision/recall/F1 and the five largest errors. -->

**Where it fails:** see the five largest Random Forest errors above. Possible reasons are rapid weather changes, unusual cloud conditions and the limited input features. These are hypotheses, not confirmed causes.

*This project is a research prototype. NASA POWER data are gridded data products, not measurements from a household panel, and the forecasts are estimates that may be wrong.*

# What we'd do next

1. Test more input features and longer forecast horizons (one to seven days).
2. Convert forecast radiation to expected electricity for a real panel system and try the alert with a real household's energy-use plan.

# Sources

- NASA POWER (data): https://power.larc.nasa.gov/ and https://power.larc.nasa.gov/docs/
- scikit-learn (models): https://scikit-learn.org/stable/
- pandas: https://pandas.pydata.org/ and NumPy: https://numpy.org/
- Plotly (charts): https://plotly.com/python/
- Streamlit (application): https://streamlit.io/
- Requests: https://requests.readthedocs.io/
- AI tool: OpenAI ChatGPT was used as a coding and development assistant (https://chatgpt.com/). Claude (Anthropic, https://claude.ai/) was used to review the project against the hackathon rules and to help fix the code and write-up. The team member reviewed and understands the project.
- Code: https://github.com/mdariyantsf/EcoMind-AI
