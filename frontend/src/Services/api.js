import axios from "axios";

// Create an instance of axios with default configurations
const api = axios.create({
  baseURL: "http://localhost:5000/api",
  headers: {
    "content-type": "application/json",
  },
});

export default api;
