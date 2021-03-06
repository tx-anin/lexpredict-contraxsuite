"""
    Copyright (C) 2017, ContraxSuite, LLC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    You can also be released from the requirements of the license by purchasing
    a commercial license from ContraxSuite, LLC. Buying such a license is
    mandatory as soon as you develop commercial activities involving ContraxSuite
    software without disclosing the source code of your own applications.  These
    activities include: offering paid services to customers as an ASP or "cloud"
    provider, processing documents on the fly in a web application,
    or shipping ContraxSuite within a closed source product.
"""
import os
import tempfile
from shutil import rmtree

from apps.common.file_storage.local_file_storage import ContraxsuiteLocalFileStorage
from tests.django_test_case import DjangoTestCase

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2018, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-contraxsuite/blob/1.2.3/LICENSE"
__version__ = "1.2.3"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


class TestLocalFileStorage(DjangoTestCase):

    def test_local_file_access(self):
        temp_dir = tempfile.mkdtemp()
        try:
            sub_dir_rel = os.path.join('documents', 'sub1', 'sub2')
            os.makedirs(os.path.join(temp_dir, sub_dir_rel))

            with open(os.path.join(temp_dir, sub_dir_rel, 'file.txt'), 'w') as f:
                f.write('Hello, World!')

            with open(os.path.join(temp_dir, 'documents', 'sub1', 'file2.txt'), 'w') as f:
                f.write('Hello, World2!')

            lfa = ContraxsuiteLocalFileStorage()
            lfa.root_dir = temp_dir
            lfa.documents_path = 'documents/'

            self.assertEqual(lfa.list_documents('sub1/sub2'), ['sub1/sub2/file.txt'])
            self.assertEqual(lfa.list_documents('sub1'), ['sub1/file2.txt', 'sub1/sub2/file.txt'])

            with lfa.get_as_local_fn('documents/sub1/sub2/file.txt') as (fn, _uri):
                with open(fn, 'r') as f:
                    self.assertEqual(f.readline(), 'Hello, World!')
        finally:
            rmtree(temp_dir)
