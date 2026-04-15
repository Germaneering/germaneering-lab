"""Tests for geosearoute client behavior."""

import unittest
from unittest import mock

from geosearoute_cli.client import GeoSeaRouteClient
from geosearoute_cli.models import (
	ServiceConfig,
	NearestQuery,
	StopCoordinate,
	SolveQuery,
)


class TestGeoSeaRouteClient(unittest.TestCase):
	"""Test request construction and response normalization."""

	def setUp(self):
		self.config = ServiceConfig(
			base_url="https://geosearoute.p.rapidapi.com",
			rapidapi_host="geosearoute.p.rapidapi.com",
			rapidapi_key="secret-key",
		)
		self.session = mock.Mock()
		self.client = GeoSeaRouteClient(self.config, session=self.session, timeout=5)

	def test_builds_nearest_request(self):
		request = self.client.build_nearest_request(NearestQuery(57.7089, 11.9746))

		self.assertEqual(request.method, "GET")
		self.assertEqual(request.path, "/nearest")
		self.assertEqual(request.query_params["distance"], 500.0)
		self.assertEqual(request.headers["x-rapidapi-host"], "geosearoute.p.rapidapi.com")
		self.assertEqual(request.headers["x-rapidapi-key"], "secret-key")

	def test_builds_solve_request(self):
		query = SolveQuery(
			stops=(
				StopCoordinate(11.9746, 57.7089, 0),
				StopCoordinate(4.47917, 51.9225, 1),
			),
			speed_knots=24.0,
		)
		request = self.client.build_solve_request(query)

		self.assertEqual(request.method, "POST")
		self.assertEqual(request.path, "/solve")
		self.assertEqual(request.query_params["speed"], 24.0)
		self.assertEqual(request.json_body, {"stops": [[11.9746, 57.7089], [4.47917, 51.9225]]})

	def test_normalizes_json_response(self):
		response = mock.Mock()
		response.status_code = 200
		response.ok = True
		response.json.return_value = {"point": {"lat": 57.701}}
		response.text = '{"point": {"lat": 57.701}}'
		self.session.request.return_value = response

		result = self.client.nearest(NearestQuery(57.7089, 11.9746))

		self.assertTrue(result.is_success)
		self.assertEqual(result.payload["point"]["lat"], 57.701)

	def test_transport_errors_are_normalized(self):
		self.session.request.side_effect = RuntimeError("boom")

		result = self.client.nearest(NearestQuery(57.7089, 11.9746))

		self.assertFalse(result.is_success)
		self.assertEqual(result.error_category, "transport")