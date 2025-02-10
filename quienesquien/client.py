from dataclasses import dataclass, fields

import requests

from .person import Person


@dataclass
class SearchResult:
    success: bool
    num_registros: int
    persons: list[Person]


@dataclass
class Client:
    base_url = 'https://app.q-detect.com/'
    username: str
    client_id: str
    secret_key: str

    def _fetch_auth_token(self) -> str:
        """Retrieve authentication token from the API."""
        auth_url = f'{self.base_url}/api/token?client_id={self.client_id}'
        headers = {'Authorization': f'Bearer {self.secret_key}'}

        response = requests.get(auth_url, headers=headers)
        response.raise_for_status()

        return response.text

    def search(
        self,
        nombre: str,
        paterno: str,
        materno: str,
        match_score: int = 60,
        rfc: str | None = None,
        curp: str | None = None,
        sex: str | None = None,
        birthday: str | None = None,
        search_type: int | None = None,
        search_list: str | None = None,
    ) -> SearchResult:
        """Perform a search request and return the results.

        Args:
            nombre: First name(s)
            paterno: First surname
            materno: Second surname
            match_score: Minimum match percentage (default: 60)
            rfc: Mexican RFC
            curp: Mexican CURP
            sex: Gender - 'M' for male, 'F' for female
            birthday: Date of birth in dd/mm/yyyy format
            search_type: Type of search - 0 for individual, 1 for company
            search_list: Comma-separated list of specific lists to search
               (e.g., 'PPE, PEPINT, VENC') if not provided, searches all
        """
        token = self._fetch_auth_token()

        # Build base URL with required parameters
        search_url = (
            f'{self.base_url}/api/find?client_id={self.client_id}'
            f'&username={self.username}&percent={match_score}'
            f'&name={nombre} {paterno} {materno}'
        )

        # Add optional parameters if provided
        if rfc:
            search_url += f'&rfc={rfc}'
        if curp:
            search_url += f'&curp={curp}'
        if sex:
            search_url += f'&sex={sex}'
        if birthday:
            search_url += f'&birthday={birthday}'
        if search_type is not None:
            search_url += f'&type={search_type}'
        if search_list:
            search_url += f'&list={search_list}'

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        response_data = response.json()
        person_fields = {field.name for field in fields(Person)}
        matched_persons = [
            Person(
                **{
                    k.lower(): v
                    for k, v in person_data.items()
                    if v is not None and k.lower() in person_fields
                }
            )
            for person_data in response_data.get('data', [])
        ]

        return SearchResult(
            success=response_data.get('success', False),
            num_registros=len(matched_persons),
            persons=matched_persons,
        )
