import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import ReviewSection from '../components/ReviewSection';
import LoadingPage from './LoadingPage';
import NoCover from '../assets/NoCover.jpg';
import api from '../api';

const BookDetail = () => {
 
  const [searchParams] = useSearchParams();
  const key = searchParams.get('key');
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  let description = 'No description available.'; // * Default value

  if (typeof data.description === 'string' && data.description.length > 0) {
    description = data.description;
  } else if (data.description?.value) {
    description = data.description.value;
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/api/book/?key=${key}`);

        setData(response.data);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return <LoadingPage />;
  }

  return (
    <>
      <Navbar />
      <main className='m-12'>
        <section className='flex gap-10 flex-col justify-center items-center md:flex-row'>
          {data.covers && data.covers.length > 0 ?
            <img
              src={`https://covers.openlibrary.org/b/id/${data.covers[0]}-M.jpg`}
              alt={`Cover of ${data.title}`}
              className='w-72 h-96 object-cover'
            />
            :
            <img
              src={NoCover}
              alt={`Cover of ${data.title}`}
              className='w-72 h-96 object-cover'
            />
          }
          <article>
            <h1 className='text-3xl font-bold text-red-500 text-center sm:text-left'>{data.title}</h1>
            <br />
            <p className="text-lg">Author/s: ??? {/* Add actual authors */}</p>
            <p className='text-lg'>{description}</p>
            <p className='mt-4 text-lg'>Rating: {data.rating}{ isNaN(data.rating) ? '' : '/5 ⭐'}</p>
          </article>
        </section>
        <section className="mt-8">
          <ReviewSection bookKey={key} />
        </section>
      </main>
    </>
  )
}

export default BookDetail