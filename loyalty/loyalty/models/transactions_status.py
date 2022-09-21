from enum import Enum


class TransactionStatus(Enum):
    PENDING = 'pending'
    PROCESSED = 'processed'
    ERROR = 'error'
    PARTIAL_ERROR = 'partial_error'
