import boto


class CounterPool(object):
    '''
    Handles schema level interactions with DynamoDB and generates individual
    counters as needed.
    '''
    table_name = None
    schema = {
        'hash_key_name': 'counter_name',
        'hash_key_proto_value': 'S',
    }

    def __init__(self, aws_access_key=None, aws_secret_key=None, table_name=None, schema=None, auto_create_table=True):
        self.conn = self.get_conn(aws_access_key, aws_secret_key)
        self.table_name = table_name or self.table_name
        self.schema = schema or self.schema

        super(CounterPool, self).__init__()

    def get_conn(self, aws_access_key=None, aws_secret_key=None):
        return boto.connect_dynamodb(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )

    def get_table_name(self):
        if not self.table_name:
            raise NotImplementedError(
                'You must provide a table_name value or override the get_table_name method'
            )
        return self.table_name

    def get_schema(self):
        if not self.schema:
            raise NotImplementedError(
                'You must provide a schema value or override the get_schema method'
            )

        return self.conn.create_schema(**self.schema)

    def does_table_exist(self):
        table_name = self.get_table_name()
        existing_tables = self.conn.list_tables()

        return table_name in existing_tables
