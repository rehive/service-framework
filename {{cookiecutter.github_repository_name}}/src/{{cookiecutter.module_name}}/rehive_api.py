import requests

from rehive import Rehive
from {{cookiecutter.module_name}}.models import ExternalSyncTask
from {{cookiecutter.module_name}}.enums import APISelectionEnum

class RehiveApiInterface:

    def __init__(self, company):
        self.company = company
        self.api_token = self.company.admin.token

    def update_rehive_transaction(self, data_to_update):
        # Create a SyncTask object
        task = ExternalSyncTask.objects.create(
            data=data_to_update,
            method='PATCH',
            api=APISelectionEnum.REHIVE
        )
