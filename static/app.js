// static/app.js
document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("register-form");
  const loginForm = document.getElementById("login-form");
  const postForm = document.getElementById("post-form");
  const postsList = document.getElementById("posts-list");
  let authToken = "";

  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;

    const response = await fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      alert("Registration successful");
    } else {
      alert("Registration failed");
    }
  });

  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      const data = await response.json();
      authToken = data.token;
      alert("Login successful");
    } else {
      alert("Login failed");
    }
  });

  postForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const title = document.getElementById("post-title").value;
    const content = document.getElementById("post-content").value;

    const response = await fetch("/api/posts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      body: JSON.stringify({ title, content }),
    });

    if (response.ok) {
      alert("Post created successfully");
      fetchPosts(); // Refresh posts list
    } else {
      alert("Post creation failed");
    }
  });

  async function fetchPosts() {
    const response = await fetch("/api/posts");
    const posts = await response.json();

    postsList.innerHTML = "";
    posts.forEach((post) => {
      const li = document.createElement("li");
      li.textContent = `${post.title}: ${post.content}`;
      postsList.appendChild(li);
    });
  }

  // Function to fetch the logged-in user
  async function getUserInfo() {
    try {
      const response = await fetch("/api/user_info", {
        method: "GET",
        credentials: "include", // Include cookies with the request
      });
      if (response.ok) {
        const data = await response.json();
        document.getElementById(
          "username"
        ).textContent = `Hello, ${data.username}`;
        document.getElementById("user-info").style.display = "block";
        document.getElementById("login-info").style.display = "none";
      } else {
        document.getElementById("login-info").style.display = "block";
      }
    } catch (error) {
      console.error("Error fetching user info:", error);
    }
  }

  // Function to handle logout
  async function handleLogout() {
    try {
      const response = await fetch("/api/logout", {
        method: "POST",
        credentials: "include", // Include cookies with the request
      });
      if (response.ok) {
        window.location.href = "/"; // Redirect to homepage or login page
      } else {
        console.error("Logout failed");
      }
    } catch (error) {
      console.error("Error during logout:", error);
    }
  }

  // Event listener for logout button
  document
    .getElementById("logout-button")
    .addEventListener("click", handleLogout);

  // Fetch user info on page load
  getUserInfo();

  fetchPosts(); // Load posts on page load
});
