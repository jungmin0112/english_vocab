import copy
import json
from pathlib import Path
import tempfile
import unittest

from quiz import is_correct, load_words, run_quiz, validate_words


class QuizTests(unittest.TestCase):
    def setUp(self):
        self.words = load_words(Path(__file__).parent / "fixtures" / "words.json")

    def play(self, answers, selected=None):
        answers = iter(answers)
        output = []
        result = run_quiz(self.words, selected if selected is not None else list(self.words),
                          read=lambda prompt: next(answers), write=output.append)
        return result, "\n".join(output)

    def test_grading(self):
        for answer in ["돌아 가다", " 돌아\t가다 ", "반환하다"]:
            self.assertTrue(is_correct(answer, self.words["return"]["meanings"]))
        for answer in ["", "  ", "되돌아오다"]:
            self.assertFalse(is_correct(answer, self.words["return"]["meanings"]))

    def test_results_defaults_and_original_data(self):
        original = copy.deepcopy(self.words)
        result, output = self.play(["사과", "오답", "돌아 가다", ""])
        self.assertEqual([r["rating"] for r in result], ["Good", "Again", "Good"])
        self.assertEqual(result[2]["answer"], "돌아 가다")
        self.assertIn("전체 3문제 | 정답 2 | 오답 1", output)
        self.assertIn("달리다, 운영하다", output)
        self.assertEqual(self.words, original)

    def test_rating_edits_and_invalid_input(self):
        result, output = self.play(["사과", "", "반환하다", "x", "0", "99", "2", "1", "bad",
                                    "1", "1", "3", "3", ""])
        self.assertEqual([r["rating"] for r in result], ["Hard", "Again", "Easy"])
        self.assertIn("오답은 Again", output)

    def test_restore_good(self):
        result, _ = self.play(["사과", "1", "3", "1", "2", ""], ["apple"])
        self.assertEqual(result[0]["rating"], "Good")

    def test_limit_and_duplicates(self):
        self.words = {f"word{i}": {"meanings": ["뜻"]} for i in range(20)}
        selected = ["word0", "word0"] + list(self.words)[1:]
        result, _ = self.play(["뜻"] * 15 + [""], selected)
        self.assertEqual(len(result), 15)
        self.assertEqual([r["english"] for r in result], list(self.words)[:15])

    def test_empty_cases(self):
        result, output = self.play([], [])
        self.assertEqual(result, [])
        self.assertIn("출제 가능한", output)
        self.words = {}
        result, output = self.play([])
        self.assertIn("먼저 단어를 등록", output)

    def test_cancellation_at_each_stage(self):
        for exception in [EOFError, KeyboardInterrupt]:
            for prefix in [[], ["사과"], ["사과", "1"]]:
                with self.subTest(exception=exception, prefix=prefix):
                    answers = iter(prefix)
                    def read(prompt):
                        try:
                            return next(answers)
                        except StopIteration:
                            raise exception
                    original = copy.deepcopy(self.words)
                    self.assertIsNone(run_quiz(self.words, ["apple"], read, lambda text: None))
                    self.assertEqual(self.words, original)

    def test_invalid_schema(self):
        for value in [[], {"Apple": {"meanings": ["사과"]}}, {"apple": "사과"},
                      {"apple": {"meanings": []}}, {"apple": {"meanings": [" "]}},
                      {"apple": {"meanings": [1]}}]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_words(value)

    def test_bad_files(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "words.json"
            with self.assertRaises(FileNotFoundError):
                load_words(path)
            for text in ['{', '{"apple": {}, "apple": {}}']:
                path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_words(path)

    def test_unknown_selection(self):
        with self.assertRaises(ValueError):
            self.play([], ["missing"])


if __name__ == "__main__":
    unittest.main()
