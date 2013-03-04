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




