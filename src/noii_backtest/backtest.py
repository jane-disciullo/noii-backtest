
import pandas as pd


def calculate_return(entry_price, exit_price, signal):
    """Calculate the return for one trade."""

    if signal not in (-1, 0, 1):
        raise ValueError("Signal must be -1, 0, or 1.")

    if entry_price <= 0:
        raise ValueError("Entry price must be greater than zero.")

    if exit_price <= 0:
        raise ValueError("Exit price must be greater than zero.")

    return (
        (exit_price - entry_price)
        / entry_price
    ) * signal


def run_backtest(trades: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Calculate returns and summary statistics
    for a collection of trades.
    """

    required_columns = {
        "entry_price",
        "exit_price",
        "signal",
    }

    missing = required_columns - set(trades.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    results = trades.copy()

    results["return"] = results.apply(
        lambda row: calculate_return(
            row["entry_price"],
            row["exit_price"],
            row["signal"]
        ),
        axis=1
    )

    results["equity"] = (
        1 + results["return"]
    ).cumprod()

    num_trades = len(results)

    winning_trades = (
        results["return"] > 0
    ).sum()

    losing_trades = (
        results["return"] < 0
    ).sum()

    summary = {
        "num_trades": num_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": (
            winning_trades / num_trades
            if num_trades > 0
            else 0
        ),
        "average_return": (
            results["return"].mean()
            if num_trades > 0
            else 0
        ),
        "total_return": (
            results["equity"].iloc[-1] - 1
            if num_trades > 0
            else 0
        ),
    }

    return results, summary
