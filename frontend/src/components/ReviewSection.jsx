import React, { useState, useEffect } from 'react'
import Review from './Review'
import ReviewForm from './ReviewForm'
import api from '../api'

const ReviewSection = ({ bookKey }) => {

  const [reviews, setReviews] = useState([]);
  const [user, setUser] = useState('');

  useEffect(() => {
    const fetchReviews = async () => {
      try {
        const res = await api.get(`api/book/review/?key=${bookKey}`);

        if (res.status !== 200) {
          throw new Error('Failed to fetch reviews');
        }
        setReviews(res.data || []);
      } catch (error) {
        console.error(error);
      }
    };

    fetchReviews();
  }, []);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get(`api/user/profile/`);
        if (res.status !== 200) {
          throw new Error('No user found');
        }
        setUser(res.data[0]['username']);
      } catch (error) {
        console.error(error);
      }
    };

    fetchUser();
  }, []);

  const formatDate = (date) => {
    const d = new Date(date);
    return `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`;
  }

  const handleAddReview = async (newReview) => {
    setReviews((prevReviews) => [newReview, ...prevReviews]);
  }

  const handleUpdateReview = (updatedReview) => {
    setReviews((prevReviews) =>
      prevReviews.map((review) =>
        review.id === updatedReview.id ? updatedReview : review
      )
    );
  }

  const handleDeleteReview = async (id) => {
    try {
      await api.delete(`api/user/review/${id}/`);
      setReviews((prevReviews) => prevReviews.filter((review) => review.id !== id));
    } catch (error) {
      console.error("Error deleting review:", error);
    }
  }

  return (
    <>
      <h1 className='text-3xl font-bold'>Reviews</h1>
      <ReviewForm book={bookKey} method="POST" action={handleAddReview} />
      <br />
      {reviews.length === 0 ?
        <p>No reviews yet</p>
        :
        reviews.map((review) => (
          <Review
            key={review.id}
            bookKey = {bookKey}
            reviewId={review.id}
            user={review.user}
            review={review.review}
            rating={review.rating}
            createDate={formatDate(review.created_at)}
            like={review.total_likes}
            dislike={review.total_dislikes}
            userReaction={review.user_reaction}
            isUser = {user === review.user}
            onUpdate={handleUpdateReview}
            onDelete={handleDeleteReview}
          />
        ))
      }
    </>
  )
}

export default ReviewSection