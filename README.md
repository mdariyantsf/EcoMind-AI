☀️ EcoMind AI

AI-Powered Solar Intelligence & Climate Decision Support

Track: AI + Climate
Location: Dhaka, Bangladesh
Project Creator: Ariyan Tausif

---

1. The Problem

Households that depend on solar energy need to make practical decisions about energy use when solar resources vary from day to day.

In Dhaka, Bangladesh, changing weather conditions, cloud cover, humidity, and seasonal patterns can influence the amount of solar radiation reaching the Earth's surface.

However, household solar-battery managers may not have an accessible way to examine the next day's expected solar resource before planning battery use.

EcoMind AI explores how machine learning can support this decision through next-day solar radiation forecasting.

2. What We Built

EcoMind AI is a solar resource forecasting and decision-support application focused on Dhaka, Bangladesh.

It uses historical daily weather and solar radiation data from NASA POWER to train and evaluate machine learning models.

The application provides:

- Historical solar radiation visualization.
- Next-day solar radiation forecasting.
- Comparison between machine learning models and a persistence baseline.
- Seasonal forecast-error analysis.
- Low-solar resource alerts.
- Evaluation of alert precision, recall, and F1 score.
- Investigation of the largest prediction errors.
- Interactive forecasting with user-provided weather inputs.
- Downloadable model evaluation results.

The intended user is a household solar-battery manager who wants an additional information source when planning household battery use.

3. Research Objectives

EcoMind AI investigates three main research questions:

1. Can machine learning improve next-day solar radiation forecasts compared with the persistence baseline in Dhaka?
2. Does forecasting performance differ between the monsoon season and other months?
3. Can a low-solar alert help identify days when household energy planning may need extra attention?

The project also evaluates low-solar alerts using a threshold calculated exclusively from training data.

4. How It Works

Data Source

NASA POWER Daily API:

https://power.larc.nasa.gov/

Location:

- Latitude: 23.8103
- Longitude: 90.4125
- City: Dhaka
- Country: Bangladesh

The application requests the following daily parameters:

Parameter| Meaning
ALLSKY_SFC_SW_DWN| All-sky surface shortwave downward solar radiation
T2M| Temperature at 2 metres
CLOUD_AMT| Cloud amount
RH2M| Relative humidity

The target variable is daily solar radiation, measured in kWh/m²/day.

Forecasting Method

The model uses today's available values to estimate tomorrow's solar radiation.

Input features:

- Today's solar radiation
- Today's temperature
- Today's cloud amount
- Today's relative humidity

Target:

- Following day's solar radiation

Models

EcoMind AI compares three forecasting approaches.

1. Persistence Baseline

The baseline assumes that tomorrow's solar radiation will be the same as today's.

2. Linear Regression

A machine learning reference model that learns a linear relationship between today's input features and tomorrow's solar radiation.

3. Random Forest

An ensemble machine learning model that learns more complex relationships between the input features and the forecasting target.

No model is assumed to be better before evaluation.

5. Evaluation Strategy

The project uses chronological evaluation.

- Earlier dates are used for training.
- The most recent available target year is reserved for testing.
- Dates are not randomly shuffled.
- All models are evaluated on the same held-out test period.

The main evaluation metric is Mean Absolute Error (MAE).

Root Mean Squared Error (RMSE) is also reported.

Lower error indicates more accurate predictions.

The project reports the actual results produced by the application. It does not assume that a more complex model must outperform the baseline.

Evaluation results are saved in:

- "ecomind_ai_results.md"
- "ecomind_ai_model_metrics.csv"
- "ecomind_ai_test_predictions.csv"

6. Seasonal Intelligence

Dhaka's climate has distinct seasonal conditions.

EcoMind AI compares forecasting errors across:

- Monsoon season: June to September.
- Other months: January to May and October to December.

This analysis helps investigate whether next-day solar radiation is more difficult to forecast during particular parts of the year.

7. Low Solar Resource Alerts

EcoMind AI calculates a low-solar threshold using the 25th percentile of the training-period target values.

A forecast below this threshold produces a low-solar resource alert.

The application evaluates these alerts using:

- Precision
- Recall
- F1 score
- Correct alerts
- False alerts
- Missed low-solar days

The threshold is calculated from training data rather than the held-out test targets.

8. Failure Investigation

A forecasting system should also identify where it performs poorly.

EcoMind AI identifies the five largest Random Forest prediction errors in the test period.

These cases allow investigation of possible reasons for forecasting failures, including:

- Rapid weather changes.
- Unusual cloud conditions.
- Missing observations.
- Limitations of the selected input features.

These explanations are treated as hypotheses unless independently verified.

9. Decision Support

The intended decision is whether a household solar-battery manager in Dhaka should review the household's battery-use plan because of an expected low-solar day.

EcoMind AI provides an additional forecast signal to support that decision.

It does not automatically control batteries or guarantee electricity availability.

10. Important Scientific Limitations

Solar radiation and solar electricity generation are not the same thing.

EcoMind AI forecasts solar radiation reaching the Earth's surface. It does not directly predict the electricity generated by a particular solar panel.

Actual electricity generation also depends on:

- Solar panel capacity.
- Panel tilt and orientation.
- Shading.
- Panel efficiency.
- System losses.
- Installation conditions.

NASA POWER data are gridded environmental data products. They are not direct measurements from an individual household's solar panel.

Forecasts are estimates and may be inaccurate, especially during unusual weather conditions.

11. Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Requests
- NASA POWER Daily API

12. How to Run

Install the required libraries:

pip install -r requirements.txt

Start the application:

streamlit run app.py

The application retrieves historical data from NASA POWER when it runs, so an internet connection is required.

13. Sources and Credits

Dataset

NASA POWER:
https://power.larc.nasa.gov/

NASA POWER API Documentation:
https://power.larc.nasa.gov/docs/

Machine Learning

Scikit-learn:
https://scikit-learn.org/

Data Processing

Pandas:
https://pandas.pydata.org/

NumPy:
https://numpy.org/

Visualization

Plotly:
https://plotly.com/python/

Application Framework

Streamlit:
https://streamlit.io/

14. Future Improvements

With further development, EcoMind AI could be improved by:

1. Testing additional forecasting features.
2. Comparing multiple forecast horizons.
3. Evaluating the model on more recent independently available observations.
4. Incorporating local solar-panel system specifications to estimate potential electricity generation.
5. Testing the decision-support system with real household energy-use scenarios.

---

EcoMind AI — Turning Solar Data into Better Decisions.

Created by Ariyan Tausif
Dhaka, Bangladesh
