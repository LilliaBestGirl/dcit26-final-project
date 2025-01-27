import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar';
import Spinner from '../components/Spinner';
import api from '../api';

const Register = () => {

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();

    try {
      const res = await api.post('/api/register/', { username, email, password });
      if (res.status === 201) {
        alert('Registration successful, log in to continue.');
        navigate('/login');
      }
    } catch (error) {
      console.log(error);
      
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
    <Navbar />
      <main>
        <section className='flex items-center justify-center mt-24'>
          <form action="" method="post" onSubmit={handleSubmit} className='flex flex-col gap-4 items-center justify-center w-72 border-2 border-black rounded-lg p-4'>
            <h1 className="text-2xl text-center">Register</h1>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className='rounded-lg p-2 w-full text-black border-2 border-black'
              required
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className='rounded-lg p-2 w-full text-black border-2 border-black'
              required
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className='rounded-lg p-2 w-full text-black border-2 border-black'
              required
            />
            <p className="text-sm mr-auto">Already have an account? <Link to={'/login'} className='text-blue-400 underline'>Login here</Link></p>
            {loading ? <Spinner /> :
            <button
              type="submit"
              className="bg-red-500 text-white text-lg rounded-lg p-2 w-24 hover:bg-red-600 transition-colors"
            >
              Register
            </button>
            }
          </form>
        </section>
      </main>
    </>
  )
}

export default Register