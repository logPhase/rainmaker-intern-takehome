"""The tests you are expected to write.

These four are the shape we look for, not the limit. Delete the skips and make them real — and
add your own: a test is only worth having if it would fail when the code is wrong.
"""

import pytest

pytestmark = pytest.mark.skip(reason="write these")


def test_a_filing_with_no_transaction_yields_nothing():
    """FIL-025 is a record date. Extraction must produce no transaction from it."""


def test_the_acquirer_and_the_target_are_not_swapped():
    """Direction is the error that survives review. Pin it on a real filing."""


def test_a_consideration_keeps_the_unit_the_document_printed():
    """FIL-001: 'Rs. 16.44 Crores' is 16.44 crore, not a bare 16.44 and not 1644."""


def test_a_missing_consideration_stays_missing():
    """No stated figure means None. Never 0, never an estimate."""
