"""HTTP client for geosearoute RapidAPI endpoints."""

from __future__ import annotations

from typing import Any, Optional

import requests

from .models import NearestQuery, ServiceConfig, ServiceRequest, ServiceResponse, SolveQuery


class GeoSeaRouteClient:
	"""Thin client for the fixed geosearoute RapidAPI integration."""

	def __init__(self, config: ServiceConfig, session: Optional[Any] = None, timeout: int = 30) -> None:
		self.config = config
		self.session = session or requests.Session()
		self.timeout = timeout

	def build_nearest_request(self, query: NearestQuery) -> ServiceRequest:
		return ServiceRequest(
			method="GET",
			path="/nearest",
			query_params={"lat": query.latitude, "lon": query.longitude, "distance": query.distance_km},
			json_body=None,
			headers=self._build_headers(),
		)

	def build_solve_request(self, query: SolveQuery) -> ServiceRequest:
		stops = [[stop.longitude, stop.latitude] for stop in query.stops]
		return ServiceRequest(
			method="POST",
			path="/solve",
			query_params={"speed": query.speed_knots},
			json_body={"stops": stops},
			headers=self._build_headers(),
		)

	def nearest(self, query: NearestQuery) -> ServiceResponse:
		return self._send(self.build_nearest_request(query))

	def solve(self, query: SolveQuery) -> ServiceResponse:
		return self._send(self.build_solve_request(query))

	def _build_headers(self) -> dict:
		return {
			"x-rapidapi-host": self.config.rapidapi_host,
			"x-rapidapi-key": self.config.rapidapi_key,
		}

	def _send(self, request: ServiceRequest) -> ServiceResponse:
		try:
			response = self.session.request(
				request.method,
				f"{self.config.base_url}{request.path}",
				params=request.query_params,
				json=request.json_body,
				headers=request.headers,
				timeout=self.timeout,
			)
		except Exception as exc:
			return ServiceResponse(
				status_code=None,
				payload=None,
				raw_text=str(exc),
				is_success=False,
				error_category="transport",
			)

		payload = None
		try:
			payload = response.json()
		except ValueError:
			payload = None

		raw_text = getattr(response, "text", None)
		if isinstance(raw_text, str):
			raw_text = raw_text.strip() or None

		return ServiceResponse(
			status_code=response.status_code,
			payload=payload,
			raw_text=raw_text,
			is_success=bool(response.ok),
			error_category=None if response.ok else "remote",
		)
