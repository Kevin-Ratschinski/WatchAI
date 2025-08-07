from typing import List

from pydantic import BaseModel, Field


class OllamaConfig(BaseModel):
    host: str
    model: str


class WatcherConfig(BaseModel):
    name: str
    enabled: bool
    interval_seconds: int = Field(..., alias='interval')
    prompt: str


class ActionConfig(BaseModel):
    name: str
    enabled: bool


class Config(BaseModel):
    ollama: OllamaConfig
    watchers: List[WatcherConfig]
    actions: List[ActionConfig]
