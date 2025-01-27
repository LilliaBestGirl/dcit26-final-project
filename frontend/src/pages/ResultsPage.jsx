import React, { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import Navbar from '../components/Navbar';
import LoadingPage from './LoadingPage';
import BookResult from '../components/BookResult';
import api from '../api';

const ResultsPage = () => {

  const [searchParams] = useSearchParams();
  const query = searchParams.get('q');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        setLoading(true);
        const encodedQuery = encodeURIComponent(query);
        const res = await api.get(`api/search/?q=${encodedQuery}&page=${page}`);
        setResults(res.data.docs || []);
        setTotalPages(Math.ceil(res.data.numFound / 20));
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [query, page]);

  if (loading) {
    return <LoadingPage />
  }

  return (
    <>
      <Navbar />
      <main>
        <h1 className="text-2xl font-bold ml-8 mt-8 sm:text-3xl sm:ml-24">Results for "{query}"</h1>
        <section className="grid gap-4 m-8 sm:grid-cols-2 md:grid-cols-3 place-items-center">
          {results.length > 0 ?
            results.map((book) => <BookResult key={book.key} book={book} />)
            :
            <h1 className='text-3xl font-bold text-center'>No books found</h1>
          }
        </section>

        {results.length > 0 && (
          <section className="mx-auto my-8 flex gap-4 justify-center">
            <button className='border-2 border-black px-4 py-2 rounded-lg transition-colors hover:bg-gray-300 disabled:cursor-not-allowed' disabled={page === 1} onClick={() => setPage(page - 1)}>Previous</button>
            <p className='text-lg mt-2'>Page {page} of {totalPages}</p>
            <button className='border-2 border-black px-8 py-2 rounded-lg transition-colors hover:bg-gray-300 disabled:cursor-not-allowed' disabled={page === totalPages || totalPages === 0} onClick={() => setPage(page + 1)}>Next</button>
          </section>
        )}
      </main>
    </>
  )
}

export default ResultsPage