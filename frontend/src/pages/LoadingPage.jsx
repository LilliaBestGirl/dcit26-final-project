import React from 'react'
import Navbar from '../components/Navbar'
import Spinner from '../components/Spinner'

const LoadingPage = () => {
  return (
    <>
      <Navbar />
      <main className='mt-24'>
        <Spinner />
        <p className="text-center text-l text-red-500">Loading...</p>
      </main>
    </>
  )
}

export default LoadingPage