import re

def normalize_ocr_text(text: str) -> str:
    """
    Normalize common OCR formatting problems while
    preserving line structure.
    """

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Collapse repeated spaces
        line = re.sub(r"\s+", " ", line)

        lines.append(line)

    return "\n".join(lines)


def parse_amount(value: str):

    if not value:
        return None

    value = value.strip()

    value = value.replace(
        "₹", ""
    ).replace(
        "Rs.", ""
    ).replace(
        "Rs", ""
    ).replace(
        "€", ""
    ).replace(
        "$", ""
    ).replace(
        "£", ""
    ).replace(
        "¥", ""
    ).strip()

    if "," in value and "." in value:
        value = value.replace(",", "")

    elif "," in value:

        parts = value.split(",")

        if len(parts[-1]) == 2:
            value = ".".join(parts)

        else:
            value = "".join(parts)

    try:
        return float(value)

    except ValueError:
        return None

def extract_gst_number(text: str):

    pattern = (
        r"\b\d{2}[A-Z]{5}\d{4}[A-Z]"
        r"[A-Z0-9]Z[A-Z0-9]\b"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE
    )

    return match.group(0).upper() if match else None


def extract_vendor_name(text: str):

    # Prefer the supplier/company name explicitly.
    patterns = [
        r"SUPPLIER\s*/?\s*FROM\s*\n\s*([^\n]+)",

        r"([A-Z][A-Z\s&.-]+(?:PVT\s+LTD|PRIVATE\s+LIMITED|LTD|LLP))",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            vendor = match.group(1).strip()

            # Avoid OCR fragments.
            if len(vendor) > 5:
                return vendor

    # Fallback
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:20]:

        upper = line.upper()

        if (
            "PVT LTD" in upper
            or "PRIVATE LIMITED" in upper
            or "LIMITED" in upper
            or "LLP" in upper
        ):
            return line

    return lines[0] if lines else None


