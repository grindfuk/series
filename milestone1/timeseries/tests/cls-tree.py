import inspect
from pprint import pprint
from SimulatedTimeSeries import SimulatedTimeSeries
from StreamTimeSeriesInterface import StreamTimeSeriesInterface
from TimeSeriesInterface import TimeSeriesInterface
from SizedContainerTimeSeriesInterface import SizedContainerTimeSeriesInterface
from TimeSeries import TimeSeries
from ArrayTimeSeries import ArrayTimeSeries


for cls in [TimeSeriesInterface, SizedContainerTimeSeriesInterface, TimeSeries, ArrayTimeSeries,
            StreamTimeSeriesInterface, SimulatedTimeSeries]:
    breakdown = inspect.getmembers(cls)
    print(cls.__name__)
    for key, value in breakdown:
        if key in ['__doc__', '__module__', '__dict__']:
            continue
        if ' ' + cls.__name__ + '.' in str(value):
            print(4*' ' + key) #, str(breakdown[key]))
