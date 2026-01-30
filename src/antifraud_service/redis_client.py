import redis.asyncio as redis
import json


class RedisClient:
    def __init__(self, host='redis', port=6379):
        self.client = redis.Redis(host=host, port=port)
    
    
    async def get_user_result(self, phone_number, birth_date):
        user_key = f"user:{phone_number}:{birth_date}"

        result = await self.client.get(user_key)
        if result:
            return json.loads(result)
        return None
    
    async def set_user_result(self, phone_number, birth_date, result):
        user_key = f"user:{phone_number}:{birth_date}"
        await self.client.set(user_key, json.dumps(result))


   
redis_client = RedisClient()