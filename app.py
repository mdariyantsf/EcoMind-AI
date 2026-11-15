
import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px

from datetime import date
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ============================================================
# EcoMind AI
# Dhaka Solar Resource Forecast & Decision Support
# Created by Ariyan Tausif
# ============================================================

st.set_page_config(
    page_title="EcoMind AI | Solar Intelligence",
    page_icon="☀️",
    layout="wide"
)

LATITUDE = 23.8103
LONGITUDE = 90.4125
LOCATION_NAME = "Dhaka, Bangladesh"

START_DATE = "20150101"
END_DATE = "20251231"

TARGET = "solar_radiation"
FEATURES = [
    "solar_today",
    "temperature",
    "cloud_amount",
    "humidity"
]

PARAMETER_MAP = {
    "ALLSKY_SFC_SW_DWN": "solar_radiation",
    "T2M": "temperature",
    "CLOUD_AMT": "cloud_amount",
    "RH2M": "humidity"
}


# ============================================================
# Page styling
# ============================================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(145deg, #071b25, #0b2b35);
        color: #ecfdf5;
    }

    h1, h2, h3 {
        color: #d1fae5 !important;
    }

    .hero {
        padding: 28px;
        border-radius: 18px;
        background: linear-gradient(120deg, #064e3b, #0f766e);
        border: 1px solid #2dd4bf;
        margin-bottom: 20px;
    }

    .hero p {
        color: #d1fae5;
        font-size: 16px;
    }

    .metric-card {
        background: #103b45;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #1e6b70;
    }

    .small-note {
        color: #a7c8c5;
        font-size: 13px;
    }

    div[data-testid="stMetric"] {
        background: #103b45;
        border: 1px solid #1e6b70;
        padding: 14px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# NASA POWER data collection
# ============================================================

@st.cache_data(ttl=86400, show_spinner=False)
def download_nasa_power_data():

    url = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
    )

    parameters = ",".join(PARAMETER_MAP.keys())

    query = {
        "parameters": parameters,
        "community": "RE",
        "longitude": LONGITUDE,
        "latitude": LATITUDE,
        "start": START_DATE,
        "end": END_DATE,
        "format": "JSON",
        "time-standard": "LST"
    }

    response = requests.get(
        url,
        params=query,
        timeout=90
    )

    response.raise_for_status()
    result = response.json()

    parameter_data = (
        result.get("properties", {})
        .get("parameter", {})
    )

    if not parameter_data:
        raise ValueError(
            "NASA POWER returned no parameter data."
        )

    frames = []

    for api_name, column_name in PARAMETER_MAP.items():

        values = parameter_data.get(api_name)

        if not values:
            raise ValueError(
                f"NASA POWER did not return {api_name}. "
                "Check parameter availability."
            )

        series = pd.Series(values, name=column_name)
        series.index = pd.to_datetime(
            series.index,
            format="%Y%m%d",
            errors="coerce"
        )

        frames.append(series)

    data = pd.concat(frames, axis=1)
    data.index.name = "date"
    data = data.reset_index()

    data = data.replace([-999, -999.0], np.nan)

    for column in PARAMETER_MAP.values():
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    data = data.dropna(subset=[TARGET])
    data = data.sort_values("date")
    data = data.drop_duplicates(subset=["date"])

    return data.reset_index(drop=True)


# ============================================================
# Prepare next-day forecasting dataset
# ============================================================

def prepare_dataset(raw_data):

    df = raw_data.copy()

    df = df.sort_values("date").reset_index(drop=True)

    df["solar_today"] = df["solar_radiation"]

    # Tomorrow's observed solar radiation is the target.
    df["target"] = df["solar_radiation"].shift(-1)

    # The input weather values belong to the current day.
    # The target belongs to the following day.
    df["target_date"] = df["date"].shift(-1)

    df = df.dropna(
        subset=["target", "target_date"]
    ).copy()

    df["target_year"] = df["target_date"].dt.year

    df["season"] = np.where(
        df["target_date"].dt.month.isin([6, 7, 8, 9]),
        "Monsoon (June–September)",
        "Other months"
    )

    return df.reset_index(drop=True)


# ============================================================
# Model creation
# ============================================================

def create_linear_model():

    return Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ])


