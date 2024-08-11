import React, { useEffect, useState } from "react";
import "./App.css";
import Login from "./Components/Login/Login";
import api from "./Services/api";

function App() {
  const [users, setUsers] = useState();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch users from the API
    const fetchUsers = async () => {
      try {
        const response = await api.get("/users"); // Assuming you have a '/users' endpoint
        setUsers(response.data);
        console.log(users);
      } catch (error) {
        console.error("Error fetching users:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []); // Empty dependency array means this effect runs once after the initial render

  return (
    <div className="App">
      <Login />
    </div>
  );
}

export default App;
