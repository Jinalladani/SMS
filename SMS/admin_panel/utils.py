from admin_panel import models


def get_credentials(key):
    """
    Get credentials from database
    :return: credentials
    """
    try:
        return models.SettingModel.objects.get(key=key).value
    except models.SettingModel.DoesNotExist:
        if key == "EMAIL_BACKEND":
            settings = models.SettingModel.objects.create(key=key, value="django.core.mail.backends.smtp.EmailBackend")
        if key == "EMAIL_HOST":
            settings = models.SettingModel.objects.create(key=key, value="smtp.gmail.com")
        if key == "EMAIL_PORT":
            settings = models.SettingModel.objects.create(key=key, value="587")
        if key == "EMAIL_HOST_USER":
            settings = models.SettingModel.objects.create(key=key, value="societyfunds@gmail.com")
        if key == "EMAIL_HOST_PASSWORD":
            settings = models.SettingModel.objects.create(key=key, value="Bonrix@#123")
        if key == "EMAIL_USE_TLS":
            settings = models.SettingModel.objects.create(key=key, value=True)
        if key == "SMSURL":
            settings = models.SettingModel.objects.create(key=key, value="http://quicksms.highspeedsms.com/sendsms/sendsms.php?username=BREbonrix&password=sales55&type=TEXT&sender=BONRIX&mobile={phone_no}&message=Your%20OTP%20for%20login%20verification%20is%20:=%20{otp}")
        
        return settings.value