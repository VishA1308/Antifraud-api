from fastapi import FastAPI
from .models import UserCreate
from .redis_client import redis_client
from .metrics import requests_total, user_checks_total, cache_hits, check_duration, get_metrics
import time

app = FastAPI(title="antifraud service")

@app.post("/users/", status_code=201)
async def create_user(user: UserCreate):
    # Начинаем замер времени проверки
    start_time = time.time()
    
    # 1. Пробуем взять из Redis кэша
    cached = await redis_client.get_user_result(user.phone_number, user.birth_date)
    if cached:
        # Увеличиваем счетчик кэш-попаданий
        cache_hits.labels(type="hit").inc()
        # Увеличиваем счетчик проверок (результат из кэша)
        user_checks_total.labels(result="cached").inc()
        # Замеряем время (оно будет маленьким)
        check_duration.observe(time.time() - start_time)
        # Увеличиваем счетчик HTTP запросов
        requests_total.labels(method="POST", endpoint="/users/", status=201).inc()
        return cached
    
    # Если не в кэше - увеличиваем счетчик кэш-промахов
    cache_hits.labels(type="miss").inc()
    
    # 2. Выполняем проверки
    errors = []
    
    if user.is_under_18():
        errors.append("Пользователь младше 18")
    
    if user.is_not_rus_phone():
        errors.append("Не российский номер")
    
    if user.has_open_loans():
        errors.append("Займ не закрыт")
    
    # 3. Формируем результат
    result = {
        "stop_factors": errors,
        "result": len(errors) == 0  # True если ошибок нет
    }
    
    # 4. Сохраняем в Redis
    await redis_client.set_user_result(user.phone_number, user.birth_date, result)
    
    # 5. Обновляем метрики
    duration = time.time() - start_time
    check_duration.observe(duration)
    
    # Считаем результат проверки
    if len(errors) == 0:
        user_checks_total.labels(result="approved").inc()
    else:
        user_checks_total.labels(result="rejected").inc()
    
    # Считаем HTTP запрос
    requests_total.labels(method="POST", endpoint="/users/", status=201).inc()
    
    return result

@app.get("/metrics")
async def metrics():
    """Отдает метрики для Prometheus"""
    return get_metrics()