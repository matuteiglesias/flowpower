def pretty_print_trace(run):
    print(f"🧪 Run ID: {getattr(run, 'name', 'unknown')}")
    print(f"✅ Status: {getattr(run, 'status', 'unknown')}")
    print(f"🧵 Calls: {len(getattr(run, 'api_calls', []))}")
    print()

    for i, call in enumerate(run.api_calls or []):
        name = getattr(call, "name", f"step_{i}")
        output = getattr(call, "output", "")
        print(f"→ {name}: {str(output)[:80]}")
