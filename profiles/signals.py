from django import dispatch

follow_notification = dispatch.Signal(use_caching=True)