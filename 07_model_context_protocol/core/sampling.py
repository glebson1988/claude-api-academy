import asyncio
from typing import Any

from mcp import ClientSession, types
from mcp.client.session import SamplingFnT
from mcp.shared.context import RequestContext

from core.claude import Claude


def create_sampling_callback(claude_service: Claude) -> SamplingFnT:
    async def sampling_callback(
        context: RequestContext[ClientSession, Any],
        params: types.CreateMessageRequestParams,
    ) -> types.CreateMessageResult | types.ErrorData:
        messages = []
        for message in params.messages:
            if not isinstance(message.content, types.TextContent):
                return types.ErrorData(
                    code=-32602, message="Only text sampling is supported"
                )
            messages.append(
                {"role": message.role, "content": message.content.text}
            )

        # Claude.chat uses a synchronous SDK; keep the MCP event loop available.
        response = await asyncio.to_thread(
            claude_service.chat,
            messages=messages,
            system=params.systemPrompt,
            max_tokens=params.maxTokens,
            temperature=params.temperature if params.temperature is not None else 1.0,
            stop_sequences=params.stopSequences or [],
        )

        stop_reasons = {
            "end_turn": "endTurn",
            "stop_sequence": "stopSequence",
            "max_tokens": "maxTokens",
        }
        return types.CreateMessageResult(
            role="assistant",
            model=response.model,
            content=types.TextContent(
                type="text", text=claude_service.text_from_message(response)
            ),
            stopReason=stop_reasons.get(response.stop_reason, response.stop_reason),
        )

    return sampling_callback
