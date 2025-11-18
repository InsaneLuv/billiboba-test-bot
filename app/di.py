from __future__ import annotations

from typing import Any, Mapping

from dishka import provide, Provider, Scope
from pymongo import AsyncMongoClient
from openai import OpenAI
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from app.config import get_settings, Settings
from app.services.chatgpt import ChatService


class AppProvider(Provider):
    scope = Scope.APP

    @provide
    def settings(self) -> Settings:
        return get_settings()

    @provide
    def openai_client(self, settings: Settings) -> OpenAI:
        return OpenAI(api_key=settings.openai_api_key.get_secret_value())

    @provide
    def mongo_client(self, settings: Settings) -> AsyncMongoClient:
        return AsyncMongoClient(settings.mongodb_uri)

    @provide
    def mongo_db(self, mongo_client: AsyncMongoClient, settings: Settings) -> AsyncDatabase:
        return mongo_client[settings.database_name]

    @provide
    def history_collection(self, mongo_db: AsyncDatabase, settings: Settings) -> AsyncCollection:
        return mongo_db[settings.history_collection]

    @provide
    def chat_service(
            self,
            openai_client: OpenAI,
            history_collection: AsyncCollection,
            settings: Settings,
    ) -> ChatService:
        return ChatService(openai_client, history_collection, settings)
