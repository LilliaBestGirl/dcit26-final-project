import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Spinner from '../components/Spinner'
import api from '../api'
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../constants'

const Login = () => {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();

    try {
      const res = await api.post('/api/token/', { username, password });
      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
        
        navigate('/');
      }
    } catch (error) {
      console.log(error)
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
            <h1 className="text-2xl text-center">Login</h1>
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
              type="password"
              name="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className='rounded-lg p-2 w-full text-black border-2 border-black'
              required
            />
            <p className="text-sm mr-auto">Don't have an account? <Link to={'/register'} className='text-blue-400 underline'>Register here</Link></p>
            {loading ? <Spinner /> :
            <button
              type="submit"
              className="bg-red-500 text-white text-lg rounded-lg p-2 w-24 hover:bg-red-600 transition-colors"
            >
              Login
            </button>
            }
          </form>
        </section>
      </main>
    </>
  )
}

export default Login