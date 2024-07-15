from typing import AsyncGenerator


async def create_stream_generator(model, stream) -> AsyncGenerator[str, None]:
    async for chunk in stream:
        if chunk is not None:
            print(f"=== {chunk}")
            chunk = chunk.to_dict()
            chunk['model'] = model
            yield chunk.__str__()

