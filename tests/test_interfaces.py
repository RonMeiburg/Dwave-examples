#    Copyright 2018 D-Wave Systems Inc.

#    Licensed under the Apache License, Version 2.0 (the "License")
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http: // www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import unittest
from random import randint

from factoring.interfaces import factor


class TestInterfaces(unittest.TestCase):

    def test_factor_output(self):
        P = randint(0, 2**6-1)
        output = factor(P)

        self.assertSetEqual(set(output), {'results', 'timing', 'numberOfReads'})
        for result in output['results']:
            self.assertSetEqual(set(result), {'a', 'b', 'valid', 'numOfOccurrences', 'percentageOfOccurrences'})
            self.assertIsInstance(result['a'], int)
            self.assertIsInstance(result['b'], int)
            self.assertIsInstance(result['valid'], bool)
            self.assertIsInstance(result['numOfOccurrences'], int)
            self.assertIsInstance(result['percentageOfOccurrences'], float)
        self.assertIsInstance(output['numberOfReads'], int)
        self.assertSetEqual(set(output['timing']), {'actual'})
        self.assertSetEqual(set(output['timing']['actual']), {'qpuProcessTime'})
        self.assertIsInstance(output['timing']['actual']['qpuProcessTime'], int)

    def test_factor_invalid(self):
        for P in [-1, 64, 'a']:
            self.assertRaises(ValueError, factor, P)

    @unittest.skip("not robust enough yet")
    def test_factor_validity(self):
        for P in {a*b for a in range(2**3) for b in range(2**3)}:
            output = factor(P)

            self.assertTrue(output['results'][0]['valid'])
