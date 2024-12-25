let fetchToken = async () => {
    let response = await fetch("http://127.0.0.1:8000/api/token/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: "administrator",
            password: "123admin123",
        }),
    });

    // Check if the response is OK
    if (!response.ok) {
        console.error("Failed to fetch token:", response.statusText);
        return;
    }

    let data = await response.json();
    console.log(response.headers);
};

fetchToken();
