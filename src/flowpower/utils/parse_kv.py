def parse_kv_pairs(pairs: list[str]) -> dict:
    """
    Converts ['a=1', 'b=2'] → {'a': '1', 'b': '2'}
    """
    result = {}
    if not pairs:
        return result
    for item in pairs:
        if "=" not in item:
            raise ValueError(f"Expected key=value format, got: {item}")
        key, value = item.split("=", 1)
        result[key.strip()] = value.strip()
    return result
