from fastapi import FastAPI
from .models import UserCreate
from .redis_client import redis_client
from .metrics import (
    requests_total,
    user_checks_total,
    cache_hits,
    check_duration,
    http_requests_by_status,          # <-- ДОБАВЬ
    http_response_time_by_status,     # <-- ДОБАВЬ
    get_metrics
)
import time

app = FastAPI(title="antifraud service")

@app.post("/users/", status_code=201)
async def create_user(user: UserCreate):
    # Начинаем замер ВСЕГО времени запроса
    total_start_time = time.time()
    
    # Начинаем замер времени проверки
    check_start_time = time.time()
    
    # Проверяем кэш
    cached = await redis_client.get_user_result(user.phone_number, user.birth_date)
    if cached:
        cache_hits.labels(type="hit").inc()
        user_checks_total.labels(result="cached").inc()
        
        check_duration.observe(time.time() - check_start_time)
        
        # НОВОЕ: Время всего запроса
        total_duration = time.time() - total_start_time
        http_response_time_by_status.labels(status_code=201).observe(total_duration)
        
        # НОВОЕ: Счетчик запросов по статусу
        http_requests_by_status.labels(status_code=201).inc()
        
        requests_total.labels(method="POST", endpoint="/users/", status=201).inc()
        return cached
    
    cache_hits.labels(type="miss").inc()
    
    # Выполняем проверки
    errors = []
    
    if user.is_under_18():
        errors.append("Пользователь младше 18")
    
    if user.is_not_rus_phone():
        errors.append("Не российский номер")
    
    if user.has_open_loans():
        errors.append("Займ не закрыт")
    
    result = {
        "stop_factors": errors,
        "result": len(errors) == 0
    }
    
    # Сохраняем в кэш
    await redis_client.set_user_result(user.phone_number, user.birth_date, result)
    
    # Обновляем бизнес-метрики
    if len(errors) == 0:
        user_checks_total.labels(result="approved").inc()
    else:
        user_checks_total.labels(result="rejected").inc()
    
    check_duration.observe(time.time() - check_start_time)
    
    # НОВОЕ: Время всего запроса
    total_duration = time.time() - total_start_time
    http_response_time_by_status.labels(status_code=201).observe(total_duration)
    
    # НОВОЕ: Счетчик запросов по статусу
    http_requests_by_status.labels(status_code=201).inc()
    
    requests_total.labels(method="POST", endpoint="/users/", status=201).inc()
    
    return result

@app.get("/metrics")
async def metrics():
    return get_metrics()