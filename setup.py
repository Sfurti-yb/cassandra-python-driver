# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

from pathlib import Path
from setuptools import setup, Extension
try:
    import tomllib as toml
except ImportError:
    import tomli as toml

# ========================== General purpose vals to describe our current platform ==========================
is_windows = sys.platform.startswith('win32')
is_macos = sys.platform.startswith('darwin')
is_pypy = "PyPy" in sys.version
is_supported_platform = sys.platform != "cli" and not sys.platform.startswith("java")
is_supported_arch = sys.byteorder != "big"
is_supported = is_supported_platform and is_supported_arch

# ========================== A few upfront checks ==========================
platform_unsupported_msg = \
"""
===============================================================================
The optional C extensions are not supported on this platform.
===============================================================================
"""

arch_unsupported_msg = \
"""
===============================================================================
The optional C extensions are not supported on big-endian systems.
===============================================================================
"""

pypy_unsupported_msg = \
"""
=================================================================================
Some optional C extensions are not supported in PyPy. Only murmur3 will be built.
=================================================================================
"""

if is_pypy:
    sys.stderr.write(pypy_unsupported_msg)
if not is_supported_platform:
    sys.stderr.write(platform_unsupported_msg)
elif not is_supported_arch:
    sys.stderr.write(arch_unsupported_msg)

# ========================== Extensions ==========================
pyproject_toml = Path(__file__).parent / "pyproject.toml"
with open(pyproject_toml,"rb") as f:
    pyproject_data = toml.load(f)
driver_project_data = pyproject_data["tool"]["cassandra-driver"]

def key_or_false(k):
    return driver_project_data[k] if k in driver_project_data else False

try_murmur3 = key_or_false("build-murmur3-extension") and is_supported
try_libev = key_or_false("build-libev-extension") and is_supported
try_cython = key_or_false("build-cython-extensions") and is_supported and not is_pypy

build_concurrency = driver_project_data["build-concurrency"]

exts = []
if try_murmur3:
    murmur3_ext = Extension('cassandra.cmurmur3', sources=['cassandra/cmurmur3.c'])
    sys.stderr.write("Appending murmur extension %s\n" % murmur3_ext)
    exts.append(murmur3_ext)

if try_libev:
    libev_includes = driver_project_data["libev-includes"]
    libev_libs = driver_project_data["libev-libs"]
    if is_macos:
        libev_includes.extend(['/opt/homebrew/include', os.path.expanduser('~/homebrew/include')])
        libev_libs.extend(['/opt/homebrew/lib'])
    libev_ext = Extension('cassandra.io.libevwrapper',
                          sources=['cassandra/io/libevwrapper.c'],
                          include_dirs=libev_includes,
                          libraries=['ev'],
                          library_dirs=libev_libs)
    sys.stderr.write("Appending libev extension %s\n" % libev_ext)
    exts.append(libev_ext)

if try_cython:
    sys.stderr.write("Trying Cython builds in order to append Cython extensions\n")
    try:
        from Cython.Build import cythonize
        cython_candidates = ['cluster', 'concurrent', 'connection', 'cqltypes', 'metadata',
                             'pool', 'protocol', 'query', 'util']
        compile_args = [] if is_windows else ['-Wno-unused-function']
        exts.extend(cythonize(
            [Extension('cassandra.%s' % m, ['cassandra/%s.py' % m],
                       extra_compile_args=compile_args)
                       for m in cython_candidates],
                       nthreads=build_concurrency,
                       exclude_failures=True))

        exts.extend(cythonize(
            Extension("*", ["cassandra/*.pyx"],
                      extra_compile_args=compile_args),
                      nthreads=build_concurrency))
    except Exception as exc:
        sys.stderr.write("Failed to cythonize one or more modules. These will not be compiled as extensions (optional).\n")
        sys.stderr.write("Cython error: %s\n" % exc)

# ========================== YugaByte metadata override ==========================
# Import version from cassandra/__init__.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cassandra'))
import cassandra
__version__ = cassandra.__version__

# ========================== And finally setup() itself ==========================
setup(
    name='yb-cassandra-driver',
    version=__version__,
    description='DataStax Driver for YCQL YugabyteDB',
    url='http://github.com/yugaByte/cassandra-python-driver',
    project_urls={
        'Documentation': 'https://docs.yugabyte.com/stable/drivers-orms/python/ycql/',
        'Source': 'https://github.com/yugabyte/cassandra-python-driver/',
    },
    author='yugabyte',
    author_email='pypi@yugabyte.com',
    packages=[
        'cassandra', 'cassandra.io', 'cassandra.cqlengine', 'cassandra.graph',
        'cassandra.datastax', 'cassandra.datastax.insights', 'cassandra.datastax.graph',
        'cassandra.datastax.graph.fluent', 'cassandra.datastax.cloud',
        "cassandra.column_encryption"
    ],
    keywords='cassandra,cql,orm',
    include_package_data=True,
    install_requires=['geomet>=1.1', "Deprecated>=1.3.1"],
    extras_require={
        'graph': ['gremlinpython==3.4.6'],
        'cle': ['cryptography>=42.0']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    ext_modules=exts
)
