from hstest import SQLTest, dynamic_test
from hstest import wrong, correct


class TestSQLProject(SQLTest):
    queries = {
        'create_table': None,
        'insert_data': None,
        'available_aircraft': None,
        'most_popular_aircraft': None,
        'largest_number_of_aircraft': None
    }

    @dynamic_test
    def test_queries(self):

        self.execute('create_table')

        result1 = self.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;")

        if 'hangars' not in result1.fetchall()[0]:
            return wrong("Can't find 'hangars' table in the database")

        self.execute('insert_data')

        result2 = self.execute("SELECT Count(*) AS cnt FROM hangars")
        cnt = result2.fetchone()[0]
        if cnt != 19:
            return wrong("There should be 19 records, but your query returns " + str(cnt))

        result3 = self.execute('available_aircraft')
        aircraft_cnt = result3.fetchone()[0]
        if 43 != aircraft_cnt:
            return wrong(
                "There are 43 available  crafts are in all hangars, but your query returns " + str(aircraft_cnt))

        result4 = self.execute('most_popular_aircraft')
        popular_a = result4.fetchone()[0]
        if 'X-Wing' not in popular_a:
            return wrong("The most popular aircraft is 'X-Wing', but your query returns '" + popular_a + "'")

        result5 = self.execute('largest_number_of_aircraft')
        large_h = result5.fetchone()[0]
        if 'R5-D4' not in large_h:
            return wrong(
                "The largest number of aircraft is in the hangar 'R5-D4', but your query returns '"
                + large_h + "'")

        return correct()

