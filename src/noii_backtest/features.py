
import pandas as pd


def add_imbalance_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate imbalance shares relative to paired + imbalance shares."""
    df = df.copy()

    denominator = (
        df["paired_shares"] +
        df["imbalance_shares"]
    )

    if (denominator <= 0).any():
        raise ValueError("paired_shares + imbalance_shares must be greater than zero.")

    df["imbalance_ratio"] = (
        df["imbalance_shares"] / denominator
    )

    return df


def add_signed_imbalance(df: pd.DataFrame) -> pd.DataFrame:
    """Convert buy/sell imbalance into a signed numerical signal."""
    df = df.copy()

    direction_map = {
        "B": 1,
        "S": -1,
        "N": 0,
        "O": 0,
    }

    df["direction_sign"] = (
        df["imbalance_direction"]
        .map(direction_map)
        .fillna(0)
    )

    df["signed_imbalance"] = (
        df["imbalance_ratio"] *
        df["direction_sign"]
    )

    return df


def add_price_deviation(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate near-price deviation from reference price."""
    df = df.copy()

    if (df["reference_price"] <= 0).any():
        raise ValueError("reference_price must be greater than zero.")

    df["near_reference_deviation"] = (
        (df["near_price"] - df["reference_price"])
        / df["reference_price"]
    )

    return df
