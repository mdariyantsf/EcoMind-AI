☀️ EcoMind AI
AI-Powered Solar Intelligence & Climate Decision Support
Research location: Dhaka, Bangladesh
Project creator: Ariyan Tausif
1. The Problem
Households that depend on solar energy need to make practical decisions when solar resources may vary from day to day.
In Dhaka, changing weather conditions, cloud cover, humidity, and seasonal patterns can influence the amount of solar radiation reaching the Earth's surface. EcoMind AI explores how machine learning can support household solar-battery planning through next-day solar-radiation forecasting.
2. What EcoMind AI Does
EcoMind AI is an AI-powered solar-resource forecasting and decision-support application focused on Dhaka.
It uses historical daily weather and solar-radiation data from NASA POWER to train and evaluate machine-learning models.
The application currently provides:
Historical solar-radiation visualization.
Next-day solar-radiation forecasting.
Comparison between AI models and a persistence baseline.
Seasonal forecast-error analysis.
Low-solar resource alerts.
Evaluation of alert precision, recall, and F1 score.
Investigation of the largest prediction errors.
Interactive forecasting with user-provided weather inputs.
Downloadable model-evaluation results.
The intended user is a household solar-battery manager who wants an additional information source when reviewing a household battery-use plan.
3. Research Questions
Can machine learning improve next-day solar-radiation forecasts compared with a persistence baseline in Dhaka?
Does forecasting performance differ between the monsoon season and other months?
Can a low-solar alert help identify days when household energy planning may need extra attention?
4. Data Source and Location
Source: NASA POWER Daily API
Documentation: NASA POWER API documentation
Current research location:
Latitude: 23.8103
Longitude: 90.4125
City: Dhaka
Country: Bangladesh
The application requests these daily parameters:
NASA POWER parameter
Meaning
ALLSKY_SFC_SW_DWN
All-sky surface shortwave downward solar radiation
T2M
Temperature at 2 metres
CLOUD_AMT
Cloud amount
RH2M
Relative humidity at 2 metres
The target variable is daily solar radiation, measured in kWh/m²/day.
5. How Forecasting Works
The current model uses today's available values to estimate tomorrow's solar radiation.
Input features:
Today's solar radiation
Today's temperature
Today's cloud amount
Today's relative humidity
Target: Following day's solar radiation.
EcoMind AI compares three approaches:
Persistence baseline: assumes tomorrow's solar radiation will equal today's.
Linear Regression: learns a linear relationship between today's inputs and tomorrow's solar radiation.
Random Forest: learns more complex relationships from the input features.
No model is assumed to be better before evaluation.
6. Evaluation Strategy
The project uses chronological evaluation:
Earlier dates are used for training.
The most recent available target year is reserved for testing.
Dates are not randomly shuffled.
All models are evaluated on the same held-out test period.
The main metrics are Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE). Lower values indicate smaller prediction errors.
The currently committed generated report covers 2015–2025, with 2025 as the held-out test year. Consult ecomind_ai_results.md and ecomind_ai_model_metrics.csv for the recorded results. Results may change when the application is rerun with updated data or code.
7. Seasonal Intelligence
The application compares forecast errors across:
Monsoon season: June to September.
Other months: January to May and October to December.
This analysis helps investigate whether next-day solar-radiation forecasting is more difficult during particular parts of the year.
8. Low-Solar Resource Alerts
EcoMind AI calculates a low-solar threshold using the 25th percentile of the training-period target values.
A forecast below this threshold produces a low-solar resource alert.
The application evaluates alerts using:
Precision
Recall
F1 score
Correct alerts
False alerts
Missed low-solar days
The threshold is calculated from training data rather than held-out test targets.
9. Solar Energy Estimator Module
The repository includes solar_calculator.py, a standalone Python module for a simplified estimate of daily solar-panel energy.
It uses:
estimated_energy_kwh = panel_capacity_kwp × irradiation_kwh_m2_day × performance_ratio
Example:
from solar_calculator import estimate_daily_energy

estimate = estimate_daily_energy(
    panel_capacity_kwp=2.0,
    irradiation_kwh_m2_day=4.5,
    performance_ratio=0.80,
)

print(estimate.energy_kwh_per_day)
The example values are illustrative, not a claim about a real installation.
Important: The module is currently a standalone calculation utility. It is not yet connected to the Streamlit interface in app.py. The current forecast is surface solar radiation; it does not model panel tilt, orientation, shading, or plane-of-array irradiance. Therefore, its output is a preliminary screening estimate, not a validated panel-specific generation forecast.
10. Scientific Limitations
Solar radiation and solar electricity generation are not the same thing.
EcoMind AI forecasts solar radiation reaching the Earth's surface. It does not directly predict the electricity generated by a particular solar panel.
Actual electricity generation also depends on:
Solar panel capacity.
Panel tilt and orientation.
Shading.
Panel efficiency and temperature.
Inverter and wiring losses.
Installation and maintenance conditions.
Solar irradiation received at the panel plane.
NASA POWER data are gridded environmental data products, not direct measurements from an individual household's solar panel. Forecasts are estimates and may be inaccurate, especially during unusual weather conditions.
EcoMind AI does not automatically control batteries or guarantee electricity availability.
11. Repository Files
File
Purpose
app.py
Main Streamlit application, NASA POWER data pipeline, model training/evaluation, forecasting, charts, and alerts
solar_calculator.py
Standalone solar-energy estimation utility
MODEL_CARD.md
Model purpose, data, methods, evaluation, intended use, and limitations
ecomind_ai_results.md
Results report generated by the application
ecomind_ai_model_metrics.csv
MAE and RMSE comparison for evaluated methods
ecomind_ai_test_predictions.csv
Held-out test predictions
requirements.txt
Python dependencies
README.md
Project overview and setup instructions
12. How to Run
Install the required libraries:
pip install -r requirements.txt
Start the application:
streamlit run app.py
The application retrieves historical data from NASA POWER when it runs, so an internet connection is required.
To run the standalone calculator example:
python solar_calculator.py
13. Technology Stack
Python
Streamlit
Pandas
NumPy
Scikit-learn
Plotly
Requests
NASA POWER Daily API
Useful references:
NASA POWER
Scikit-learn
Pandas
NumPy
Plotly
Streamlit
14. Future Improvements
Integrate the Solar Energy Estimator into the Streamlit interface.
Add panel orientation and plane-of-array irradiation modelling.
Test additional forecasting features and forecast horizons.
Evaluate the model with rolling-origin and multi-year backtesting.
Add calibrated prediction intervals.
Validate the system with independently measured local solar-panel output.
Extend to additional locations only after location-specific data preparation, training, and evaluation.
EcoMind AI — Turning Solar Data into Better Decisions.
Created by Ariyan Tausif
Dhaka, Bangladesh
