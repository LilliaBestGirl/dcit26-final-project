import React, { useEffect, useState } from 'react'
import api from '../api'

const ReviewForm = ({ book, reviewId, method, action, currentReview }) => {

  const [rating, setRating] = useState(0)
  const [review, setReview] = useState('')

  useEffect(() => {
    if (currentReview) {
      setRating(currentReview.rating)
      setReview(currentReview.review)
    }
  }, [currentReview])

  const handleSumbit = async (e) => {
    e.preventDefault();
    
    try {
      if (method === 'PUT') {
        const res = await api.put(`api/user/review/${reviewId}/`, { rating, review, book })
        if (res.status === 200) {
          action(res.data);
          setRating(0);
          setReview('');
        }
      } else if (method === 'POST') {
        const res = await api.post('api/user/review/', { rating, review, book })
        if (res.status === 201) {
          action(res.data);
          setRating(0);
          setReview('');
        }
      }
    } catch (error) {
      if (error.status === 500) {
        alert('You can only post one review per book.');
      }
    }
  }

  return (
    <form method='POST' onSubmit={handleSumbit}>
      <div className='flex flex-col gap-2'>
        <label htmlFor="rating">Rating</label>
        <input type="number" name="rating" id="rating" min="1" max="5" placeholder='Rating' className='border border-gray-300 rounded-lg p-2' value={rating} onChange={(e) => setRating(e.target.value)} required />
      </div>
      <div className='flex flex-col gap-2'>
        <label htmlFor="review">Review</label>
        <textarea name="review" id="review" cols="30" rows="10" placeholder='Review' className='border border-gray-300 rounded-lg p-2' value={review} onChange={(e) => setReview(e.target.value)} required></textarea>
      </div>
      <button type='submit' className='bg-red-500 text-white text-lg rounded-lg p-2 hover:bg-red-600 transition-colors mt-4'>Submit</button>
    </form>
  )
}

export default ReviewForm