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

        result1 = self.execute("SELECT max(case when name = 'floor' then 1 else 0 end) as f  FROM pragma_table_info('hangars')")
        is_floor = result1.fetchone()[0]
        if is_floor != 1:
            return wrong("There is no column 'floor' in the table 'hangars'")

        self.execute('update_floor')

        result2 = self.execute("SELECT "
                               "sum(case when floor <> substr(hangar_id, 1, instr(hangar_id, '-') - 1) then 1 else 0 end) as cnt "
                               "FROM hangars")
        cnt = result2.fetchone()[0]
        if cnt > 0:
            result3 = self.execute("SELECT '(e.g., for hangar_id = ''' ||''|| hangar_id ||''|| ''' the value ''' ||''|| "
                                   "substr(hangar_id, 1, instr(hangar_id, '-') - 1) ||''|| "
                                   "''' is expected, but your result is ''' ||''|| floor ||''|| ''')' as er_msg  "
                                   "FROM hangars "
                                   "WHERE floor <> substr(hangar_id, 1, instr(hangar_id, '-') - 1) "
                                   "LIMIT 1;")
            err_msg = result3.fetchone()[0]
            return wrong(str(cnt) + " updates are incorrect " + err_msg)

        return correct()
