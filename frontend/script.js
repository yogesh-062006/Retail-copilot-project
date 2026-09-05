async function loadDashboard() {
    try {
        const response = await fetch("/api/dashboard");
        const data = await response.json();

        document.getElementById("revenue").textContent =
            "₹" + data.total_revenue.toLocaleString("en-IN");

        document.getElementById("units").textContent =
            data.total_units_sold.toLocaleString("en-IN");

        document.getElementById("best-product").textContent =
            data.best_product;


        // LOW STOCK
        const lowStockContainer =
            document.getElementById("low-stock");

        if (data.low_stock.length === 0) {
            lowStockContainer.innerHTML =
                "<p>No low-stock products.</p>";
        } else {
            lowStockContainer.innerHTML =
                data.low_stock.map(item => `
                    <div class="alert-item">
                        <strong>${item.product_name}</strong>
                        <br>
                        Stock: ${item.current_stock}
                        | Reorder Level: ${item.reorder_level}
                    </div>
                `).join("");
        }


        // DEAD STOCK
        const deadStockContainer =
            document.getElementById("dead-stock");

        if (data.dead_stock.length === 0) {
            deadStockContainer.innerHTML =
                "<p>No dead-stock products.</p>";
        } else {
            deadStockContainer.innerHTML =
                data.dead_stock.map(item => `
                    <div class="alert-item">
                        <strong>${item.product_name}</strong>
                        <br>
                        Current Stock: ${item.current_stock}
                    </div>
                `).join("");
        }


        // SALES CHANGES
        const salesChangesContainer =
            document.getElementById("sales-changes");

        if (data.sales_changes.length === 0) {
            salesChangesContainer.innerHTML =
                "<div class='sales-item'>No significant sales changes detected.</div>";
        } else {
            salesChangesContainer.innerHTML =
                data.sales_changes.map(change => `
                    <div class="sales-item">
                        <strong>${change.change_type}</strong>
                        <br><br>
                        Date: ${change.date}
                        <br>
                        Latest Units: ${change.latest_units}
                        <br>
                        Previous Average:
                        ${change.previous_average_units}
                        <br>
                        Change:
                        ${change.percentage_change}%
                    </div>
                `).join("");
        }

    } catch (error) {
        console.error("Dashboard Error:", error);
    }
}


// --------------------------------------------------
// SUGGESTION BUTTON
// --------------------------------------------------

function setQuestion(question) {
    document.getElementById("question").value = question;
}


// --------------------------------------------------
// ASK AI
// --------------------------------------------------

async function askQuestion() {

    const question =
        document.getElementById("question").value.trim();

    const answer =
        document.getElementById("answer");


    if (!question) {
        answer.textContent = "Please enter a question.";
        return;
    }


    answer.innerHTML =
        "<strong>RetailIQ AI</strong><br><br>⏳ Analyzing your retail data...";


    try {

        const response = await fetch("/api/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })
        });


        const data = await response.json();


        if (!response.ok) {

            answer.innerHTML =
                "<strong>Error:</strong><br>" +
                (data.detail || "Unable to get AI response.");

            return;
        }


        answer.innerHTML =
            formatAnswer(data.answer);


    } catch (error) {

        console.error("AI Error:", error);

        answer.innerHTML =
            "<strong>Connection Error</strong><br><br>" +
            "Unable to connect to RetailIQ AI.";
    }
}


// --------------------------------------------------
// FORMAT GEMINI ANSWER
// --------------------------------------------------

function formatAnswer(text) {

    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/\n/g, "<br>")
        .replace(
            /ANSWER:/g,
            "<strong>ANSWER</strong><br>"
        )
        .replace(
            /EVIDENCE:/g,
            "<br><br><strong>EVIDENCE</strong><br>"
        )
        .replace(
            /RECOMMENDATION:/g,
            "<br><br><strong>RECOMMENDATION</strong><br>"
        );
}


// --------------------------------------------------
// START
// --------------------------------------------------

loadDashboard();