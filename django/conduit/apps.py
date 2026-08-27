from django.apps import AppConfig
from rest_framework.serializers import Serializer

class ConduitConfig(AppConfig):
    name = 'conduit'

    def ready(self):
        # update Serializer __init__ so that it uses our custom 'blank' error message
        original__init = Serializer.__init__

        def updated_init(self, *args, **kwargs):
            original__init(self, *args, **kwargs)

            CUSTOM_BLANK_MESSAGE = "can't be blank"

            for field in self.fields.values():
                
                field.error_messages["blank"] = CUSTOM_BLANK_MESSAGE

        Serializer.__init__ = updated_init