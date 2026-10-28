"""Template registry — order here is the library order."""

import importlib

_MODULES = [
    "a_intake",
    "b_questionnaires",
    "c_primary_care",
    "d_medical_surgical",
    "e_procedure_consents",
    "f_rx_letters",
    "g_optical_handouts",
]

ALL_DOCS = []
for _m in _MODULES:
    try:
        mod = importlib.import_module(f"templates.{_m}")
    except ModuleNotFoundError as e:
        if e.name == f"templates.{_m}":
            continue
        raise
    ALL_DOCS.extend(mod.DOCS)

ALL_DOCS.sort(key=lambda d: d.code)
