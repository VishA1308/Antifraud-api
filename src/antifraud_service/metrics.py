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

def get_metrics():
    return Response(generate_latest(), media_type='text/plain')