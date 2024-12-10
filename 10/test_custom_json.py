import unittest
import json
import custom_json


class TestCustomJson(unittest.TestCase):
    def test_loads_valid(self):
        json_str = '{"hello": 10, "world": "value"}'
        expected = json.loads(json_str)
        result = custom_json.loads(json_str)
        self.assertEqual(result, expected)

    def test_dumps_valid(self):
        obj = {"hello": 10, "world": "value"}
        expected = json.dumps(obj, separators=(', ', ': '))
        result = custom_json.dumps(obj)
        self.assertEqual(result, expected)

    def test_round_trip(self):
        json_str = '{"hello": 10, "world": "value"}'
        obj = custom_json.loads(json_str)
        serialized = custom_json.dumps(obj)
        self.assertEqual(json_str, serialized)

    def test_invalid_loads(self):
        invalid_jsons = [
            '',
            'hello',
            '{"key": value}',
            '{"key": 123,}',
            '{"key": [1, 2,]',
        ]
        for invalid_json in invalid_jsons:
            with self.assertRaises(Exception):
                custom_json.loads(invalid_json)

    def test_compare_with_json(self):
        test_cases = [
            '{"key": 123, "name": "Alice"}',
            '{"empty_dict": {}, "empty_list": []}',
            '{"number": 3.14, "boolean": true}',
        ]
        for case in test_cases:
            with self.subTest(case=case):
                parsed_custom = custom_json.loads(case)
                parsed_standard = json.loads(case)
                self.assertEqual(parsed_custom, parsed_standard)

                serialized_custom = custom_json.dumps(parsed_custom)
                serialized_standard = json.dumps(
                    parsed_standard, separators=(', ', ': '))
                self.assertEqual(serialized_custom, serialized_standard)


if __name__ == '__main__':
    unittest.main()
