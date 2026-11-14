# EcoMind AI — Project Write-up

**Track:** Climate + AI  
**Project:** EcoMind AI — AI-Powered Solar Intelligence & Decision Support  
**Primary evaluation location:** Dhaka, Bangladesh

## Problem
Solar operators and battery managers need advance information about expected solar conditions to plan operations. Daily solar radiation varies with cloud cover, rainfall, temperature, and seasonal conditions.

## Approach
EcoMind AI uses historical daily weather and solar-radiation data from the Open-Meteo Historical Weather API. A Random Forest regression model learns to predict the next day's daily shortwave solar radiation from the current day's weather and radiation conditions. A global city search provides exploratory forecasts, while formal scientific evaluation remains focused on Dhaka.

## Evaluation
The data is ordered by date. The earliest 80% of examples are used for training and the latest 20% for testing; dates are not shuffled. The model is compared against a persistence baseline that predicts tomorrow's radiation as equal to today's radiation. Mean Absolute Error (MAE) is the primary metric.

**Replace these placeholders with actual notebook results:**
- Training period: [actual dates]
- Held-out test period: [actual dates]
- EcoMind AI MAE: [measured value] MJ/m²/day
- Persistence MAE: [measured value] MJ/m²/day
- Result: [state honestly whether the model improved on persistence]

## Decision supported
The forecast can help a solar-site operator or battery manager anticipate comparatively lower or higher solar conditions and review operational or charging plans. It is decision support, not an automated control system.

## Limitations
The target is solar radiation, not electricity generation. Historical values are reanalysis estimates rather than measurements from a specific solar panel. Formal evaluation is Dhaka-only; forecasts for other cities are exploratory and may not generalise.

## Tools and sources
Python, pandas, NumPy, scikit-learn, Open-Meteo APIs, Plotly, and Gradio. AI assistance used: [describe tools and use in accordance with event rules].
