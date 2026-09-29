def validate_bill(data: dict):
    errors = []
    warnings = []

    # -------------------------
    # Required fields
    # -------------------------

    required_fields = [
        "bill_number",
        "bill_date",
        "total_amount",
        "payable_amount"
    ]

    for field in required_fields:
        if data.get(field) is None:
            errors.append(f"Missing field: {field}")

    # -------------------------
    # Negative amount checks
    # -------------------------

    amount_fields = [
        "total_amount",
        "gst_amount",
        "discount",
        "payable_amount",
        "received_amount"
    ]

    for field in amount_fields:
        value = data.get(field)

        if value is not None and value < 0:
            errors.append(
                f"{field} cannot be negative"
            )

    # -------------------------
    # Amount calculation check
    # -------------------------

    total = data.get("total_amount")
    gst = data.get("gst_amount")
    discount = data.get("discount")
    round_off = data.get("round_off")
    payable = data.get("payable_amount")

    if total is not None and payable is not None:

        # Convention 1:
        # Total already includes GST
        expected_inclusive = total

        if discount is not None:
            expected_inclusive -= discount

        if round_off is not None:
            expected_inclusive += round_off

        # Convention 2:
        # Total excludes GST
        expected_exclusive = total

        if gst is not None:
            expected_exclusive += gst

        if discount is not None:
            expected_exclusive -= discount

        if round_off is not None:
            expected_exclusive += round_off

        inclusive_match = (
            abs(expected_inclusive - payable) <= 0.10
        )

        exclusive_match = (
            abs(expected_exclusive - payable) <= 0.10
        )

        # IMPORTANT:
        # Only compare expected values when they
        # were actually calculated.

        if not inclusive_match and not exclusive_match:
            warnings.append(
                "Payable amount mismatch. "
                f"Expected approximately "
                f"{expected_inclusive:.2f} or "
                f"{expected_exclusive:.2f}, "
                f"but found {payable:.2f}"
            )

    # -------------------------
    # Received amount check
    # -------------------------

    received = data.get("received_amount")

    if payable is not None and received is not None:

        if received < payable:
            warnings.append(
                "Received amount is less than payable amount"
            )

        elif received > payable:
            warnings.append(
                "Received amount is greater than payable amount"
            )

    # -------------------------
    # Final validation status
    # -------------------------

    valid = len(errors) == 0

    return {
        "valid": valid,
        "errors": errors,
        "warnings": warnings
    }