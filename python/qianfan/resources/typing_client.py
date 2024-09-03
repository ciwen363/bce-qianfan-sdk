# Copyright (c) 2024 Baidu, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
client typing
"""

from typing import Any, List, Optional

from typing_extensions import Literal

from qianfan.utils.pydantic import BaseModel

__all__ = ["Completion"]


class FunctionCall(BaseModel):
    parameters: Any
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: str
    """The name of the function to call."""


class SearchResult(BaseModel):
    index: int
    url: str
    title: str
    datasource_id: str


class SearchInfo(BaseModel):
    is_beset: Optional[int] = None

    rewrite_query: Optional[str] = None

    search_results: Optional[List[SearchResult]] = None


class ChatCompletionMessage(BaseModel):
    content: Optional[str] = None
    """The contents of the message."""

    role: Literal["assistant"]
    """The role of the author of this message."""

    name: Optional[str] = None

    content_type: Optional[str] = None

    function_call: Optional[FunctionCall] = None


class Choice(BaseModel):
    finish_reason: Optional[str] = None
    """The reason the model stopped generating tokens.
    "normal", "stop", "length", "tool_calls", "content_filter", "function_call"
    """

    index: int
    """The index of the choice in the list of choices."""

    message: ChatCompletionMessage
    """A chat completion message generated by the model."""

    need_clear_history: Optional[bool] = None

    ban_round: Optional[int] = None

    function_call: Optional[FunctionCall] = None

    search_info: Optional[SearchInfo] = None

    flag: Optional[int] = None

    tools_info: Optional[Any] = None


class CompletionUsage(BaseModel):
    completion_tokens: int
    """Number of tokens in the generated completion."""

    prompt_tokens: int
    """Number of tokens in the prompt."""

    total_tokens: int
    """Total number of tokens used in the request (prompt + completion)."""


class Completion(BaseModel):
    id: str
    """A unique identifier for the chat completion."""

    choices: List[Choice]
    """A list of chat completion choices.

    Can be more than one if `n` is greater than 1.
    """

    created: int
    """The Unix timestamp (in seconds) of when the chat completion was created."""

    model: str
    """The model used for the chat completion."""

    object: Literal["chat.completion"]
    """The object type, which is always `chat.completion`."""

    usage: Optional[CompletionUsage] = None
    """Usage statistics for the completion request."""


class ChoiceDelta(BaseModel):
    content: Optional[str] = None
    """The contents of the message."""


class CompletionChunkChoice(BaseModel):
    delta: ChoiceDelta
    """A chat completion delta generated by streamed model responses."""

    finish_reason: Optional[
        Literal[
            "normal", "stop", "length", "tool_calls", "content_filter", "function_call"
        ]
    ] = None
    """The reason the model stopped generating tokens."""

    index: int
    """The index of the choice in the list of choices."""


class CompletionChunk(BaseModel):
    id: str
    """A unique identifier for the chat completion. Each chunk has the same ID."""

    choices: List[CompletionChunkChoice]
    """A list of chat completion choices."""

    created: int
    """The Unix timestamp (in seconds) of when the chat completion was created.

    Each chunk has the same timestamp.
    """

    model: str
    """The model to generate the completion."""

    object: str
    """The object type"""

    usage: Optional[CompletionUsage] = None
    """
    An optional field that will only be present when you set
    `stream_options: {"include_usage": true}` in your request. When present, it
    contains a null value except for the last chunk which contains the token usage
    statistics for the entire request.
    """
