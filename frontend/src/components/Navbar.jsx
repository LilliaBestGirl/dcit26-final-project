import React from 'react'
import { Link } from 'react-router-dom'
import { GiHamburgerMenu } from 'react-icons/gi';
import { ACCESS_TOKEN } from '../constants'
import SearchBar from './SearchBar';

const Navbar = () => {

  const token = localStorage.getItem(ACCESS_TOKEN);

  return (
    <header>
        <nav className='flex bg-stone-700 text-white items-center px-4 md:px-8 py-2'>
            <h1 className='text-3xl font-bold'><Link to={'/'}>Logo</Link></h1>
            <SearchBar />
            <section className='hidden ml-auto sm:block'>
                <Link to={token ? '/logout' : '/login'} className='text-lg bg-red-500 p-2 rounded-lg hover:bg-red-600 transition-all'>{token ? 'Logout' : 'Login'}</Link>
            </section>
            <section className='ml-auto sm:hidden'>
                <button><GiHamburgerMenu className='text-3xl'/></button>
            </section>
        </nav>
    </header>
  )
}

export default Navbar