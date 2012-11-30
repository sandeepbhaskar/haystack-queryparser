#!/usr/bin/python
# coding: latin-1

"""
Testing common search query syntax.
"""


from unittest import *
from haystack.query import SQ
from getSQ import ParseSQ

class SimpleTest(TestCase):
    def setUp(self):pass

    def test_parse(self):
        testcase = {
            "note":str(SQ(content="note")),
            '"need note"':str(SQ(content__exact="need note")),
            "author:admin":str(SQ(author="admin")),
            "author:admin notes":str(SQ(author="admin")&SQ(content="notes")),
            'title:"need note"':str(SQ(title__exact="need note")),
            # "need note 您好测试这":str(SQ(content="need")&SQ(content="note")&SQ(content=u"您")&SQ(content=u"好")&SQ(content=u"测")&SQ(content=u"试")&SQ(content=u"这")),
            "need note NOT used":str(SQ(content="need")&SQ(content="note") & ~SQ(content="used")),
            "(a AND b) OR (c AND d)":str((SQ(content="a")&SQ(content="b"))|(SQ(content="c")&SQ(content="d"))),
            "a AND b OR (c AND d)":str(SQ(content="a")&SQ(content="b")|(SQ(content="c")&SQ(content="d"))),
        }
        parser = ParseSQ()
        
        for case in testcase.keys():
            self.assertEqual(str(parser.parse(case)),testcase[case])

    def test_parse_with_new_default(self):
        testcase = {
            'helo again bye':{'sq':str(SQ(content='helo')|SQ(content='again')|SQ(content='bye')),
                              'operator':'OR'},
            'helo again AND bye':{
                'sq':str((SQ(content='helo')|SQ(content='again'))&SQ(content='bye')),
                'operator':'OR'},
            'helo again AND bye run':{
                'sq':str(((SQ(content='helo')|SQ(content='again'))&SQ(content='bye'))|SQ(content='run')),
                'operator':'OR'},

        }
        for case in testcase.keys():
            parser = ParseSQ(testcase[case]['operator'])
            self.assertEqual(str(parser.parse(case,)),testcase[case]['sq'])
    def test_operators(self):
        testcase = {
            "note":str(SQ(content="note")),
            "need -note":str(SQ(content="need")&~SQ(content="note")),
            "need +note":str(SQ(content="need")&SQ(content="note")),
            "need+note":str(SQ(content="need+note")),
        }
        parser = ParseSQ()
        
        for case in testcase.keys():
            self.assertEqual(str(parser.parse(case)),testcase[case])


def main():
    suite = TestLoader().loadTestsFromTestCase(SimpleTest)
    TextTestRunner(verbosity=2).run(suite)
