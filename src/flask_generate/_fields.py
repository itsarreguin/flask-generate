from ._utils import _get_field_name_and_type


peewee_fields = {
    'big-int': 'BitIntegerField()',
    'bool': 'BooleanField()',
    'date': 'DateField()',
    'datetime': 'DateTimeField()',
    'decimal': 'DecimalField()',
    'double': 'DoublueField()',
    'file': 'CharField(max_length=255)',
    'float': 'FloatField()',
    'int': 'IntegerField()',
    'small-int': 'SmallIntegerField()',
    'str': 'CharField(max_length=255)',
    'text': 'TextField()',
    'time': 'TimeField()',
    'timestamp': 'TimeStampField()',
    'uuid': 'UUIDField()',
}

sqlalchemy_fields = {
    'big-int': 'BigInteger',
    'bool': 'Boolean',
    'date': 'Date',
    'datetime': 'DateTime',
    'decimal': 'Decimal',
    'double': 'Double',
    'file': 'String',
    'float': 'Float',
    'int': 'Integer',
    'small-int': 'SmallInteger',
    'str': 'String',
    'text': 'Text',
    'time': 'Time',
    'uuid': 'Uuid'
}


def _make_form_label(value: str) -> str:
    field, _ = _get_field_name_and_type(value)
    field = (
        field.replace('_', ' ').replace('-', ' ') if '_' or '-' in value
        else value
    )
    return field.title()


def field_name(value: str) -> str:
    field_name, _ = _get_field_name_and_type(value).lower()
    return field_name


def field_type(value: str) -> str:
    _, field_type = _get_field_name_and_type(value)
    return field_type


def form_field(value: str) -> str:
    field_name, field_type = _get_field_name_and_type(value)
    field_label: str = _make_form_label(field_name)

    form_fields = {
        'bool': f"BooleanField(label='{field_label}')",
        'str': f"StringField(label='{field_label}')",
        'file': f"FileField(label='{field_label}')",
    }
    return form_fields[field_type]


def import_fields(value: str) -> str:
    pass


def table_field(orm: str, value: str) -> str:
    _, field_type = _get_field_name_and_type(value)

    if orm == 'sqla':
        return f'mapped_column({sqlalchemy_fields[field_type]})'
    return peewee_fields[field_type]