
# EcoMind AI
## Dhaka Solar Resource Forecast & Household Decision Support

**Track:** AI + Climate  
**Project Location:** Dhaka, Bangladesh  
**Team:** Ariyan Tausif (Solo Participant)

### 1. Problem

Households and small solar-energy users need to understand how much solar energy may be available on the following day. Cloud cover, humidity, and temperature can affect solar radiation. Without a useful forecast, users may find it difficult to plan energy use and battery charging.

EcoMind AI explores whether machine learning can improve next-day solar-resource forecasts for Dhaka compared with a simple persistence baseline.

### 2. What We Built

EcoMind AI is a data-driven solar-resource forecasting and decision-support application. It uses historical NASA POWER daily data for Dhaka to predict the next day's daily all-sky surface shortwave solar radiation.

The application includes:
- Historical solar-resource visualization.
- A persistence baseline.
- Linear Regression and Random Forest models.
- Chronological training and testing.
- Seasonal performance analysis.
- Low-solar-resource alerts.
- Example forecast failures and model evaluation.
- A manual forecast interface for entering weather observations.

### 3. Data and Method

**Primary data source:** NASA POWER Daily API  
https://power.larc.nasa.gov/

**Location:** Dhaka, Bangladesh  
**Coordinates:** 23.8103° N, 90.4125° E

The application requests daily solar radiation and weather-related variables, including:
- `ALLSKY_SFC_SW_DWN`
- `T2M`
- `CLOUD_AMT`
- `RH2M`

The target is next-day daily all-sky surface shortwave solar radiation, measured in kWh/m²/day.

The models use today's available observations to estimate the next day's solar radiation. Data is divided chronologically: earlier observations are used for training and the latest complete target year is reserved for testing. The data is not randomly shuffled.

### 4. Models and Baseline

EcoMind AI compares three approaches:

1. **Persistence baseline:** predicts that the next day's solar radiation will be the same as today's.
2. **Linear Regression:** learns relationships between weather-related input variables and next-day solar radiation.
3. **Random Forest:** captures potentially non-linear relationships in the data.

Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) are used to evaluate forecast performance on the held-out test period.

### 5. Results

**Complete this section after running the application and recording the actual test results. Do not estimate or invent metrics.**

| Model | Test MAE (kWh/m²/day) | Test RMSE |
|---|---:|---:|
| Persistence | [Insert actual result] | [Insert actual result] |
| Linear Regression | [Insert actual result] | [Insert actual result] |
| Random Forest | [Insert actual result] | [Insert actual result] |

**Best-performing model:** [Insert after evaluation]

**Seasonal findings:** [Insert actual monsoon and non-monsoon results]

### 6. Real-World Decision Support

The intended user is a household solar-battery manager in Dhaka.

A next-day solar-resource forecast can help the user anticipate relatively low or high solar availability and plan energy use accordingly. The low-solar alert is based on a threshold calculated from the training-period data.

The application forecasts solar radiation, not actual electricity generation or guaranteed battery performance.

### 7. Limitations and Failure Analysis

Forecasts may be less reliable during unusual weather conditions or when the input data does not represent rapidly changing local conditions. NASA POWER data is not a direct measurement from an individual household's solar panels.

The application includes examples of forecast errors so that weak predictions can be examined rather than hidden. Model performance must be interpreted using the held-out test results.

### 8. Next Steps

Future improvements could include:
- Testing additional forecasting models.
- Evaluating more recent observations.
- Adding more local weather information.
- Improving the usefulness of household decision recommendations.

### 9. Sources

- NASA POWER Data Access Viewer: https://power.larc.nasa.gov/
- NASA POWER Documentation: https://power.larc.nasa.gov/docs/
- Scikit-learn Documentation: https://scikit-learn.org/stable/

### 10. Code and Application

**GitHub Repository:** https://github.com/mdariyantsf/EcoMind-AI

**Application:** Run the project using the instructions in `README.md`.

---

**Created by Ariyan Tausif**  
Bangladesh | Veritas AI International High School Hackathon 2026
