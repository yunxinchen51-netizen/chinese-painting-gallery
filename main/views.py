import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import LayoutSettings

@csrf_exempt
def layout_positions(request):
    """Read or update the shared layout positions."""
    setting, _ = LayoutSettings.objects.get_or_create(key='gallery-layout-positions')
    if request.method == 'GET':
        return JsonResponse({'positions': setting.positions})
    if request.method == 'POST':
        try:
            payload = json.loads(request.body or '{}')
            positions = payload.get('positions', payload)
            if not isinstance(positions, dict):
                raise ValueError('positions must be an object')
        except (json.JSONDecodeError, ValueError, TypeError):
            return JsonResponse({'error': 'Invalid positions payload'}, status=400)
        setting.positions = positions
        setting.save(update_fields=['positions', 'updated_at'])
        return JsonResponse({'positions': setting.positions})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
