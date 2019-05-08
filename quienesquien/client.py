import requests
import xml.etree.ElementTree as ET

from .person import Person, PERSON_FIELDNAMES


class Client:

    client_user = None
    client_password = None
    client_url = None

    def __init__(self, url: str, user: str, password: str):
        """
        Configura el endpoint y las credenciales para realizar busquedas
        :param url: https://peps.mx/datos/qws
        :param user: usuario
        :param password:  password
        :return:
        """
        self.client_user = user
        self.client_password = password
        self.client_url = url

    def search(self, nombre, paterno, materno):
        login_url = f'{self.client_url}/access?var1={self.client_user}'\
                    f'&var2={self.client_password}'
        login_response = requests.get(login_url)
        url = f'{self.client_url}/pepsp?nombre={nombre}' \
              f'&paterno={paterno}&materno={materno}'
        response = requests.get(url, cookies=login_response.cookies)
        root = ET.fromstring(response.content)
        persons = []
        for person in root.iter('persona'):
            if len(person) > 0:
                kwargs = dict()
                for field in PERSON_FIELDNAMES:
                    if person.find(field) is not None:
                        field_value = person.find(field).text
                        kwargs[field] = field_value
                persons.append(Person(kwargs))
        xml_resumen = root.find('resumen')
        resumen = dict(
            id_resultado=xml_resumen.find('id_resultado').text,
            num_registros=xml_resumen.find('num_registros').text,
            num_conex_dia=xml_resumen.find('num_conex_dia').text
        )
        return dict(
            resumen=resumen,
            persons=persons
        )
