#!/usr/bin/env python

from runtest import TestBase
import platform

class TestCase(TestBase):
    def __init__(self):
        TestBase.__init__(self, 'dynamic', """
# DURATION     TID     FUNCTION
         [ 63876] | main() {
0.739 us [ 63876] |   foo();
1.903 us [ 63876] | } /* main */
""")

    def pre(self):
        if platform.machine().startswith('arm'):
            return TestBase.TEST_SKIP
        return TestBase.TEST_SUCCESS

    def build(self, name, cflags='', ldflags=''):
        cflags = cflags.replace('-pg', '')
        cflags = cflags.replace('-finstrument-functions', '')
        cflags += ' -fno-pie -fno-plt'  # workaround of build failure
        return TestBase.build(self, name, cflags, ldflags)

    def runcmd(self):
        uftrace = TestBase.uftrace_cmd
        options = '-P . -U bar --no-libcall'
        program = 't-' + self.name
        return '%s %s %s' % (uftrace, options, program)
