from ._utils import _get_field_name_and_type, _to_snake_case


sqla_mapping_types = {
    'big-int': 'int',
    'bool': 'bool',
    'date': 'date',
    'datetime': 'datetime',
    'decimal': 'decimal',
    'double': 'float',
    'file': 'str',
    'float': 'float',
    'int': 'int',
    'small-int': 'int',
    'str': 'str',
    'text': 'str',
    'time': 'time',
    'uuid': 'UUID'
}

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
    label = (
        value.replace('_', ' ').replace('-', ' ') if '_' or '-' in value
        else value
    )
    return label.title()


def field_name(value: str) -> str:
    field_name, _ = _get_field_name_and_type(value)
    return field_name.lower()


def field_type(value: str) -> str:
    _, field_type = _get_field_name_and_type(value)
    return sqla_mapping_types[field_type]


def form_field(value: str) -> str:
    field_name, field_type = _get_field_name_and_type(value)
    field_label: str = _make_form_label(field_name)

    form_fields = {
        'bool': f"BooleanField(label='{field_label}')",
        'date': f"DateField(label='{field_label}')",
        'datetime': f"DateTimeField(label='{field_label}')",
        'email': f"EmailField(label='{field_label}')",
        'file': f"FileField(label='{field_label}')",
        'float': f"FloatField(label='{field_label}')",
        'int': f"IntegerField(label='{field_label}')",
        'str': f"StringField(label='{field_label}')",
        'tel': f"TelField(label='{field_label}')",
        'time': f"TimeField(label='{field_label}')",
        'url': f"URLField(label='{field_label}')",
    }
    return form_fields[field_type]


def import_fields(fields: list[str]) -> str:
    field_list = [
        sqlalchemy_fields[_get_field_name_and_type(field)[1]] for field in fields
    ]
    return ', '.join(field_list)


def table_field(orm: str, value: str) -> str:
    _, field_type = _get_field_name_and_type(value)

    if orm == 'sqlalchemy':
        return f'mapped_column({sqlalchemy_fields[field_type]})'
    return peewee_fields[field_type]


def table_name(value: str) -> str:
    return _to_snake_case(value)