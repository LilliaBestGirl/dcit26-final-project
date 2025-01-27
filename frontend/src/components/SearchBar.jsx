import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

const SearchBar = () => {

  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    if (!query) return;
    
    e.preventDefault();
    const encodedQuery = encodeURIComponent(query);
    navigate(`/search?q=${encodedQuery}`);
  }

  return (
    <form className='flex gap-2 flex-grow justify-center' onSubmit={handleSubmit}>
      <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search" className="rounded-lg p-2 w-5/6 md:w-1/2 text-black" required />
      <button type="submit" className="bg-red-500 text-white text-lg rounded-lg p-2 hidden md:block hover:bg-red-600 transition-colors">Search</button>
    </form>
  )
}

export default SearchBar