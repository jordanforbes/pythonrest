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

  fetchPosts(); // Load posts on page load
});
