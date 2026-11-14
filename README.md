# EcoMind AI
### AI-Powered Solar Intelligence & Decision Support

**Veritas AI International High School Hackathon 2026 — Climate + AI**

EcoMind AI forecasts next-day daily shortwave solar radiation using current-day weather and solar conditions. The formal scientific evaluation is based on Dhaka, Bangladesh. A global city search is included for exploratory use.

## Files
- `EcoMind_AI.ipynb` — Colab notebook for data collection, ML training, chronological testing, persistence baseline, MAE comparison, feature importance, and Gradio dashboard.
- `PROJECT_REPORT.md` — one-page project write-up template.
- `requirements.txt` — Python dependencies.

## Run
1. Open `EcoMind_AI.ipynb` in Google Colab.
2. Run all cells from top to bottom.
3. Wait for the notebook to download historical data, train/evaluate the model, and launch the dashboard.
4. Copy actual metrics and test dates into `PROJECT_REPORT.md`.

## Scientific integrity
- Target: `shortwave_radiation_sum` (daily solar radiation), not electricity generation.
- Training/testing: chronological split; no shuffle.
- Baseline: tomorrow's radiation = today's radiation.
- Global city outputs are exploratory; formal evaluation is Dhaka-only.
- Never claim the model beats persistence unless measured MAE confirms it.

## Data sources
- https://open-meteo.com/en/docs/historical-weather-api
- https://open-meteo.com/en/docs
- https://open-meteo.com/en/docs/geocoding-api

Historical values are reanalysis estimates and can differ from local sensor measurements. Review API terms and attribution requirements before public use.
