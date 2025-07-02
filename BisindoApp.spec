# -*- mode: python ; coding: utf-8 -*-
import os
import importlib.util

# Get the path to the mediapipe package to find its model files
spec = importlib.util.find_spec('mediapipe')
mediapipe_path = os.path.dirname(spec.origin)

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('label_dict.json', '.'),
        ('model.p', '.'),
        ('requirements.txt', '.'),
        # This line is crucial: it copies the mediapipe model files
        (os.path.join(mediapipe_path, 'modules'), 'mediapipe/modules')
    ],
    hiddenimports=[
        'mediapipe.solutions.hands',
        'mediapipe.solutions.drawing_utils',
        # Comprehensive hidden imports for scikit-learn and its dependencies
        'sklearn.utils._cython_blas',
        'sklearn.neighbors._typedefs',
        'sklearn.neighbors._quad_tree',
        'sklearn.tree',
        'sklearn.tree._utils',
        'sklearn.ensemble._forest',
        'sklearn.svm._libsvm',
        'numpy.core._methods',
        'numpy.lib.format',
        'scipy.sparse.csgraph._validation',
        'scipy._lib.messagestream'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='BisindoApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
