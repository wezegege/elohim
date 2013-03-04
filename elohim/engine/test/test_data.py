#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
        root.get.assert_called_once_with(['test', 'something'])
        modifiers = result.modifiers()
        self.assertIn(['test', 'something'], modifiers)

    def test_reference(self):
        root = mock.Mock()
        root.get = mock.Mock(return_value='outer')
        result = data.parse_pointer('test::<test::inner>')
        self.assertEquals(str(result), '<test::<test::inner>>')
        self.assertEquals(result(root), 'outer')
        root.get.assert_any_call(['test', 'inner'])
        root.get.assert_called_with(['test', 'outer'])
        self.assertEquals(root.get.call_count, 2)
        modifiers = result.modifiers()
        self.assertIn(['test', 'inner'], modifiers)

    def test_double_reference(self):
        def entry_get(key):
            if key == ['test', 'three']:
                return 'two'
            elif key == ['test', 'two']:
                return 'one'
            else:
                return 'zero'

        root = mock.Mock()
        root.get = mock.Mock(wraps=entry_get)
        result = data.parse_pointer('test::<test::<test::three>>')
        self.assertEquals(str(result), '<test::<test::<test::three>>>')
        self.assertEquals(result(root), 'zero')
        root.get.assert_any_call(['test', 'three'])
        root.get.assert_any_call(['test', 'two'])
        root.get.assert_called_with(['test', 'one'])
        self.assertEquals(root.get.call_count, 3)
        modifiers = result.modifiers()
        self.assertIn(['test', 'three'], modifiers)



