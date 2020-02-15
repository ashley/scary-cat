from unittest import TestCase, main
from unittest.mock import patch

from main import (
    dummy_validate,
    procede
)

class TestScaryCat(TestCase):
    def validate_validators_type(self):
        result, detail = dummy_validate(None)
        self.assertEqual(bool, type(result))
        self.assertEqual(str, type(detail))

   #@patch('procede', return_value='yes')    
   #def test_yes_procede(self, input):
   #    self.assertEqual(True, procede(''))
    

if __name__ == '__main__':
    main()
