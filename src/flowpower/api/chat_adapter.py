from fastapi.responses import StreamingResponse

def sse_adapter(generator):
    """Wrap a token-yielding generator in an SSE-compatible stream."""
    async def event_stream():
        for token in generator:
            yield f"data: {token}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
