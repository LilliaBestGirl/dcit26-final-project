import React from 'react'
import { Link } from 'react-router-dom';
import NoCover from '../assets/NoCover.jpg'

const BookResult = ({ book }) => {

  const bookCover = book.cover_edition_key ? `https://covers.openlibrary.org/b/olid/${book.cover_edition_key}-M.jpg` : NoCover;

  return (
    <div className='flex gap-2 justify-center items-center border-2 border-black rounded-lg w-90 max-h-72 p-4 shadow-md hover:shadow-lg transition-shadow'>
      <img
        src={bookCover}
        alt={`Cover of ${book.title}`}
        className='w-36 h-48 object-cover'
      />
      <article>
        <div className="relative group w-32">
          <h1 className='text-center truncate-title w-full overflow-hidden text-ellipsis whitespace-nowrap cursor-default'>
            <Link to={`/book?key=${book.key}`}>{book.title}</Link>
          </h1>
          <div className='absolute top-2/3 left-1/2 -translate-x-1/2 mt-2 hidden group-hover:block bg-black text-white text-sm p-2 rounded-lg shadow-lg w-max max-w-xs transition-all'>
            {book.title}
          </div>
        </div>
        <p>Rating: {book.rating} {isNaN(book.rating) ? '' : '⭐'}</p>
      </article>
    </div>
  )
}

export default BookResult