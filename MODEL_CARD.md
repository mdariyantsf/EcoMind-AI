# EcoMind AI — Model Card

## 1. Model overview

**Project:** EcoMind AI  
**Purpose:** Next-day solar-radiation forecasting and household solar-battery decision support  
**Research location:** Dhaka, Bangladesh  
**Creator:** Ariyan Tausif  
**Primary data source:** NASA POWER Daily API

EcoMind AI estimates the next calendar day's surface solar radiation from the current day's solar and weather observations. It is designed as an additional information source for planning, not as a guarantee of solar electricity production or household power availability.

## 2. Intended use

Appropriate uses include:

- Exploring next-day solar-resource conditions for Dhaka.
- Comparing machine-learning forecasts with a simple persistence baseline.
- Reviewing seasonal differences in forecast error.
- Providing an additional signal when a household solar-battery manager reviews an energy-use plan.
- Educational demonstrations of time-ordered environmental forecasting.

The forecast should be considered alongside local weather information, actual system monitoring, battery state of charge, and professional advice where relevant.

## 3. Out-of-scope uses

EcoMind AI is not designed to:

- Guarantee electricity generation, battery availability, or uninterrupted power.
- Automatically control an inverter, battery, or electrical installation.
- Replace an on-site solar assessment or an installer’s engineering calculations.
- Provide a bankable energy-yield estimate or financial guarantee.
- Forecast locations other than Dhaka unless the data pipeline and model are retrained and independently evaluated for those locations.

## 4. Data

The application requests daily data from the NASA POWER Daily API for the Dhaka point location:

- Latitude: 23.8103
- Longitude: 90.4125
- Period currently configured in `app.py`: 2015-01-01 to 2025-12-31

| NASA POWER parameter | Internal column | Description |
|---|---|---|
| `ALLSKY_SFC_SW_DWN` | `solar_radiation` | All-sky surface shortwave downward radiation |
| `T2M` | `temperature` | Temperature at 2 metres |
| `CLOUD_AMT` | `cloud_amount` | Cloud amount |
| `RH2M` | `humidity` | Relative humidity at 2 metres |

The target is the following day's `solar_radiation`, reported by the application in kWh/m²/day.

NASA POWER provides gridded/reanalysis-based environmental data products. These are not measurements from an individual rooftop or solar-panel installation. Missing-value codes such as `-999` are converted to missing values by the application.

## 5. Model inputs and target

The current-day input features configured in `app.py` are:

- `solar_today`
- `temperature`
- `cloud_amount`
- `humidity`

The target is the next calendar day's solar radiation.

The dataset is ordered by date and reindexed to a daily calendar before the next-day target is created. This helps ensure that the shifted target represents the next calendar day rather than simply the next available observation.

## 6. Compared methods

### Persistence baseline

Assumes tomorrow's solar radiation will equal today's solar radiation.

### Linear Regression

A scikit-learn pipeline using median imputation, standard scaling, and linear regression.

### Random Forest

A scikit-learn pipeline using median imputation and `RandomForestRegressor` with the parameters currently configured in `app.py`:

- `n_estimators=250`
- `max_depth=12`
- `min_samples_leaf=3`
- `random_state=42`
- `n_jobs=-1`

These are the repository's current implementation settings, not a claim that they are globally optimal.

## 7. Evaluation design

The application uses chronological evaluation:

- Earlier target years are used for training.
- The latest available target year is held out for testing.
- Rows are not randomly shuffled.
- All three methods are evaluated on the same held-out period.

The repository's current generated results report:

- Data period: 2015-01-01 to 2025-12-31
- Training rows: 3,652
- Test year: 2025
- Test rows: 365

Metrics:

| Method | MAE (kWh/m²/day) | RMSE (kWh/m²/day) |
|---|---:|---:|
| Persistence baseline | 0.7525 | 1.0317 |
| Linear Regression | 0.6635 | 0.8904 |
| Random Forest | 0.6591 | 0.8931 |

On this reported test period, Random Forest has the lowest MAE, while Linear Regression has the lowest RMSE. The results do not establish that one model will perform best in future years or at other locations.

## 8. Seasonal analysis

The current application groups target dates into:

- Monsoon: June–September
- Other months: January–May and October–December

Reported MAE:

| Season | Persistence | Linear Regression | Random Forest | Test days |
|---|---:|---:|---:|---:|
| Other months | 0.6558 | 0.5797 | 0.5670 | 243 |
| Monsoon | 0.9451 | 0.8304 | 0.8425 | 122 |

The higher reported errors during the monsoon period indicate that forecasting was more difficult in that portion of this test year. This is an observation from one held-out year, not a universal climate conclusion.

## 9. Low-solar alert evaluation

The current application defines a low-solar threshold using the 25th percentile of training-period target values. The reported threshold is **3.605 kWh/m²/day**.

Reported Random Forest alert metrics:

- Precision: 0.6610
- Recall: 0.4699
- F1: 0.5493
- Correct alerts: 39
- False alerts: 20
- Missed low-solar days: 44

The persistence alert is also evaluated in the generated results file. These metrics describe the held-out test period and should not be interpreted as a guarantee for future alerts.

## 10. Known limitations and risks

1. **Single location:** The current model is configured for Dhaka only.
2. **Gridded data:** NASA POWER data do not represent measurements at a specific rooftop.
3. **Limited features:** The model uses four current-day features. It does not currently include a full numerical weather forecast, panel geometry, shading, or local microclimate measurements.
4. **Forecast uncertainty:** The app returns point predictions; it does not currently provide calibrated prediction intervals.
5. **Changing conditions:** Unusual weather, data gaps, or climate variability can increase errors.
6. **Solar resource is not electricity:** Solar radiation in kWh/m²/day is not the same as the electricity produced by a panel in kWh/day.
7. **Single test year:** The current reported test uses 2025. Additional rolling-origin or multi-year backtesting would provide stronger evidence.
8. **No operational control:** The project does not connect to or control real electrical equipment.

## 11. Solar Energy Estimator relationship

The separate `solar_calculator.py` module provides a transparent, assumption-based estimate:

`estimated_energy_kwh = panel_capacity_kwp × solar_irradiation_kwh_m2_day × performance_ratio`

It uses the forecast radiation as a simplified irradiation proxy. Since the current forecast is based on surface radiation and does not model panel tilt, azimuth, shading, or plane-of-array irradiance, this result is a preliminary screening estimate only. It is not a validated panel-specific generation forecast.

## 12. Reproducibility

The current application is implemented in `app.py`. Install dependencies using:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

The application retrieves data from NASA POWER and therefore requires an internet connection. Generated evaluation outputs are saved in:

- `ecomind_ai_results.md`
- `ecomind_ai_model_metrics.csv`
- `ecomind_ai_test_predictions.csv`

For the exact implementation, parameters, and latest generated results, inspect the current source code and generated result files in this repository.

## 13. Responsible-use statement

EcoMind AI is an educational and research-oriented decision-support prototype. Users should not make safety-critical, financial, or installation decisions from its predictions alone. Actual solar generation depends on the solar resource at the panel plane, system design, equipment condition, shading, temperature, and other site-specific factors.

---

**EcoMind AI — Turning Solar Data into Better Decisions.**  
Created by Ariyan Tausif  
Dhaka, Bangladesh
