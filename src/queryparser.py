class QueryParser:

    def __init__(self):
        pass

    def read(self, path='queries.sql'):
        with open(path, 'r', encoding='utf-8') as sql_file:
            queries_raw = sql_file.read()
        queries_list = queries_raw.split(';')
        queries = {}
        for query_raw in queries_list:
            if query_raw:
                query_and_comment = query_raw.strip().split('\n')
                comment = query_and_comment[0]
                query = '\n'.join(query_and_comment[1:]).strip()
                assert comment.startswith('--', 0, 2), f'Wrong query format near {query_raw}'
                name = comment[2:]
                queries[name] = query
        self.queries = queries

    def get_query(self, key):
        try:
            if key in self.queries:
                return self.queries
            else:
                raise KeyError('No such query in file')
        except AttributeError:
            raise Exception('Query file not read')
