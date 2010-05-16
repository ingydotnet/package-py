from package.unittest import *

class TestImport(TestCase):
    def test_import(self):
        import thingy

        self.assertTrue(True, 'thingy modules imported cleanly')

if __name__ == '__main__':
    main()
