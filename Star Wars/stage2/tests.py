from hstest import SQLTest, dynamic_test
from hstest import wrong, correct


class TestSQLProject(SQLTest):
    queries = {
        'create_table': None,
        'insert_data': None,
        'add_floor': None,
        'update_floor': None
    }

    @dynamic_test
    def test_queries(self):
        self.execute('create_table')
        self.execute('insert_data')
        self.execute('add_floor')

        result1 = self.execute_and_fetch_all("SELECT lower(type) as type FROM pragma_table_info('hangars') WHERE name "
                                             "= 'floor'")
        if len(result1) == 0:
            return wrong("There is no column 'floor' in the table 'hangars'")
        if 'text' not in result1[0][0]:
            return wrong("The column 'floor' was created, but it has wrong type: '" +
                         str(result1[0][0]) + "' instead of 'text'")

        self.execute('update_floor')

        result2 = self.execute_and_fetch_all("SELECT hangar_id, substr(hangar_id, 1, instr(hangar_id, '-') - 1) AS s, "
                                             "floor, count(*) over () AS cnt "
                                             "FROM hangars "
                                             "WHERE floor <> substr(hangar_id, 1, instr(hangar_id, '-') - 1) "
                                             "Limit 1;")

        if len(result2) > 0:
            return wrong(str(result2[0][3]) + " updates are incorrect, e.g. for hangar_id = '" + str(result2[0][0]) +
                         "', the floor value was expected to be '" + str(result2[0][1]) +
                         "', and now it is '" + str(result2[0][2]) + "'")

        return correct()