def create_random_forest():

    return Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        (
            "model",
            RandomForestRegressor(
                n_estimators=250,
                max_depth=12,
                min_samples_leaf=3,
                random_state=42,
                n_jobs=-1
            )
        )
    ])


# ============================================================
# Chronological model evaluation
# ============================================================

def evaluate_models(dataset):

    available_years = sorted(
        dataset["target_year"].dropna().unique()
    )

    if len(available_years) < 3:
        raise ValueError(
            "Not enough historical years for a reliable "
            "chronological train/test evaluation."
        )

    test_year = int(available_years[-1])

    train = dataset[
        dataset["target_year"] < test_year
    ].copy()

    test = dataset[
        dataset["target_year"] == test_year
    ].copy()

    if train.empty or test.empty:
        raise ValueError(
            "The chronological train/test split is empty."
        )

    X_train = train[FEATURES]
    y_train = train["target"]

    X_test = test[FEATURES]
    y_test = test["target"]

    # Persistence baseline:
    # Tomorrow's solar radiation = today's solar radiation.
    persistence_predictions = test["solar_today"].to_numpy()

    linear_model = create_linear_model()
    linear_model.fit(X_train, y_train)

    linear_predictions = linear_model.predict(X_test)

    forest_model = create_random_forest()
    forest_model.fit(X_train, y_train)

    forest_predictions = forest_model.predict(X_test)

    predictions = {
        "Persistence baseline": persistence_predictions,
        "Linear Regression": linear_predictions,
        "Random Forest": forest_predictions
    }

    result_rows = []

    for model_name, predicted in predictions.items():

        mae = mean_absolute_error(y_test, predicted)

        rmse = np.sqrt(
            mean_squared_error(y_test, predicted)
        )

        result_rows.append({
            "Model": model_name,
            "MAE": mae,
            "RMSE": rmse
        })

    metrics = pd.DataFrame(result_rows)

    test_results = test[
        ["target_date", "target", "season"]
    ].copy()

    test_results["Persistence baseline"] = (
        persistence_predictions
    )

    test_results["Linear Regression"] = (
        linear_predictions
    )

    test_results["Random Forest"] = (
        forest_predictions
    )

    test_results = test_results.rename(
        columns={"target": "Actual"}
    )

    return {
        "test_year": test_year,
        "train": train,
        "test": test,
        "metrics": metrics,
        "test_results": test_results,
        "linear_model": linear_model,
        "forest_model": forest_model
    }


# ============================================================
# Seasonal analysis
# ============================================================

def seasonal_analysis(test_results):

    rows = []

    for season in test_results["season"].dropna().unique():

        subset = test_results[
            test_results["season"] == season
        ]

        if subset.empty:
            continue

        for model_name in [
            "Persistence baseline",
            "Linear Regression",
            "Random Forest"
        ]:

            mae = mean_absolute_error(
                subset["Actual"],
                subset[model_name]
            )

            rows.append({
                "Season": season,
                "Model": model_name,
                "MAE": mae,
                "Days evaluated": len(subset)
            })

    return pd.DataFrame(rows)


# ============================================================
# Low-solar alert evaluation
# ============================================================

def low_solar_analysis(train, test_results):

    threshold = float(
        train["target"].quantile(0.25)
    )

    actual_low = (
        test_results["Actual"] < threshold
    )

    predicted_low = (
        test_results["Random Forest"] < threshold
    )

    true_positive = int(
        (actual_low & predicted_low).sum()
    )

    false_positive = int(
        (~actual_low & predicted_low).sum()
    )

    false_negative = int(
        (actual_low & ~predicted_low).sum()
    )

    true_negative = int(
        (~actual_low & ~predicted_low).sum()
    )

    precision = (
        true_positive / (true_positive + false_positive)
        if true_positive + false_positive > 0
        else 0.0
    )

    recall = (
        true_positive / (true_positive + false_negative)
        if true_positive + false_negative > 0
        else 0.0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall > 0
        else 0.0
    )

    results = {
        "threshold": threshold,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "true_negative": true_negative
    }

    return results


# ============================================================
# Next-day prediction from user inputs
# ============================================================

