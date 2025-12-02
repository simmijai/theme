# redis_otp.py - REPLACE ALL CONTENT WITH THIS:
import random
import json
from django.core.cache import cache
from django.utils import timezone
import time

class RedisOTPManager:
    
    @staticmethod
    def generate_otp(email):
        """Generate and store OTP"""
        otp = str(random.randint(100000, 999999))
        
        # Check rate limit
        attempts_key = f"otp_attempts:{email}"
        attempts = cache.get(attempts_key, 0)
        
        if attempts >= 3:
            return None, "Too many OTP attempts. Try again in 5 minutes."
        
        # Store OTP for 10 minutes (600 seconds)
        cache.set(f"otp:{email}", otp, timeout=600)
        
        # Update attempts (expire in 5 minutes = 300 seconds)
        cache.set(attempts_key, attempts + 1, timeout=300)
        
        return otp, None
    
    @staticmethod
    def verify_otp(email, entered_otp):
        """Verify OTP"""
        stored_otp = cache.get(f"otp:{email}")
        
        if not stored_otp:
            return False, "OTP expired or not found"
        
        if stored_otp == entered_otp:
            # Delete after successful verification
            cache.delete(f"otp:{email}")
            return True, "OTP verified successfully"
        
        return False, "Invalid OTP"
    
    @staticmethod
    def cleanup_otp(email):
        """Remove OTP"""
        cache.delete(f"otp:{email}")
        cache.delete(f"otp_attempts:{email}")
    
    @staticmethod
    def get_remaining_time(email):
        """Get remaining time for OTP"""
        try:
            # Get TTL (Time To Live) from cache
            import django
            if django.VERSION >= (4, 0):
                # Django 4.0+ has ttl() method
                remaining = cache.ttl(f"otp:{email}")
            else:
                # For older Django, simulate TTL
                remaining = 600  # Default 10 minutes
        except:
            remaining = 600
        
        return remaining if remaining and remaining > 0 else 0