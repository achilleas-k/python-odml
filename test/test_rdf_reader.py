import datetime
import unittest

from rdflib import Literal
import odml.format as format

from odml import Property, Section, Document
from odml.tools.rdf_converter import RDFWriter, RDFReader
from odml.tools.parser_utils import ParserException

odmlns = format.Format.namespace()


class TestRDFReader(unittest.TestCase):

    def setUp(self):
        doc = Document()
        sec = Section(name="sec1", type="test", parent=doc)
        Section(name="sec2", type="test", parent=sec)
        Property(name="prop1", values=[1.3], parent=sec)

        self.doc = doc

    def test_rdf_formats(self):
        """
        Test if document gets correctly converted to odml for turtle, xml and n3.
        """
        w = RDFWriter(self.doc).get_rdf_str()
        r = RDFReader().from_string(w, "turtle")
        self.assertEqual(len(r[0].sections), 1)
        self.assertEqual(len(r[0].sections[0].sections), 1)
        self.assertEqual(len(r[0].sections[0].properties), 1)

        w = RDFWriter(self.doc).get_rdf_str("xml")
        r = RDFReader().from_string(w, "xml")
        self.assertEqual(len(r[0].sections), 1)
        self.assertEqual(len(r[0].sections[0].sections), 1)
        self.assertEqual(len(r[0].sections[0].properties), 1)

        w = RDFWriter(self.doc).get_rdf_str("n3")
        r = RDFReader().from_string(w, "n3")
        self.assertEqual(len(r[0].sections), 1)
        self.assertEqual(len(r[0].sections[0].sections), 1)
        self.assertEqual(len(r[0].sections[0].properties), 1)

    def test_doc(self):
        """
        Test if a document and its attributes get converted correctly from rdf to odml.
        """
        doc = Document()
        doc.author = "D. N. Adams"
        doc.version = 42
        doc.date = datetime.date(1979, 10, 12)

        w = RDFWriter(doc).get_rdf_str()
        r = RDFReader().from_string(w, "turtle")

        self.assertEqual(r[0].author, "D. N. Adams")
        self.assertEqual(r[0].version, "42")
        self.assertEqual(r[0].date, datetime.date(1979, 10, 12))

    def test_section(self):
        """
        Test if a section and its attributes get converted correctly from rdf to odml.
        """
        doc = Document()
        sec1 = Section(name="sec1", type="test", parent=doc, definition="Interesting stuff.",
                       reference="The Journal")
        Section(name="sec2", type="test", parent=sec1)

        w = RDFWriter(doc).get_rdf_str()
        r = RDFReader().from_string(w, "turtle")

        self.assertEqual(r[0].sections[0].name, "sec1")
        self.assertEqual(r[0].sections[0].type, "test")
        self.assertEqual(r[0].sections[0].id, sec1.id)
        self.assertEqual(r[0].sections[0].definition, "Interesting stuff.")
        self.assertEqual(r[0].sections[0].reference, "The Journal")
        self.assertEqual(r[0].sections[0].parent, r[0])
        self.assertEqual(len(r[0].sections[0].sections), 1)

    def test_property(self):
        """
        Test if a property and its attributes get converted correctly from rdf to odml.
        """
        doc = Document()
        sec1 = Section(name="sec1", type="test", parent=doc)
        prop2 = Property(name="numbers", definition="any number", dtype="float", parent=sec1,
                         values=[1, 3.4, 67.8, -12], unit="meter", uncertainty=0.8,
                         value_origin="force", reference="Experiment 1")

        w = RDFWriter(doc).get_rdf_str()
        r = RDFReader().from_string(w, "turtle")

        prop = r[0].sections[0].properties["numbers"]

        self.assertEqual(prop.name, "numbers")
        self.assertEqual(prop.dtype, "float")
        self.assertEqual(prop.id, prop2.id)
        self.assertEqual(prop.parent, r[0].sections[0])
        self.assertEqual(len(prop.values), 4)
        self.assertEqual(prop.values, [1, 3.4, 67.8, -12])
        self.assertEqual(prop.definition, "any number")
        self.assertEqual(prop.unit, "meter")
        self.assertEqual(prop.uncertainty, "0.8")
        self.assertEqual(prop.value_origin, "force")
        self.assertEqual(prop.reference, "Experiment 1")
