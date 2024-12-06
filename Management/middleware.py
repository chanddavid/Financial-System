from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.http import Http404
from rest_framework.views import exception_handler
from finance.logger import logger
import json


class IncomingRequestHandleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"{request.method}")
        logger.info(f"{request.get_full_path()}")
        logger.info(f"{dict(request.headers)}")

        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                body = json.loads(request.body)
                logger.info(f"{json.dumps(body)}")
            except ValueError:
                logger.info("Request Body: Invalid JSON")
        
        response = self.get_response(request)

        logger.info(f"{response.status_code}")
        return response
    

class ErrorHandleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except ValidationError as e:
            logger.exception(stack_info=False, msg=f"validation error={e.args}")
            return JsonResponse({'error': 'Invalid data', 'details': str(e)}, status=400)
        
        except IntegrityError as e:
            logger.exception(stack_info=False,msg=f"Integrity error: {str(e)}")
            return JsonResponse({'error': 'Database error', 'details': str(e)}, status=400)
        
        except Http404 as e:
            logger.error(stack_info=False, msg=f"404 error: {str(e)}")
            return JsonResponse({'error': 'Resource not found', 'details': str(e)}, status=404)
        
        except Exception as e:
            logger.error(stack_info=False, msg=f"Unexpected error: {str(e)}")
            return JsonResponse({'error': 'An unexpected error occurred', 'details': str(e)}, status=500)
        
        return response