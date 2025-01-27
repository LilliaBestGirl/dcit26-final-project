import React from 'react'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import NotFound from './pages/NotFound';
import ResultsPage from './pages/ResultsPage';
import BookDetail from './pages/BookDetail';
import UserProfile from './pages/UserProfile';
import ProtectedLayout from './components/ProtectedLayout';
import './index.css'

const Logout = () => {
  localStorage.clear()
  return <Navigate to="/" />
}

const RegisterAndLogout = () => {
  localStorage.clear()
  return <Register />
}

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<ProtectedLayout redirect={false}/>}>
          <Route path='/' element={<Home />} />
          <Route path='/login' element={<Login />} />
          <Route path='/logout' element={<Logout />} />
          <Route path='/register' element={<RegisterAndLogout />} />
          <Route path='/search' element={<ResultsPage />} />
          <Route path='/book' element={<BookDetail />} />
          <Route path='*' element={<NotFound />} />
        </Route>
        <Route element={<ProtectedLayout redirect={true}/>}>
          <Route path="/profile" element={<UserProfile />}/>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App