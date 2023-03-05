from mongoengine import Document

from common.serializer.strategies.strategy_manager import initialize_manager


def default(document: Document) -> Document:
    keys_to_parse: dict = {
        '_id': { 'type': 'id' },
        'organization_id': { 'type': 'id' },
        'bucket_id': { 'type': 'id' },
        'campaign_id': { 'type': 'id' },
        'event_code_id': { 'type': 'id' },
        'birthdate': { 'type': 'date' },
        'created_at': { 'type': 'date' },
        'updated_at': { 'type': 'date' },
        'start_date': { 'type': 'date' },
        'end_date': { 'type': 'date' },
    }

    for key in document:
        type: dict = keys_to_parse.get(key, {}).get('type', 'empty')
        document[key] = initialize_manager(type).parse_value(key, document)

    document.pop('password', None)

    return document
