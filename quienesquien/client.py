import datetime as dt
from dataclasses import dataclass
from typing import Mapping

import httpx

from .enums import Gender, SearchList, SearchType
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

    async def _get_client(self) -> httpx.AsyncClient:
        """Create and return an httpx.AsyncClient instance."""
        return httpx.AsyncClient()

    async def _make_request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, str | int | None] | None = None,
    ) -> httpx.Response:
        """Make an HTTP request using an async client."""
        async with await self._get_client() as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
            )
            response.raise_for_status()
            return response

    async def _fetch_auth_token(self) -> str:
        """Retrieve authentication token from the API."""
        if self._auth_token is not None:
            return self._auth_token

        auth_url = f'{self.base_url}/api/token'
        params = {'client_id': self.client_id}
        headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Accept-Encoding': 'identity',
        }

        response = await self._make_request(
            'GET', auth_url, headers=headers, params=params
        )
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
        gender: Gender | None = None,
        birthday: dt.date | None = None,
        search_type: SearchType | None = None,
        search_list: tuple[SearchList, ...] | None = None,
    ) -> SearchResult:
        """Perform a search request and return the results.

        Args:
            nombre (str): First name(s) of the person.
            paterno (str): First surname.
            materno (str): Second surname.
            match_score (int, opt.): Minimum match percentage (default: 60).
            rfc (str, opt.): Mexican RFC.
            curp (str, opt.): Mexican CURP.
            gender (Gender, opt.): masculino or femenino.
            birthday (datetime.date, opt.): Date of birth.
            search_type (SearchType, opt.): fisica or moral.
            search_list (tuple[SearchList, ...], opt.): Lists to search.
               If not provided, searches all.
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
        if gender:
            params['sex'] = gender.value
        if birthday:
            params['birthday'] = birthday.strftime('%d/%m/%Y')
        if search_type is not None:
            params['type'] = search_type.value
        if search_list:
            params['list'] = ','.join(item.value for item in search_list)

        headers = {'Authorization': f'Bearer {token}'}

        response = await self._make_request(
            'GET', search_url, params=params, headers=headers
        )
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
