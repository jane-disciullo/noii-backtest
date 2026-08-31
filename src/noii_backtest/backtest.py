
def calculate_return(entry_price, exit_price, signal):
    """
    Calculate trade return.

    signal:
        1  = long
        0  = no trade
       -1  = short
    """

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


def backtest_trade(entry_price, exit_price, signal):
    """Return a simple trade result dictionary."""

    trade_return = calculate_return(
        entry_price,
        exit_price,
        signal
    )

    return {
        "entry_price": entry_price,
        "exit_price": exit_price,
        "signal": signal,
        "return": trade_return,
    }
