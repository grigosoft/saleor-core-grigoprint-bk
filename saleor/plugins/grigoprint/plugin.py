
from ...order.models import Order
from ..base_plugin import BasePlugin


class GrigoprintPlugin(BasePlugin):
    PLUGIN_ID = "grigo.grigoprint"
    PLUGIN_NAME = "Grigoprint"
    DEFAULT_ACTIVE = True
    PLUGIN_DESCRIPTION = "aggiunta funzionalita per prodotti personalizzati"
    CONFIGURATION_PER_CHANNEL = False

