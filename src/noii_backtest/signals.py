
import pandas as pd


def generate_signal(
    df: pd.DataFrame,
    imbalance_threshold: float = 0.20,
) -> pd.DataFrame:
    """
    Generate NOII + price signals.

    Long:
        signed imbalance >= threshold
        AND near price > reference price

    Short:
        signed imbalance <= -threshold
        AND near price < reference price

    Otherwise:
        0 = no trade
    """

    df = df.copy()

    df["signal"] = 0

    long_condition = (
        (df["signed_imbalance"] >= imbalance_threshold)
        & (df["near_price"] > df["reference_price"])
    )

    short_condition = (
        (df["signed_imbalance"] <= -imbalance_threshold)
        & (df["near_price"] < df["reference_price"])
    )

    df.loc[long_condition, "signal"] = 1
    df.loc[short_condition, "signal"] = -1

    return df
