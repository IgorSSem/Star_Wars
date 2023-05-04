from hstest import SQLTest, dynamic_test
from hstest import wrong, correct


class TestSQLProject(SQLTest):
    queries = {
        'available_aircraft': None,
        'most_popular_aircraft': None,
        'largest_number_of_aircraft': None
    }

    @dynamic_test
    def test_queries(self):

        # As I understand it, creating and populating a table is not the subject of this test.

        csr1 = self.execute("SELECT name FROM sqlite_schema WHERE type = 'table' and name = 'hangars';")

        if len(csr1.fetchall()) == 0:
            self.execute(
                "CREATE TABLE 'hangars' ('hangar_id' TEXT,'type_of_aircraft' TEXT,'aircraft_in_hangar' INTEGER);")
            self.execute(
                "INSERT INTO 'hangars' ('hangar_id','type_of_aircraft','aircraft_in_hangar') VALUES "
                "('R2-C1','X-Wing','3'),"
                "('R2-C1','Jedi Starfighter','1'),"
                "('R2-C4','X-Wing','2'),"
                "('R2-C6','X-Wing','2'),"
                "('R2-C6','B-Wing','2'),"
                "('R5-D4','X-Wing','4'),"
                "('R5-D4','Jedi Starfighter','2'),"
                "('R5-D4','B-Wing','3'),"
                "('R5-D4','Slave 1','1'),"
                "('R5-D8','B-Wing','2'),"
                "('R5-D8','Slave 1','2'),"
                "('R5-D11','Slave 1','1'),"
                "('R9-G3','X-Wing','5'),"
                "('R9-G3','Jedi Starfighter','1'),"
                "('R9-G3','B-Wing','2'),"
                "('R9-G8','Slave 1','1'),"
                "('R9-G11','B-Wing','2'),"
                "('R9-G13','X-Wing','3'),"
                "('R9-G13','B-Wing','4');")

        csr2 = self.execute("SELECT count(*) AS cnt FROM hangars;")
        if csr2.fetchone()[0] == 0:
            return wrong("The table 'hangars' is empty.")

        answ1 = self.execute_and_fetch_all('available_aircraft')

        if len(answ1) == 0:
            return wrong("Your query 'available_aircraft' returned an empty dataset")

        aircraft_cnt = answ1[0][0]

        test1 = self.execute_and_fetch_all("SELECT sum(aircraft_in_hangar) as cnt_a FROM hangars;")
        cnt_e = test1[0][0]
        if cnt_e != aircraft_cnt:
            return wrong(
                "There are " + str(cnt_e) + " available  crafts are in all hangars, but your query returns "
                + str(aircraft_cnt))

        answ2 = self.execute_and_fetch_all('most_popular_aircraft')
        if len(answ2) < 1:
            return wrong("Your query 'most_popular_aircraft' returned an empty dataset")

        test2 = self.execute_and_fetch_all(";WITH x1 AS ("
                                           "SELECT type_of_aircraft, sum(aircraft_in_hangar) AS amount "
                                           "FROM hangars "
                                           "GROUP BY type_of_aircraft "
                                           "), x2 AS ("
                                           "SELECT type_of_aircraft, amount, max(amount) over () AS max_a "
                                           "FROM x1) "
                                           "SELECT type_of_aircraft FROM x2 WHERE amount = max_a;")

        if len(answ2) != len(test2):
            return wrong("Your query returns the " + str(len(answ2)) + " most popular aircraft"
                         ", expected: " + str(len(test2)))
        i = 0
        while i < len(test2):
            j = 0
            inlist = 0
            while j < len(answ2):
                if test2[i][0] in answ2[j]:
                    inlist = 1
                j = j + 1
            if inlist == 0:
                return wrong("Aircraft '" + str(test2[i][0]) + "' is not in your list of the most popular crafts")
            i = i + 1

        answ3 = self.execute_and_fetch_all('largest_number_of_aircraft')
        if len(answ3) < 1:
            return wrong("Your query 'largest_number_of_aircraft' returned an empty dataset")

        test3 = self.execute_and_fetch_all("SELECT hangar_id "
                                           "FROM "
                                           "(SELECT hangar_id, Amount, max(Amount) over () AS max_a "
                                           "FROM "
                                           "(SELECT hangar_id, SUM(aircraft_in_hangar) AS Amount "
                                           "FROM hangars "
                                           "GROUP BY hangar_id) q1"
                                           ") q2 "
                                           "WHERE Amount = max_a;")

        if len(answ3) != len(test3):
            return wrong("Your query returns the " + str(len(answ3)) + " hangars with the most aircraft"
                         ", expected: " + str(len(test3)))
        i = 0
        while i < len(test3):
            j = 0
            inlist = 0
            while j < len(answ3):
                if test3[i][0] in answ3[j]:
                    inlist = 1
                j = j + 1
            if inlist == 0:
                return wrong(
                    "Aircraft \'{0}\' is not in your list of hangars with the most aircraft".format(str(test3[i][0])))
            i = i + 1

        return correct()
