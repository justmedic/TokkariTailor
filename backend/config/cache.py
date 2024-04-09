from django.core.cache import cache
from django.http import JsonResponse
import json
from functools import wraps
import time

def cache_heavy_get_requests(timeout=86400):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method != 'GET':
                return view_func(request, *args, **kwargs)

            cache_key = f"{request.path}-{request.META.get('QUERY_STRING', '')}"
            cached_response_data = cache.get(cache_key)
            if cached_response_data is not None:
                # Преобразуем обратно в словарь для создания DRF Response
                return JsonResponse(json.loads(cached_response_data), safe=False)

            response = view_func(request, *args, **kwargs)
            if response.status_code == 200:
                start_time = time.time()
                response_content = response.data  # Обеспечьте рендеринг перед получением content
                elapsed_time = time.time() - start_time
            
                if elapsed_time > 0.5:
                    cache.set(cache_key, response_content, timeout)
            return response

        return _wrapped_view
    return decorator
