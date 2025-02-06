import requests

from .person import PERSON_FIELDNAMES, Person


class Client:

    client_user = None
    client_url = None
    client_id = None
    secret_id = None
    percent = 80

    def __init__(self, url: str, user: str, client_id: str, secret_id: str):
        """
        Configura el endpoint y las credenciales para realizar busquedas
        :param url: https://peps.mx/datos/qws
        :param user: usuario
        :param client_id: client_id
        :param secret_id: secret_id
        :return:
        """
        self.client_user = user
        self.client_url = url
        self.client_id = client_id
        self.secret_id = secret_id

    def search(self, nombre, paterno, materno):
        login_url = f'{self.client_url}/api/token?client_id={self.client_id}'
        headers = {'Authorization': f'Bearer {self.secret_id}'}

        login_response = requests.get(login_url, headers=headers)

        token = login_response.text

        url = f'{self.client_url}/api/find?client_id={self.client_id}'\
        f'&username={self.client_user}&percent={self.percent}'\
        f'&name={nombre} {paterno} {materno}'

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)

        data = response.json()

        persons = []
        for person in data.get('data', []):
            kwargs = dict()
            for field in PERSON_FIELDNAMES:
                if field in person:
                    kwargs[field] = person[field]
            persons.append(Person(kwargs))

        resumen = dict(
            success=data['success'],
            num_registros=len(persons),
        )
        return dict(resumen=resumen, persons=persons)
