from rest_framework import throttling

class ChangePasswordThrottle(throttling.UserRateThrottle):
    scope = 'change_password'