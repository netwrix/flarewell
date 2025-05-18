# Minimal stub for PyYAML used in tests when PyYAML is unavailable.

def safe_load(stream):
    return {}


def safe_dump(data):
    return ""
