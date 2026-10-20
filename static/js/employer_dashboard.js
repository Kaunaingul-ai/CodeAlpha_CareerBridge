
document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll(".employer-status-form");

    // Read Django's CSRF token from the browser cookie.
    function getCookie(name) {
        const cookies = document.cookie ? document.cookie.split(";") : [];

        for (const cookie of cookies) {
            const trimmed = cookie.trim();

            if (trimmed.startsWith(name + "=")) {
                return decodeURIComponent(trimmed.substring(name.length + 1));
            }
        }

        return null;
    }

    forms.forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const applicationId = form.dataset.applicationId;
            const select = form.querySelector("select[name='status']");
            const button = form.querySelector("button[type='submit']");

            if (!applicationId || !select || !button) {
                return;
            }

            const originalText = button.textContent;

            button.disabled = true;
            button.textContent = "Saving...";

            try {
                const response = await fetch(
                    `/api/employer/applications/${applicationId}/status/`,
                    {
                        method: "PATCH",
                        credentials: "same-origin",
                        headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken": getCookie("csrftoken") || "",
                        },
                        body: JSON.stringify({
                            status: select.value,
                        }),
                    }
                );

                const data = await response.json();

                if (!response.ok) {
                    let message = "Unable to update application status.";

                    if (data.detail) {
                        message = data.detail;
                    } else if (data.status) {
                        message = String(data.status);
                    }

                    throw new Error(message);
                }

                // Refresh the dashboard statistics and status badges.
                window.location.reload();
            } catch (error) {
                alert(error.message || "Something went wrong.");
                button.disabled = false;
                button.textContent = originalText;
            }
        });
    });
});
