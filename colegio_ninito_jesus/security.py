from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseForbidden
import time

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Rate limiting
        if not self.check_rate_limit(request):
            return HttpResponseForbidden('Rate limit exceeded. Please try again later.')

        # Process the request and get the response
        response = self.get_response(request)

        # Add security headers
        self.add_security_headers(response)
        
        return response

    def add_security_headers(self, response):
        # Add security headers to the response
        headers = {
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'same-origin',
            'Permissions-Policy': "geolocation=(), microphone=(), camera=()",
            'Cache-Control': 'no-store, max-age=0',
        }
        
        for header, value in headers.items():
            if header not in response:
                response[header] = value

    def check_rate_limit(self, request):
        """
        Basic rate limiting implementation
        Allows 100 requests per minute per IP
        """
        if settings.DEBUG:
            return True
            
        ip = self.get_client_ip(request)
        cache_key = f'rate_limit_{ip}'
        
        # Get the current request count and timestamp
        request_data = cache.get(cache_key, {'count': 0, 'timestamp': time.time()})
        
        # Reset counter if more than a minute has passed
        if time.time() - request_data['timestamp'] > 60:
            request_data = {'count': 0, 'timestamp': time.time()}
        
        # Increment request count
        request_data['count'] += 1
        
        # Store the updated count
        cache.set(cache_key, request_data, 60)  # Cache for 1 minute
        
        # Allow up to 100 requests per minute
        return request_data['count'] <= 100
    
    def get_client_ip(self, request):
        """Get the client's IP address from the request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
