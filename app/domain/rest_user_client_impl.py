from typing import Optional

import httpx
from pydantic import ValidationError

from app.core.rest_user_config import RestUserConfig
from app.domain.UserEntity import UserEntity
from app.domain.rest_user_client import RestUserClient

class RestUserClientImpl(RestUserClient):
    def __init__(self):
        rest_user_config = RestUserConfig()
        self._client = httpx.AsyncClient(base_url=rest_user_config.rest_user_base_url)

    def _build_url(self, path: str, **kwargs) -> str:
        return path.format(**kwargs)

    async def get_user(self, user_id: int) -> Optional[UserEntity]:
        # url = f"/users/{user_id}"
        url = self._build_url("/users/{user_id}", user_id=user_id)
        response = await self._client.get(url)

        if response.status_code == 404:
            return None  # 没找到用户
        response.raise_for_status()

        try:
            return UserEntity(**response.json())
        except ValidationError:
            return None  # 数据结构不匹配，返回 None

    async def close(self):
        await self._client.aclose()


