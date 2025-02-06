from dataclasses import dataclass
from typing import TypedDict

import requests

from .person import PERSON_FIELDNAMES, Person


class SearchResult(TypedDict):
    resumen: dict[str, int | bool]
    persons: list[Person]


@dataclass
class Client:
    client_url: str
    client_user: str
    client_id: str
    secret_id: str
    percent: int = 80

    def _get_token(self) -> str:
        login_url = f'{self.client_url}/api/token?client_id={self.client_id}'
        headers = {'Authorization': f'Bearer {self.secret_id}'}

        login_response = requests.get(login_url, headers=headers)
        login_response.raise_for_status()

        return login_response.text

    def search(self, nombre: str, paterno: str, materno: str) -> SearchResult:
        token = self._get_token()

        url = (
            f'{self.client_url}/api/find?client_id={self.client_id}'
            f'&username={self.client_user}&percent={self.percent}'
            f'&name={nombre} {paterno} {materno}'
        )

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        persons = []

        kwargs = dict()

        persons_data = data.get('data', [])

        for person in persons_data:
            for field in PERSON_FIELDNAMES:
                if person.get(field.upper()) is not None:
                    field_value = person.get(field.upper())
                    kwargs[field] = field_value
            persons.append(Person(kwargs))

        result: SearchResult = {
            'resumen': {
                'success': data['success'],
                'num_registros': len(persons),
            },
            'persons': persons,
        }

        return result
