import unittest
import os
from F1_base import Document, Collection, SearchTools


class Test(unittest.TestCase):
    def setUp(self):
        self.base = Collection()
        self.searcher = SearchTools(self.base)
        self.doc1 = '{"id": 1, "name": "Max Verstappen", "team": "Red Bull", "age": 28, "past_teams": ["Toro Rosso"], "stats": {"wins": 71, "championships": 4}}'
        self.doc2 = '{"id": 2, "name": "Lando Norris", "team": "McLaren", "age": 26, "past_teams": ["Carlin"], "stats": {"wins": 11, "championships": 1}}'
        self.doc3 = '{"id": 3, "name": "Oscar Piastri", "team": "McLaren", "age": 25, "stats": {"wins": 9}}'
        self.base.add(self.doc1)
        self.base.add(self.doc2)
        self.base.add(self.doc3)
        self.test_filename = "test_F1_base.json"

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_doc_creat(self):
        doc = Document({"id": 99, "name": "Test"})
        self.assertEqual(doc.get_id(), 99)

    def test_upd(self):
        self.base.upd(2, "stats.wins", 12)
        doc = next(d for d in self.base.documents if d.get_id() == 2)
        self.assertEqual(doc.data["stats"]["wins"], 12)

    def test_del(self):
        result = self.base.delete(1)
        self.assertTrue(result)
        self.assertEqual(len(self.base.documents), 2)

    def test_find_s1mple(self):
        res = self.searcher.find([("team", "=", "McLaren")])
        self.assertEqual(len(res), 2)

    def test_find_in(self):
        res = self.searcher.find([("past_teams", "in", "Toro Rosso")])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].get_id(), 1)

    def test_agg_sum(self):
        total_wins = self.searcher.aggregate("sum", "stats.wins")
        self.assertEqual(total_wins, 91)

    def test_agg_avg(self):
        avg_age = self.searcher.aggregate("avg", "age")
        self.assertAlmostEqual(avg_age, 79 / 3, places=4)

    def test_group(self):
        groups = self.searcher.group("team")
        self.assertEqual(groups["McLaren"], 2)
        self.assertEqual(groups["Red Bull"], 1)

    def test_save_load(self):
        self.base.save(self.test_filename)
        self.assertTrue(os.path.exists(self.test_filename))
        new_db = Collection()
        new_db.load(self.test_filename)
        self.assertEqual(len(new_db.documents), 3)
        self.assertEqual(new_db.documents[0].get_id(), 1)


if __name__ == "__main__":
    unittest.main()