def predict_next_day(
    model,
    solar_today,
    temperature,
    cloud_amount,
    humidity
):

    input_data = pd.DataFrame([{
        "solar_today": solar_today,
        "temperature": temperature,
        "cloud_amount": cloud_amount,
        "humidity": humidity
    }])

    prediction = float(
        model.predict(input_data)[0]
    )

    # Solar radiation cannot be physically negative.
    prediction = max(0.0, prediction)

    return prediction


# ============================================================
# Main interface
# ============================================================

st.markdown("""
<div class="hero">
    <h1>☀️ EcoMind AI</h1>
    <h3>Solar Intelligence & Climate Decision Support</h3>
    <p>
        An AI-powered solar resource forecasting system
        designed for household solar-battery planning
        in Dhaka, Bangladesh.
    </p>
    <p><b>Research location:</b> Dhaka, Bangladesh</p>
    <p><b>Created by:</b> Ariyan Tausif</p>
</div>
""", unsafe_allow_html=True)


st.info(
    "EcoMind AI forecasts daily solar radiation. "
    "Solar radiation is not the same as electricity generated "
    "by a solar panel."
)


with st.sidebar:

    st.header("EcoMind AI")

    st.write("Dhaka Solar Intelligence")

    st.markdown("---")

    st.write("**Data source**")
    st.write("NASA POWER Daily API")

    st.write("**Forecast target**")
    st.write("Next-day solar radiation")

    st.write("**Models**")
    st.write("- Persistence baseline")
    st.write("- Linear Regression")
    st.write("- Random Forest")

    st.markdown("---")

    if st.button("Refresh NASA POWER data"):
        download_nasa_power_data.clear()
        st.rerun()


# ============================================================
# Load and process data
# ============================================================

try:

    with st.spinner(
        "Downloading historical solar and weather data..."
    ):

        raw_data = download_nasa_power_data()

    dataset = prepare_dataset(raw_data)

    evaluation = evaluate_models(dataset)

    metrics = evaluation["metrics"]
    test_results = evaluation["test_results"]
    train = evaluation["train"]

    seasonal_results = seasonal_analysis(
        test_results
    )

    alert_results = low_solar_analysis(
        train,
        test_results
    )

except Exception as error:

    st.error(
        "EcoMind AI could not load or process the NASA POWER "
        "dataset."
    )

    st.exception(error)

    st.markdown("""
    **Possible reasons**
    - NASA POWER may be temporarily unavailable.
    - A requested parameter may not be available for this period.
    - The internet connection may have failed.
    - The dataset may not contain enough complete records.

    Please try again later. Do not interpret missing data as zero.
    """)

    st.stop()


# ============================================================
# Dashboard overview
# ============================================================

st.subheader("📊 Solar Intelligence Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Historical records",
        f"{len(raw_data):,}"
    )

with col2:
    st.metric(
        "Training records",
        f"{len(train):,}"
    )

with col3:
    st.metric(
        "Test year",
        str(evaluation["test_year"])
    )

with col4:
    st.metric(
        "Test records",
        f"{len(test_results):,}"
    )


st.caption(
    f"Dataset dates: {raw_data['date'].min().date()} "
    f"to {raw_data['date'].max().date()}. "
    "The latest target year is held out for testing."
)


# ============================================================
# Historical data chart
# ============================================================

st.markdown("---")
st.subheader("🌍 Historical Solar Radiation")

historical_chart = px.line(
    raw_data,
    x="date",
    y="solar_radiation",
    title="Daily Solar Radiation — Dhaka",
    labels={
        "date": "Date",
        "solar_radiation": "Solar radiation (kWh/m²/day)"
    }
)

historical_chart.update_layout(
    template="plotly_dark",
    height=400
)

st.plotly_chart(
    historical_chart,
    use_container_width=True
)


# ============================================================
# Model comparison
# ============================================================

st.markdown("---")
st.subheader("🤖 AI Model Evaluation")

st.write(
    "All models are evaluated on the same latest-year "
    "chronological test period."
)

st.dataframe(
    metrics.style.format({
        "MAE": "{:.4f}",
        "RMSE": "{:.4f}"
    }),
    use_container_width=True
)

metric_chart = px.bar(
    metrics,
    x="Model",
    y="MAE",
    color="Model",
    title="Mean Absolute Error — Lower is Better",
    labels={
        "MAE": "MAE (kWh/m²/day)"
    }
)

