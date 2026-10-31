import pytest

from warranty_claims import claim_allowed, out_of_warranty_charge, sla_status


def test_out_of_warranty_charge_rejects_invalid_inputs():
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("gold", 12, "defect", False)

    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_out_of_warranty_charge_registered_item_within_extended_warranty():
    assert out_of_warranty_charge("basic", 18, "defect", True) == 0


def test_out_of_warranty_charge_uses_accidental_and_standard_rates():
    assert out_of_warranty_charge("premium", 37, "accidental", False) == 200
    assert out_of_warranty_charge("standard", 30, "defect", False) == 600


def test_out_of_warranty_charge_applies_long_excess_accidental_surcharge():
    assert out_of_warranty_charge("basic", 30, "accidental", False) == 4950


def test_claim_allowed_for_recall_recent_and_normal_claims():
    assert claim_allowed(0, 5, True) is True
    assert claim_allowed(0, 6, True) is False
    assert claim_allowed(29, 0, False) is False
    assert claim_allowed(30, 2, False) is True


def test_sla_status_covers_hardware_software_priority_and_all_statuses():
    assert sla_status(48, True, False) == "on_track"
    assert sla_status(36, False, True) == "at_risk"
    assert sla_status(10, False, False) == "critical"
