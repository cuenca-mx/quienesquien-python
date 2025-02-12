from dataclasses import dataclass

import httpx

from .person import Person


@dataclass
class SearchResult:
    success: bool
    num_registros: int
    persons: list[Person]


@dataclass
class Client:
    base_url = 'https://app.q-detect.com'
    username: str
    client_id: str
    secret_key: str
    _auth_token: str | None = None

    async def _fetch_auth_token(self) -> str:
        """Retrieve authentication token from the API."""
        if self._auth_token is not None:
            return self._auth_token

        auth_url = f'{self.base_url}/api/token?client_id={self.client_id}'
        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Accept-Encoding': 'identity',
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(auth_url, headers=headers)
            response.raise_for_status()
            self._auth_token = response.text
            return self._auth_token

    async def search(
        self,
        nombre: str,
        paterno: str,
        materno: str,
        match_score: int = 60,  # Default 60, applied even if no value provided
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
        token = await self._fetch_auth_token()

        # Build base URL with required parameters
        search_url = f'{self.base_url}/api/find'

        params: dict[str, str | int | None] = {
            'client_id': self.client_id,
            'username': self.username,
            'percent': match_score,
            'name': f'{nombre} {paterno} {materno}',
        }

        # Add optional parameters if provided
        if rfc:
            params['rfc'] = rfc
        if curp:
            params['curp'] = curp
        if sex:
            params['sex'] = sex
        if birthday:
            params['birthday'] = birthday
        if search_type is not None:
            params['type'] = search_type
        if search_list:
            params['list'] = search_list

        headers = {'Authorization': f'Bearer {token}'}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                search_url, params=params, headers=headers
            )
            response.raise_for_status()
            response_data = response.json()

        matched_persons = [
            Person(**person_data)
            for person_data in response_data.get('data', [])
        ]

        return SearchResult(
            success=response_data.get('success', False),
            num_registros=len(matched_persons),
            persons=matched_persons,
        )