def extract_bill_number(text: str):

    patterns = [

        # Invoice No: INV-2026-1042
        r"\bInvoice\s*(?:No\.?|Number|#)\s*[:\-]?\s*"
        r"([A-Z0-9][A-Z0-9\-\/]*)",

        # Inv. No: INV-2026-1042
        r"\bInv\.?\s*(?:No\.?|Number|#)\s*[:\-]?\s*"
        r"([A-Z0-9][A-Z0-9\-\/]*)",

        # Bill No: B-1024
        r"\bBill\s*(?:No\.?|Number|#)\s*[:\-]?\s*"
        r"([A-Z0-9][A-Z0-9\-\/]*)",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return None


def extract_bill_number(text: str):

    patterns = [
        # Bill Number : 18111
        r"\bBill\s+Number\s*[:\-]?\s*([A-Z0-9\-\/]+)",

        # Bill No : 18111
        r"\bBill\s+No\.?\s*[:\-]?\s*([A-Z0-9\-\/]+)",

        # Invoice No : INV-2026-1042
        r"\bInvoice\s+No\.?\s*[:\-]?\s*"
        r"([A-Z0-9]+-[A-Z0-9\-\/]+)",

        # Invoice Number : INV-2026-1042
        r"\bInvoice\s+Number\s*[:\-]?\s*"
        r"([A-Z0-9]+-[A-Z0-9\-\/]+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return None


def extract_labeled_amount(text: str, labels):

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        for label in labels:

            pattern = (
                rf"{label}"
                r"\s*[:=\-|]*"
                r"\s*[^0-9\n]*"
                r"([\d,]+(?:\.\d{1,2})?)"
            )

            match = re.search(
                pattern,
                line,
                re.IGNORECASE
            )

            if match:
                return parse_amount(
                    match.group(1)
                )

    return None

def extract_total_amount(text: str):

    return extract_labeled_amount(
        text,
        [
            r"Total\s+Bill\s+Amount",
            r"Total\s+Amount",
            r"Grand\s+Total",
        ]
    )


def extract_subtotal(text: str):

    return extract_labeled_amount(
        text,
        [
            r"Sub\s*Total",
            r"Subtotal"
        ]
    )


def extract_gst_amount(text: str):

    cgst = extract_labeled_amount(
        text,
        [
            r"\bCGST"
        ]
    )

    sgst = extract_labeled_amount(
        text,
        [
            r"\bSGST"
        ]
    )

    if cgst is not None or sgst is not None:

        return round(
            (cgst or 0) + (sgst or 0),
            2
        )

    # Only match standalone GST.
    # This prevents GST from matching inside CGST/SGST.
    gst = extract_labeled_amount(
        text,
        [
            r"(?<![A-Za-z])GST(?!\s*(?:No|Number))"
        ]
    )

    return gst

def extract_discount(text: str):

    patterns = [
        # Discount (5%): 32.05
        r"\bDiscount\s*"
        r"(?:\(\s*\d+(?:\.\d+)?%\s*\))?"
        r"\s*[:=\-|]?\s*"
        r"[^0-9\n]*"
        r"([\d,]+(?:\.\d{1,2})?)",

        # Discount : 32.05
        r"\bDiscount\s*"
        r"[:=\-|]\s*"
        r"[^0-9\n]*"
        r"([\d,]+(?:\.\d{1,2})?)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return parse_amount(match.group(1))

    return None
def extract_round_off(text: str):

    return extract_labeled_amount(
        text,
        [
            r"Round\s*Off",
            r"Roundoff"
        ]
    )


def extract_payable_amount(text: str):

    amount = extract_labeled_amount(
        text,
        [
            r"Payable\s+Amount",
            r"Amount\s+Payable",
            r"Grand\s+Total"
        ]
    )

    if amount is not None:
        return amount

    # OCR sometimes damages "Payable Amount".
    amount = extract_labeled_amount(
        text,
        [
            r"Payable\s+Amou",
            r"Payable"
        ]
    )

    return amount


def extract_received_amount(text: str):

    return extract_labeled_amount(
        text,
        [
            r"Received\s+Amount",
            r"Amount\s+Received"
        ]
    )


def extract_payment_mode(text: str):

    patterns = [

        r"Payment\s+Mode"
        r"\s*[:=\-|]+\s*([A-Za-z]+)",

        r"Payment\s+Method"
        r"\s*[:=\-|]+\s*([A-Za-z]+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return None

def extract_item_count(text: str):

    lines = text.splitlines()

    count = 0

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        # Stop counting once we reach totals/payment section.
        upper = stripped.upper()

        if any(
            keyword in upper
            for keyword in [
                "TOTAL BILL",
                "TOTAL AMOUNT",
                "SUB TOTAL",
                "SUBTOTAL",
                "DISCOUNT",
                "GST:",
                "ROUND OFF",
                "PAYABLE",
                "RECEIVED AMOUNT",
                "PAYMENT MODE"
            ]
        ):
            continue

        # Format such as:
        #
        # 1 LOGIHAIR MEN TAB-30S ... 641.00 1 641.00
        #
        # or:
        #
        # 2 1,250.00 2,500.00

        if re.match(r"^\d+\s+\S+", stripped):

            # Don't count obvious non-item lines.
            if any(
                keyword in upper
                for keyword in [
                    "GST NO",
                    "BILL NUMBER",
                    "BILL DATE",
                    "INVOICE",
                    "PAYMENT",
                    "PHONE",
                    "EMAIL"
                ]
            ):
                continue

            count += 1

    return count
def extract_bill_fields(text: str):

    text = normalize_ocr_text(text)

    total_amount = extract_total_amount(text)

    gst_amount = extract_gst_amount(text)

    discount = extract_discount(text)

    round_off = extract_round_off(text)

    received_amount = extract_received_amount(text)

    payable_amount = extract_payable_amount(text)

    # OCR sometimes truncates "Payable Amount".
    # If the received amount matches the total,
    # we can reasonably use it as the payable amount.
    if payable_amount is None:

        if (
            received_amount is not None
            and total_amount is not None
            and abs(received_amount - total_amount) <= 0.01
        ):
            payable_amount = received_amount

    return {

        "vendor_name":
            extract_vendor_name(text),

        "gst_number":
            extract_gst_number(text),

        "bill_number":
            extract_bill_number(text),

        "bill_date":
            extract_bill_date(text),

        "total_amount":
            total_amount,

        "gst_amount":
            gst_amount,

        "discount":
            discount,

        "round_off":
            round_off,

        "payable_amount":
            payable_amount,

        "received_amount":
            received_amount,

        "payment_mode":
            extract_payment_mode(text),

        "item_count":
            extract_item_count(text),
    }
    
def extract_bill_date(text: str):

    patterns = [

        # Example:
        # Invoice Date: 25-Sep-2026
        r"(?:Invoice|Inv\.?|Bill)\s*Date"
        r"\s*[:\-|]?\s*"
        r"(\d{1,2}[-/][A-Za-z]{3}[-/]\d{4})",

        # Example:
        # Invoice Date: 25/09/2026
        r"(?:Invoice|Inv\.?|Bill)\s*Date"
        r"\s*[:\-|]?\s*"
        r"(\d{1,2}[-/]\d{1,2}[-/]\d{4})",

        # Fallback: find date anywhere in OCR text
        r"\b(\d{1,2}[-/][A-Za-z]{3}[-/]\d{4})\b",

        r"\b(\d{1,2}[-/]\d{1,2}[-/]\d{4})\b",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return None