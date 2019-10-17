from .base import *

if os.getenv('SERVER_TYPE') == "prod":
    from .prod import *
elif os.getenv('SERVER_TYPE') == "dev":
    from .dev import *
else:
    from .local import *
