"""
Constants module
"""

from enum import Enum


class JobStatus(Enum):
    """
    Job status enum
    """
    NOT_STARTED = 'Not Started'
    QUEUED = 'Queued'


class RequestStatus(Enum):
    """
    A request status enum
    """
    SUCCESS = 'success'
    FAILED = 'failed'
