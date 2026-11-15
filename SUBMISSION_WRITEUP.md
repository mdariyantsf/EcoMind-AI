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

Test year: 2025 (365 days). Training: 3,652 days (2015 to 2024).

| Model | MAE | RMSE |
|---|---|---|
| Persistence baseline | 0.7525 | 1.0317 |
| Linear Regression | 0.6635 | 0.8904 |
| Random Forest | 0.6591 | 0.8931 |

Our baseline scored an MAE of 0.7525 kWh/m²/day. Random Forest scored 0.6591 (about 12.4% lower) and Linear Regression scored 0.6635 (about 11.8% lower) on the held-out 2025 data. The two machine learning models are very close to each other (Random Forest is slightly better on MAE, Linear Regression is slightly better on RMSE), so we do not claim that one is clearly better than the other. We tested on one year only.

**Seasonal results (MAE):** forecasts are harder in the monsoon.

| Season | Persistence | Linear Regression | Random Forest |
|---|---|---|---|
| Other months (243 days) | 0.6558 | 0.5797 | 0.5670 |
| Monsoon, June to September (122 days) | 0.9451 | 0.8304 | 0.8425 |

**Low-solar alert** (threshold 3.605 kWh/m²/day, the 25th percentile of training targets; 83 low-solar days in the test year):

| Alert source | Precision | Recall | F1 | Correct alerts | False alerts | Missed days |
|---|---|---|---|---|---|---|
| Random Forest | 0.661 | 0.470 | 0.549 | 39 | 20 | 44 |
| Persistence | 0.554 | 0.554 | 0.554 | 46 | 37 | 37 |

The Random Forest alert gives fewer false alarms but misses more low-solar days. Overall the F1 scores are almost the same, so the alert is a useful extra signal but not a reliable warning on its own.

**Where it fails:** the five largest Random Forest errors were 2025-05-29 (actual 0.817, predicted 4.948), 2025-05-27 (actual 7.243, predicted 4.058), 2025-03-20 (actual 2.853, predicted 5.827), 2025-07-17 (actual 1.715, predicted 4.673) and 2025-09-14 (actual 1.243, predicted 3.894). In every case the persistence baseline was also wrong by a similar amount. We think this happens because the model only sees today's weather, so it cannot anticipate a sudden cloud event or storm that appears the next day. This is a hypothesis, not a confirmed cause.

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
