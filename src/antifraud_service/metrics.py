from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response

# 1. Счетчик всех HTTP запросов
requests_total = Counter(
    'antifraud_requests_total',
    'Total requests to antifraud service',
    ['method', 'endpoint', 'status']
)

# 2. Счетчик проверок пользователей
user_checks_total = Counter(
    'antifraud_user_checks_total',
    'Total user checks',
    ['result']
)

# 3. Счетчик попаданий в кэш Redis
cache_hits = Counter(
    'antifraud_cache_hits',
    'Redis cache hits',
    ['type']
)

# 4. Гистограмма времени проверки
check_duration = Histogram(
    'antifraud_check_duration_seconds',
    'Time to check user'
)
# 5. Количество запросов с разбивкой по HTTP-статусам ответов
http_requests_by_status = Counter(
    'http_requests_by_status_total',
    'HTTP requests by status code',
    ['status_code']
)

# 6. Время ответа на запрос с разбивкой по HTTP-статусам ответов
http_response_time_by_status = Histogram(
    'http_response_time_by_status_seconds',
    'HTTP response time by status code',
    ['status_code'],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
)

def get_metrics():
    return Response(generate_latest(), media_type='text/plain')