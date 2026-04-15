"""GeoSeaRoute CLI package."""

__version__ = "1.0.0"
__author__ = "Germaneering Lab"
__license__ = "Apache V2"

from .models import (
	ServiceConfig,
	NearestQuery,
	StopCoordinate,
	SolveQuery,
	ServiceRequest,
	ServiceResponse,
)

__all__ = [
	"ServiceConfig",
	"NearestQuery",
	"StopCoordinate",
	"SolveQuery",
	"ServiceRequest",
	"ServiceResponse",
	"__version__",
]
