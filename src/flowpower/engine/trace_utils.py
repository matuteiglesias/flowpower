def pretty_print_trace(run):
    print(f"🧪 Run ID: {getattr(run, 'name', 'unknown')}")
    print(f"✅ Status: {getattr(run, 'status', 'unknown')}")
    
    calls = getattr(run, "api_calls", None)
    
    if calls is None:
        print(f"⚠️  No API calls found. This may be a failed run or a run without trace data.")
        if hasattr(run, "output"):
            print("\n🖨️ Output (summary):")
            print(str(run.output)[:200])
        return

    print(f"🧵 Calls: {len(calls)}\n")
    for i, call in enumerate(calls):
        name = getattr(call, "name", f"step_{i}")
        output = getattr(call, "output", "")
        print(f"→ {name}: {str(output)[:80]}")
