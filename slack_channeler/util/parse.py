from datetime import datetime
from typing import Optional, Union

__all__ = ['parse_timestamp']


def parse_timestamp(ts: Union[float, datetime]) -> Optional[datetime]:
    if isinstance(ts, datetime):
        return ts

    if ts is not None:
        return datetime.utcfromtimestamp(ts)