metric_chart.update_layout(
    template="plotly_dark",
    showlegend=False
)

st.plotly_chart(
    metric_chart,
    use_container_width=True
)


# ============================================================
# Explain model comparison
# ============================================================

baseline_mae = float(
    metrics.loc[
        metrics["Model"] == "Persistence baseline",
        "MAE"
    ].iloc[0]
)

linear_mae = float(
    metrics.loc[
        metrics["Model"] == "Linear Regression",
        "MAE"
    ].iloc[0]
)

forest_mae = float(
    metrics.loc[
        metrics["Model"] == "Random Forest",
        "MAE"
    ].iloc[0]
)

st.markdown("### What do the results mean?")

if forest_mae < baseline_mae:

    improvement = (
        (baseline_mae - forest_mae) / baseline_mae
    ) * 100

    st.success(
        f"Random Forest achieved a {improvement:.2f}% "
        "lower MAE than the persistence baseline on the "
        "held-out test period."
    )

else:

    st.warning(
        "Random Forest did not outperform the persistence "
        "baseline on the held-out test period. This is an "
        "important result, not something to hide."
    )

if linear_mae < baseline_mae:

    st.write(
        "Linear Regression also improved on the persistence "
        "baseline in this test."
    )

else:

    st.write(
        "Linear Regression did not improve on the persistence "
        "baseline in this test."
    )


# ============================================================
# Seasonal intelligence
# ============================================================

st.markdown("---")
st.subheader("🌧️ Seasonal Intelligence")

st.write(
    "This analysis checks whether forecast errors differ "
    "between the monsoon season and the other months."
)

st.dataframe(
    seasonal_results.style.format({
        "MAE": "{:.4f}"
    }),
    use_container_width=True
)

if not seasonal_results.empty:

    seasonal_chart = px.bar(
        seasonal_results,
        x="Season",
        y="MAE",
        color="Model",
        barmode="group",
        title="Forecast Error by Season"
    )

    seasonal_chart.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        seasonal_chart,
        use_container_width=True
    )


# ============================================================
# Low-solar alert intelligence
# ============================================================

st.markdown("---")
st.subheader("⚠️ Low Solar Alert Evaluation")

st.write(
    "The alert threshold is the 25th percentile of the "
    "training-period next-day solar radiation. It is calculated "
    "without using test-period target values."
)

st.metric(
    "Training-period low-solar threshold",
    f"{alert_results['threshold']:.3f} kWh/m²/day"
)

alert_col1, alert_col2, alert_col3 = st.columns(3)

with alert_col1:
    st.metric(
        "Precision",
        f"{alert_results['precision']:.3f}"
    )

with alert_col2:
    st.metric(
        "Recall",
        f"{alert_results['recall']:.3f}"
    )

with alert_col3:
    st.metric(
        "F1 score",
        f"{alert_results['f1']:.3f}"
    )

st.write("**Alert classification counts**")

st.write({
    "Correct low-solar alerts": alert_results["true_positive"],
    "False alerts": alert_results["false_positive"],
    "Missed low-solar days": alert_results["false_negative"],
    "Correct normal-day predictions": alert_results["true_negative"]
})


# ============================================================
# Failure investigation
# ============================================================

st.markdown("---")
st.subheader("🔍 Failure Investigation")

failure_data = test_results.copy()

failure_data["Random Forest absolute error"] = (
    failure_data["Actual"]
    - failure_data["Random Forest"]
).abs()

failure_data = failure_data.sort_values(
    "Random Forest absolute error",
    ascending=False
)

worst_cases = failure_data.head(5)

st.write(
    "The following are the five largest Random Forest "
    "prediction errors in the held-out test period."
)

st.dataframe(
    worst_cases[
        [
            "target_date",
            "Actual",
            "Random Forest",
            "Persistence baseline",
            "Random Forest absolute error"
        ]
    ].style.format({
        "Actual": "{:.3f}",
        "Random Forest": "{:.3f}",
        "Persistence baseline": "{:.3f}",
        "Random Forest absolute error": "{:.3f}"
    }),
    use_container_width=True
)

