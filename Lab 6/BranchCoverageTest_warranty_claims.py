import pytest

from warranty_claims import claim_allowed, out_of_warranty_charge, sla_status


def test_charge_rejects_unknown_plan_and_negative_age():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("gold", 1, "defect", False)

    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_charge_handles_warranty_and_registration_branches():
    assert out_of_warranty_charge("basic", 12, "defect", False) == 0
    assert out_of_warranty_charge("basic", 18, "defect", True) == 0
    assert out_of_warranty_charge("premium", 36, "defect", True) == 0


def test_charge_handles_accidental_and_non_accidental_rates():
    assert out_of_warranty_charge("basic", 13, "accidental", False) == 200
    assert out_of_warranty_charge("basic", 13, "defect", False) == 100


def test_charge_handles_long_excess_for_both_claim_types():
    assert out_of_warranty_charge("basic", 25, "accidental", False) == 3575
    assert out_of_warranty_charge("basic", 25, "defect", False) == 1950


@pytest.mark.parametrize(
    ("days_since_last_claim", "claims_filed", "is_recall", "expected"),
    [
        (0, 5, True, True),
        (0, 6, True, False),
        (29, 0, False, False),
        (30, 2, False, True),
        (30, 3, False, False),
    ],
)
def test_claim_allowed_covers_recall_waiting_period_and_claim_limit_branches(
    days_since_last_claim, claims_filed, is_recall, expected
):
    assert claim_allowed(days_since_last_claim, claims_filed, is_recall) is expected


@pytest.mark.parametrize(
    ("hours_left", "is_hardware", "is_priority", "expected"),
    [
        (48, True, False, "on_track"),
        (48, False, True, "on_track"),
        (36, False, True, "at_risk"),
        (23, False, False, "at_risk"),
        (11, False, False, "critical"),
    ],
)
def test_sla_status_covers_cutoffs_priority_and_every_status(
    hours_left, is_hardware, is_priority, expected
):
    assert sla_status(hours_left, is_hardware, is_priority) == expected
