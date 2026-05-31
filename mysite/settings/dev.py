from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 注意：生产环境必须使用随机生成的SECRET_KEY，不能硬编码！
SECRET_KEY = "django-insecure-&x51)y333@7k!4n=^(fd4(adu@i9xul#gtue!&$ntdroqps1c4"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*.localhost", "*"]

# 开发环境邮件后端 - 邮件输出到控制台
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# 开发环境调试工具配置
if DEBUG:
    INSTALLED_APPS += ["django_extensions"]
    
    # 日志配置
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "INFO",
            },
        },
    }