st.caption(
    "Possible explanations for large errors may include "
    "rapid weather changes, unusual cloud conditions, "
    "missing observations or limitations in the input features. "
    "These are hypotheses, not confirmed causes."
)


# ============================================================
# Interactive next-day forecast
# ============================================================

st.markdown("---")
st.subheader("🔮 Next-Day Solar Resource Forecast")

st.write(
    "Enter today's weather and solar radiation values to "
    "estimate tomorrow's solar radiation using the trained "
    "Random Forest model."
)

st.caption(
    "Use values in the same units and definitions as the "
    "NASA POWER dataset. The forecast is an estimate, "
    "not a guarantee."
)

input_col1, input_col2 = st.columns(2)

with input_col1:

    solar_today = st.number_input(
        "Today's solar radiation (kWh/m²/day)",
        min_value=0.0,
        max_value=12.0,
        value=4.0,
        step=0.1
    )

    temperature = st.number_input(
        "Today's average temperature (°C)",
        min_value=-20.0,
        max_value=60.0,
        value=28.0,
        step=0.5
    )

with input_col2:

    cloud_amount = st.number_input(
        "Today's cloud amount (%)",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=1.0
    )

    humidity = st.number_input(
        "Today's relative humidity (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0,
        step=1.0
    )


if st.button(
    "Predict Tomorrow's Solar Resource",
    type="primary",
    use_container_width=True
):

    prediction = predict_next_day(
        evaluation["forest_model"],
        solar_today,
        temperature,
        cloud_amount,
        humidity
    )

    st.markdown("### Forecast result")

    st.metric(
        "Predicted next-day solar radiation",
        f"{prediction:.3f} kWh/m²/day"
    )

    if prediction < alert_results["threshold"]:

        st.warning(
            "Low Solar Resource Alert: the predicted value "
            "is below the training-period low-solar threshold. "
            "A household solar-battery manager may review "
            "battery-use plans."
        )

    else:

        st.success(
            "The predicted solar resource is not below the "
            "training-period low-solar threshold."
        )

    st.caption(
        "This is a model-based decision-support signal. "
        "It does not calculate actual electricity generation "
        "or guarantee household battery availability."
    )


# ============================================================
# Downloadable results
# ============================================================

st.markdown("---")
st.subheader("📥 Research Data & Results")

csv_data = test_results.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download held-out test predictions (CSV)",
    data=csv_data,
    file_name="ecomind_ai_test_predictions.csv",
    mime="text/csv"
)

metrics_csv = metrics.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download model evaluation metrics (CSV)",
    data=metrics_csv,
    file_name="ecomind_ai_model_metrics.csv",
    mime="text/csv"
)


# ============================================================
# Methodology and limitations
# ============================================================

st.markdown("---")
st.subheader("📚 Methodology")

st.markdown("""
**Location:** Dhaka, Bangladesh

**Dataset:** NASA POWER Daily API

**Forecast task:** Estimate the next day's daily
all-sky surface shortwave solar radiation.

**Input features:**
- Today's solar radiation
- Today's average temperature
- Today's cloud amount
- Today's relative humidity

**Target:** The following day's solar radiation.

**Models compared:**
1. Persistence baseline — tomorrow equals today.
2. Linear Regression.
3. Random Forest.

**Evaluation:** Earlier target dates are used for training.
The latest available target year is held out for testing.
The days are never randomly shuffled.

**Project-specific addition:** Seasonal error analysis,
low-solar alert evaluation and a household decision-support
interface for Dhaka.
""")

st.subheader("⚖️ Important limitations")

st.markdown("""
- NASA POWER data are gridded/reanalysis or satellite-based
  data products, not measurements from a household solar panel.
- The model predicts solar radiation, not electricity output.
- Actual electricity generation depends on panel capacity,
  tilt, orientation, efficiency, shading and system losses.
- The manual forecast depends on the quality of the entered
  weather values.
- The model may perform poorly during unusual weather.
- Historical performance does not guarantee future accuracy.
- The test results must be reported honestly, even if the
  AI models do not beat the persistence baseline.
""")

st.markdown("---")

st.caption(
    "EcoMind AI | AI + Climate | Dhaka, Bangladesh | "
    "Created by Ariyan Tausif"
)
