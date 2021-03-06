#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable-msg=C0111,R0904,R0903


from elohim.engine import data

import unittest2
import mock


class TestOperation(unittest2.TestCase):
    def setUp(self):
        class OperationTester(object):
            reference = None
            pointee = mock.Mock()
            subentry = mock.Mock()
            getitem = mock.Mock(return_value=subentry)

            operation = mock.Mock()
            operation.__name__ = 'operation'
            deco_operation = data.operation(strict=True)(operation)
        # pylint : disable-msg=C0103
        self.OperationTester = OperationTester

    def test_direct(self):
        decorated = self.OperationTester()
        decorated.deco_operation(list())
        self.assertTrue(decorated.operation.called)
        self.assertFalse(decorated.getitem.called)
        self.assertFalse(decorated.subentry.called)
        self.assertFalse(decorated.pointee.operation.called)

    def test_subentry(self):
        decorated = self.OperationTester()
        decorated.deco_operation(['subentry'])
        self.assertFalse(decorated.operation.called)
        decorated.getitem.assert_called_with('subentry', True)
        decorated.subentry.operation.assert_called_with(list())
        self.assertFalse(decorated.pointee.operation.called)

    def test_reference(self):
        decorated = self.OperationTester()
        decorated.reference = True
        decorated.deco_operation(list())
        self.assertFalse(decorated.operation.called)
        self.assertFalse(decorated.getitem.called)
        self.assertFalse(decorated.subentry.called)
        decorated.pointee.operation.assert_called_with(list())


class TestModifier(unittest2.TestCase):
    def setUp(self):
        #pylint : disable-msg=C0103
        class ModifierTester(object):
            content = False
            true_handler = mock.Mock()
            false_handler = mock.Mock()
            handlers = [
                    (lambda _: True, true_handler),
                    (lambda _: False, false_handler),
                    ]

            nomodification = mock.Mock()
            nomodification.__name__ = 'nomodification'
            wrapped_nomodif = data.modifier(nomodification)

            def domodification(self):
                self.content = True

            mocked_modif = mock.Mock(wraps=domodification)
            mocked_modif.__name__ = 'mocked_modif'
            wrapped_modif = data.modifier(mocked_modif)

        self.ModifierTester = ModifierTester

    def test_no_modification(self):
        decorated = self.ModifierTester()
        self.assertEquals(decorated.content, False)
        decorated.wrapped_nomodif()
        self.assertEquals(decorated.content, False)
        self.assertTrue(decorated.nomodification.called)
        self.assertFalse(decorated.true_handler.called)
        self.assertFalse(decorated.false_handler.called)

    def test_with_modifications(self):
        decorated = self.ModifierTester()
        self.assertEquals(decorated.content, False)
        decorated.wrapped_modif()
        self.assertEquals(decorated.content, True)
        self.assertTrue(decorated.mocked_modif.called)
        self.assertTrue(decorated.true_handler.called)
        self.assertFalse(decorated.false_handler.called)


class TestParsePointer(unittest2.TestCase):
    def test_simple(self):
        root = mock.Mock()
        result = data.parse_pointer('test::something')
        self.assertEquals(str(result), '<test::something>')
        result(root)
        root.getentry.assert_called_once_with(['test', 'something'])
        modifiers = result.modifiers()
        self.assertFalse(list(modifiers), list())

    def test_reference(self):
        root = mock.Mock()
        root.get = mock.Mock(return_value='outer')
        root.getentry = mock.Mock(return_value='result')
        result = data.parse_pointer('test::<test::inner>')
        self.assertEquals(str(result), '<test::<test::inner>>')
        self.assertEquals(result(root), 'result')
        root.get.assert_called_once_with(['test', 'inner'])
        root.getentry.assert_called_once_with(['test', 'outer'])
        modifiers = result.modifiers()
        self.assertIn(['test', 'inner'], modifiers)

    def test_double_reference(self):
        def entry_get(key):
            return 'two' if key == ['test', 'three'] else 'one'

        root = mock.Mock()
        root.get = mock.Mock(wraps=entry_get)
        root.getentry = mock.Mock(return_value='zero')
        result = data.parse_pointer('test::<test::<test::three>>')
        self.assertEquals(str(result), '<test::<test::<test::three>>>')
        self.assertEquals(result(root), 'zero')
        root.get.assert_any_call(['test', 'three'])
        root.get.assert_called_with(['test', 'two'])
        root.getentry.assert_called_with(['test', 'one'])
        self.assertEquals(root.get.call_count, 2)
        modifiers = result.modifiers()
        self.assertIn(['test', 'three'], modifiers)


class TestEntry(unittest2.TestCase):
    def test_get(self):
        entry = data.Entry(content=True)
        self.assertEquals(entry.get(list()), True)

    def test_getdefault(self):
        entry = data.Entry(content=True)
        key = ['subentry']
        self.assertRaises(KeyError, entry.get, key)
        result = entry.getdefault(key)
        self.assertTrue(isinstance(result, data.Entry))
        result = entry.get(key)
        self.assertTrue(isinstance(result, data.Entry))

    def test_set(self):
        entry = data.Entry(content=False)
        self.assertEquals(entry.get(list()), False)
        entry.set(list(), True)
        self.assertEquals(entry.get(list()), True)

    def test_add(self):
        entry = data.Entry(content=1)
        entry.add(list(), 1)
        self.assertEquals(entry.get(list()), 2)

    def test_initialize(self):
        entry = data.Entry()
        entry.set(['one'], False)
        entry.configure(['one'], default=True)
        self.assertEquals(entry.get(['one']), False)
        entry.initialize()
        self.assertEquals(entry.get(['one']), True)

    def test_configure(self):
        entry = data.Entry(content=False, default=True)
        self.assertEquals(entry.get(list()), False)
        self.assertEquals(entry.default, True)
        entry.reset(list())
        self.assertEquals(entry.get(list()), True)
        entry.configure(list(), default=False)
        entry.reset(list())
        self.assertEquals(entry.get(list()), False)

    def test_refer(self):
        entry = data.Entry()
        entry.set(['referee'], True)
        self.assertEquals(entry.get(['referee']), True)
        entry.refer(['reference'], 'referee')
        self.assertEquals(entry.get(['reference']), True)

    def test_refer_sub(self):
        entry = data.Entry()
        entry.set(['referee', 'value'], True)
        self.assertEquals(entry.get(['referee', 'value']), True)
        entry.refer(['reference'], 'referee')
        self.assertEquals(entry.get(['reference', 'value']), True)

    def test_refer_wrong(self):
        entry = data.Entry()
        entry.refer(['reference'], 'referee')
        self.assertEquals(entry.getentry(['reference']).pointee, None)

    def test_refer_update(self):
        entry = data.Entry()
        entry.set(['modifier'], 'one')
        entry.set(['one'], False)
        entry.set(['two'], True)
        entry.refer(['reference'], '<modifier>')
        self.assertEquals(entry.get(['reference']), False)
        entry.set(['modifier'], 'two')
        self.assertEquals(entry.get(['reference']), True)

