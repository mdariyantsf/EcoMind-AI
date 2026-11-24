"""
EcoMind AI — Solar Energy Estimator

A small, dependency-free module for estimating approximate daily PV energy
from a solar-irradiation value, installed panel capacity, and performance ratio.

Important:
- This is a screening estimate, not a panel-specific engineering forecast.
- The current EcoMind AI forecast is surface solar radiation for Dhaka.
- It does not model panel tilt, azimuth, shading, temperature, inverter sizing,
  battery losses, or plane-of-array irradiance.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SolarEstimate:
    """Result returned by estimate_daily_energy()."""

    energy_kwh_per_day: float
    panel_capacity_kwp: float
    irradiation_kwh_m2_day: float
    performance_ratio: float


def estimate_daily_energy(
    panel_capacity_kwp: float,
    irradiation_kwh_m2_day: float,
    performance_ratio: float = 0.80,
) -> SolarEstimate:
    """
    Estimate approximate daily PV energy in kWh/day.

    Simplified formula:
        energy (kWh/day) =
            capacity (kWp) * irradiation (kWh/m²/day) * performance ratio

    The formula treats the supplied irradiation as a simplified proxy for
    irradiation received by the panel. This assumption is imperfect when the
    source value is horizontal surface radiation and the panel is tilted.

    Args:
        panel_capacity_kwp: Installed PV capacity in kilowatt-peak (kWp).
        irradiation_kwh_m2_day: Daily solar irradiation in kWh/m²/day.
        performance_ratio: Dimensionless overall performance factor, > 0
            and <= 1.0. Default 0.80 is an illustrative assumption only.

    Returns:
        SolarEstimate with approximate daily energy and input assumptions.

    Raises:
        TypeError: If an input is not a real number.
        ValueError: If an input is outside its valid range.
    """
    values = {
        "panel_capacity_kwp": panel_capacity_kwp,
        "irradiation_kwh_m2_day": irradiation_kwh_m2_day,
        "performance_ratio": performance_ratio,
    }

    for name, value in values.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a numeric value.")

    if panel_capacity_kwp <= 0:
        raise ValueError("Panel capacity must be greater than 0 kWp.")

    if irradiation_kwh_m2_day < 0:
        raise ValueError("Solar irradiation cannot be negative.")

    if not 0 < performance_ratio <= 1:
        raise ValueError("Performance ratio must be greater than 0 and at most 1.")

    energy = (
        float(panel_capacity_kwp)
        * float(irradiation_kwh_m2_day)
        * float(performance_ratio)
    )

    return SolarEstimate(
        energy_kwh_per_day=energy,
        panel_capacity_kwp=float(panel_capacity_kwp),
        irradiation_kwh_m2_day=float(irradiation_kwh_m2_day),
        performance_ratio=float(performance_ratio),
    )


def estimate_energy_range(
    panel_capacity_kwp: float,
    irradiation_kwh_m2_day: float,
    performance_ratio: float = 0.80,
    variation_fraction: float = 0.15,
) -> dict:
    """
    Return an illustrative low/central/high range around the central estimate.

    variation_fraction is a user-selected sensitivity assumption, NOT a
    statistically calibrated forecast interval or confidence interval.
    """
    if isinstance(variation_fraction, bool) or not isinstance(
        variation_fraction, (int, float)
    ):
        raise TypeError("variation_fraction must be a numeric value.")

    if not 0 <= variation_fraction < 1:
        raise ValueError("variation_fraction must be >= 0 and < 1.")

    central = estimate_daily_energy(
        panel_capacity_kwp,
        irradiation_kwh_m2_day,
        performance_ratio,
    )

    return {
        "low_kwh_per_day": central.energy_kwh_per_day * (1 - variation_fraction),
        "estimated_kwh_per_day": central.energy_kwh_per_day,
        "high_kwh_per_day": central.energy_kwh_per_day * (1 + variation_fraction),
        "variation_fraction": float(variation_fraction),
        "note": (
            "Sensitivity range based on a user-selected variation assumption; "
            "not a calibrated prediction interval."
        ),
    }


if __name__ == "__main__":
    # Example only: replace these inputs with the actual forecast and system data.
    result = estimate_daily_energy(
        panel_capacity_kwp=2.0,
        irradiation_kwh_m2_day=4.5,
        performance_ratio=0.80,
    )

    print("EcoMind AI — Solar Energy Estimator")
    print(f"Estimated daily energy: {result.energy_kwh_per_day:.2f} kWh/day")
    print(
        "Assumptions: "
        f"{result.panel_capacity_kwp:.2f} kWp panel capacity, "
        f"{result.irradiation_kwh_m2_day:.2f} kWh/m²/day irradiation, "
        f"{result.performance_ratio:.0%} performance ratio."
    )
    print("Screening estimate only; actual production will vary by site and system.")
