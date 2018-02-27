import os
import unittest
import yaml

from odml.tools import dict_parser
from odml.tools.parser_utils import ParserException


class TestYAMLParser(unittest.TestCase):

    def setUp(self):
        self.basepath = 'test/resources/'

        self.yaml_reader = dict_parser.DictReader()

    def test_missing_root(self):
        filename = "missing_root.yaml"
        message = "Missing root element"

        with open(os.path.join(self.basepath, filename)) as raw_data:
            parsed_doc = yaml.load(raw_data)

        with self.assertRaises(ParserException) as exc:
            _ = self.yaml_reader.to_odml(parsed_doc)

        self.assertIn(message, str(exc.exception))

    def test_missing_version(self):
        filename = "missing_version.yaml"
        message = "Could not find odml-version"

        with open(os.path.join(self.basepath, filename)) as raw_data:
            parsed_doc = yaml.load(raw_data)

        with self.assertRaises(ParserException) as exc:
            _ = self.yaml_reader.to_odml(parsed_doc)

        self.assertIn(message, str(exc.exception))

    def test_invalid_version(self):
        filename = "invalid_version.yaml"
        message = "invalid odML document format version"

        with open(os.path.join(self.basepath, filename)) as raw_data:
            parsed_doc = yaml.load(raw_data)

        with self.assertRaises(ParserException) as exc:
            _ = self.yaml_reader.to_odml(parsed_doc)

        self.assertIn(message, str(exc.exception))
