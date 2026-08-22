const API_BASE_URL = "http://127.0.0.1:8000";

const Auth = {

    async requestOtp(phoneNumber) {

        const response = await fetch(
            `${API_BASE_URL}/api/v1/auth/request-otp`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    phone_number: phoneNumber
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Unable to request OTP"
            );
        }

        return data;
    },


    async verifyOtp(phoneNumber, otp) {

        const response = await fetch(
            `${API_BASE_URL}/api/v1/auth/verify-otp`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    phone_number: phoneNumber,
                    otp: otp
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Invalid OTP"
            );
        }

        localStorage.setItem(
            "clinexa_access_token",
            data.access_token
        );

        return data;
    },


    async getCurrentUser() {

        const token = this.getToken();

        if (!token) {
            return null;
        }

        const response = await fetch(
            `${API_BASE_URL}/api/v1/auth/me`,
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );

        if (!response.ok) {

            this.logout();

            return null;
        }

        return await response.json();
    },


    getToken() {

        return localStorage.getItem(
            "clinexa_access_token"
        );
    },


    isAuthenticated() {

        return !!this.getToken();
    },


    logout() {

        localStorage.removeItem(
            "clinexa_access_token"
        );

        localStorage.removeItem(
            "clinexa_phone_number"
        );
    }
};