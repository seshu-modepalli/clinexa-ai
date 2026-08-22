document.addEventListener("DOMContentLoaded", async () => {

    const authScreen =
        document.getElementById("auth-screen");

    const phoneStep =
        document.getElementById("phone-step");

    const otpStep =
        document.getElementById("otp-step");

    const phoneInput =
        document.getElementById("phone-number");

    const otpInput =
        document.getElementById("otp");

    const requestOtpButton =
        document.getElementById("request-otp-btn");

    const verifyOtpButton =
        document.getElementById("verify-otp-btn");

    const changeNumberButton =
        document.getElementById("change-number-btn");

    const errorElement =
        document.getElementById("auth-error");


    function showError(message) {

        errorElement.textContent = message;
    }


    function clearError() {

        errorElement.textContent = "";
    }


    function showPhoneStep() {

        phoneStep.style.display = "block";

        otpStep.style.display = "none";

        clearError();
    }


    function showOtpStep() {

        phoneStep.style.display = "none";

        otpStep.style.display = "block";

        otpInput.focus();

        clearError();
    }


    async function initialize() {

        const user = await Auth.getCurrentUser();

        if (user) {

            authScreen.style.display = "none";

            console.log(
                "Authenticated user:",
                user
            );

        } else {

            authScreen.style.display = "flex";
        }
    }


    requestOtpButton.addEventListener(
        "click",
        async () => {

            clearError();

            const phoneNumber =
                phoneInput.value.trim();

            if (!/^\d{10}$/.test(phoneNumber)) {

                showError(
                    "Please enter a valid 10-digit mobile number."
                );

                return;
            }

            requestOtpButton.disabled = true;

            requestOtpButton.textContent =
                "Sending OTP...";

            try {

                await Auth.requestOtp(
                    phoneNumber
                );

                localStorage.setItem(
                    "clinexa_phone_number",
                    phoneNumber
                );

                showOtpStep();

            } catch (error) {

                showError(
                    error.message
                );

            } finally {

                requestOtpButton.disabled = false;

                requestOtpButton.textContent =
                    "Continue";
            }
        }
    );


    verifyOtpButton.addEventListener(
        "click",
        async () => {

            clearError();

            const phoneNumber =
                localStorage.getItem(
                    "clinexa_phone_number"
                );

            const otp =
                otpInput.value.trim();

            if (!/^\d{6}$/.test(otp)) {

                showError(
                    "Please enter the 6-digit OTP."
                );

                return;
            }

            verifyOtpButton.disabled = true;

            verifyOtpButton.textContent =
                "Verifying...";

            try {

                await Auth.verifyOtp(
                    phoneNumber,
                    otp
                );

                const user =
                    await Auth.getCurrentUser();

                console.log(
                    "Clinexa user:",
                    user
                );

                authScreen.style.display =
                    "none";

            } catch (error) {

                showError(
                    error.message
                );

            } finally {

                verifyOtpButton.disabled =
                    false;

                verifyOtpButton.textContent =
                    "Verify OTP";
            }
        }
    );


    changeNumberButton.addEventListener(
        "click",
        () => {

            localStorage.removeItem(
                "clinexa_phone_number"
            );

            otpInput.value = "";

            showPhoneStep();
        }
    );


    await initialize();
});