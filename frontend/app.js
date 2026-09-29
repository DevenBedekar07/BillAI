const invoiceInput = document.getElementById("invoiceInput");
const chooseButton = document.getElementById("chooseButton");
const analyzeButton = document.getElementById("analyzeButton");

const uploadCard = document.getElementById("uploadCard");
const selectedFile = document.getElementById("selectedFile");

const loadingSection = document.getElementById("loadingSection");
const resultsSection = document.getElementById("analysis");

const newAnalysisButton =
    document.getElementById("newAnalysisButton");

let selectedInvoice = null;


/* =========================
   FILE SELECTION
========================= */

chooseButton.addEventListener("click", () => {
    invoiceInput.click();
});


invoiceInput.addEventListener("change", (event) => {

    const file = event.target.files[0];

    if (!file) {
        return;
    }

    handleFile(file);
});


function handleFile(file) {

    const allowedTypes = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ];

    const maxSize = 10 * 1024 * 1024;

    if (!allowedTypes.includes(file.type)) {

        alert(
            "Unsupported file type. Please upload JPG, PNG or WEBP."
        );

        return;
    }

    if (file.size > maxSize) {

        alert(
            "File is too large. Maximum allowed size is 10 MB."
        );

        return;
    }

    selectedInvoice = file;

    selectedFile.textContent =
        `${file.name} · ${formatFileSize(file.size)}`;

    selectedFile.hidden = false;

    analyzeButton.hidden = false;
}


/* =========================
   DRAG & DROP
========================= */

uploadCard.addEventListener("dragover", (event) => {

    event.preventDefault();

    uploadCard.classList.add("dragging");
});


uploadCard.addEventListener("dragleave", () => {

    uploadCard.classList.remove("dragging");
});


uploadCard.addEventListener("drop", (event) => {

    event.preventDefault();

    uploadCard.classList.remove("dragging");

    const file = event.dataTransfer.files[0];

    if (!file) {
        return;
    }

    handleFile(file);
});


/* =========================
   ANALYZE BILL
========================= */

analyzeButton.addEventListener("click", async () => {

    if (!selectedInvoice) {
        return;
    }

    setLoadingState(true);

    const formData = new FormData();

    formData.append(
        "file",
        selectedInvoice
    );

    try {

        const response = await fetch(
            "/analyze",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Bill analysis failed."
            );
        }

        displayResults(data);

    } catch (error) {

        console.error(error);

        alert(
            error.message ||
            "Something went wrong while analyzing the bill."
        );

    } finally {

        setLoadingState(false);
    }
});


/* =========================
   DISPLAY RESULTS
========================= */

function displayResults(data) {

    const bill = data.bill_data;
    const validation = data.validation;
    const anomaly = data.anomaly;

    document.getElementById("vendorName").textContent =
        bill.vendor_name || "Not detected";

    document.getElementById("billNumber").textContent =
        bill.bill_number || "Not detected";

    document.getElementById("billDate").textContent =
        bill.bill_date || "Not detected";

    document.getElementById("payableAmount").textContent =
        formatCurrency(bill.payable_amount);

    document.getElementById("totalAmount").textContent =
        formatCurrency(bill.total_amount);

    document.getElementById("gstAmount").textContent =
        formatCurrency(bill.gst_amount);

    document.getElementById("discountAmount").textContent =
        formatCurrency(bill.discount);

    document.getElementById("roundOff").textContent =
        formatCurrency(bill.round_off);

    document.getElementById("financialPayable").textContent =
        formatCurrency(bill.payable_amount);


    /* Validation */

    const validationBadge =
        document.getElementById("validationBadge");

    validationBadge.textContent =
        validation.valid ? "Valid" : "Issues Found";

    validationBadge.className =
        `result-badge ${
            validation.valid
                ? "valid"
                : "invalid"
        }`;


    const validationMessage =
        document.getElementById("validationMessage");

    const issuesList =
        document.getElementById("validationIssues");

    issuesList.innerHTML = "";


    if (validation.valid) {

        validationMessage.textContent =
            "The invoice passed the required validation checks.";

    } else {

        validationMessage.textContent =
            "The invoice contains validation issues.";
    }


    const issues = [
        ...(validation.errors || []),
        ...(validation.warnings || [])
    ];


    issues.forEach((issue) => {

        const div = document.createElement("div");

        div.className = "issue";

        div.textContent = `• ${issue}`;

        issuesList.appendChild(div);
    });


    /* Anomaly */

    const anomalyStatus =
        document.getElementById("anomalyStatus");

    anomalyStatus.textContent =
        capitalize(anomaly.status);


    const anomalyScore =
        document.getElementById("anomalyScore");

    anomalyScore.textContent =
        anomaly.anomaly_score ?? "—";


    /* Show results */

    resultsSection.hidden = false;

    resultsSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


/* =========================
   LOADING STATE
========================= */

function setLoadingState(isLoading) {

    if (isLoading) {

        loadingSection.hidden = false;

        resultsSection.hidden = true;

        analyzeButton.disabled = true;

        analyzeButton.textContent =
            "Analyzing...";

    } else {

        loadingSection.hidden = true;

        analyzeButton.disabled = false;

        analyzeButton.textContent =
            "Analyze Bill →";
    }
}


/* =========================
   NEW ANALYSIS
========================= */

newAnalysisButton.addEventListener("click", () => {

    selectedInvoice = null;

    invoiceInput.value = "";

    selectedFile.textContent = "";

    selectedFile.hidden = true;

    analyzeButton.hidden = true;

    resultsSection.hidden = true;

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
});


/* =========================
   HELPERS
========================= */

function formatCurrency(value) {

    if (
        value === null ||
        value === undefined ||
        Number.isNaN(Number(value))
    ) {
        return "—";
    }

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 2
        }
    ).format(value);
}


function formatFileSize(bytes) {

    if (bytes < 1024 * 1024) {

        return `${(bytes / 1024).toFixed(1)} KB`;

    }

    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}


function capitalize(value) {

    if (!value) {
        return "—";
    }

    return value.charAt(0).toUpperCase()
        + value.slice(1);
}