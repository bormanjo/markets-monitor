from . import reference, stocks


def get_symbols():
    """
    Retrieves a table of valid cryptocurrency symbols.
    Returns a DataFrame.
    """
    
    symbols = reference.get_symbols()
    fltr = symbols["type"] == "crypto"
    
    return symbols.loc[fltr, :]