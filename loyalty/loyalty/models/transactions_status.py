from enum import Enum

class TransactionStatus(Enum):
    PENDING = 'pending'
    PROCESSED = 'processed'
    ERRORED = 'errored'
    PARTIAL_ERRORED = 'partial_errored'