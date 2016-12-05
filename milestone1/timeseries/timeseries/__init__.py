import pkg_resources

from timeseries.lazy import *
from timeseries.TimeSeries import *
from timeseries.ArrayTimeSeries import *
from timeseries.SimulatedTimeSeries import *
from timeseries.StreamTimeSeriesInterface import *
from timeseries.SizedContainerTimeSeriesInterface import *
from timeseries.TimeSeriesInterface import *

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except:
    __version__ = 'unknown'
