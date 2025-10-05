import { register, login, getUsers } from './api';

function App() {
  const handleRegister = async () => {
    const userData = { username: 'testuser', email: 'test@example.com', password: 'SecurePass123' };
    const result = await register(userData);
    console.log(result);
  };

  const handleLogin = async () => {
    const credentials = { email: 'test@example.com', password: 'SecurePass123' };
    const result = await login(credentials);
    console.log(result);
  };

  const handleGetUsers = async () => {
    const token = localStorage.getItem('token');
    const users = await getUsers(token);
    console.log(users);
  };

  return (
    <div>
      <button onClick={handleRegister}>Register</button>
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleGetUsers}>Get Users</button>
    </div>
  );
}
export default App;