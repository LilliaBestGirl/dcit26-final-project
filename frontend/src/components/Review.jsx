import React, { useState } from 'react'
import { FaThumbsUp, FaThumbsDown } from 'react-icons/fa6'
import { ACCESS_TOKEN } from '../constants'
import api from '../api'
import ReviewForm from './ReviewForm'

// TODO: Style and implement review component
const Review = ({ reviewId, bookKey, user, review, rating, createDate, like, dislike, userReaction, isUser, onUpdate, onDelete }) => {

  const accessToken = localStorage.getItem(ACCESS_TOKEN);
  const [isEditing, setIsEditing] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [likes, setLikes] = useState(like);
  const [dislikes, setDislikes] = useState(dislike);
  const [initialReaction, setInitialReaction] = useState(userReaction);
  const MAX_LENGTH = 300;

  const toggleExpand = () => setIsExpanded(prev => !prev)

  const truncatedReview = review.length > MAX_LENGTH && !isExpanded
    ? `${review.slice(0, MAX_LENGTH)}...`
    : review;

  const handleReaction = async (reviewId, reaction) => {  
    
    try {
      const res = await api.post('api/review/reaction/', { review: reviewId, reaction });

      if (res.status === 201) {

        if (reaction === 'like') {
          setLikes(() => likes + 1);
        } else if (reaction === 'dislike') {
          setDislikes(() => dislikes + 1);
        }

        setInitialReaction(reaction);

      } else if (res.status === 200) {
        setInitialReaction(reaction)

        if (initialReaction === 'like' && reaction === 'dislike') {
          setLikes(() => likes - 1);
          setDislikes(() => dislikes + 1);
        } else if (initialReaction === 'dislike' && reaction === 'like') {
          setLikes(() => likes + 1);
          setDislikes(() => dislikes - 1);
        }

      } else if (res.status === 204) {

        if (initialReaction === 'like') {
          setLikes(() => likes - 1);
        } else if (initialReaction === 'dislike') {
          setDislikes(() => dislikes - 1);
        }

        setInitialReaction(null);
      }
    } catch (error) {
      console.error(error);
    }
  }

  const submitEdit = (editData) => {
    onUpdate(editData);
    setIsEditing(false);
  }

  const handleDelete = (id) => {
    if (window.confirm('Are you sure you want to delete this review?')) {
      onDelete(id);
    }
  }

  return (
    <article className='border-2 border-black rounded-lg p-4 mb-4'>
      {isEditing ? (
        <>
          <ReviewForm book={bookKey} reviewId={reviewId} method="PUT" action={submitEdit} currentReview={{ rating, review }} />
          <button onClick={() => setIsEditing(false)} className='bg-red-500 text-white text-lg rounded-lg p-2 hover:bg-red-600 transition-colors mt-4'>Cancel</button>
        </>
      ) : (
        <div className='whitespace-pre-wrap'>
          <p className='text-xl font-bold'>{user}</p>
          <p className='text-sm'>{createDate}</p>
          <p className='text-lg font bold'>Rating: {rating}/5</p>
          <p className='text-xl'>{truncatedReview}</p>
          <br />
          {
            review.length > MAX_LENGTH && (
              <button className="text-blue-400 mt-2" onClick={toggleExpand}>
                {isExpanded ? 'Read less' : 'Read more'}
              </button>
            )
          }
          <div className="flex gap-8 text-lg">
            <p><button className='inline mr-2' onClick={() => handleReaction(reviewId, 'like')} disabled={accessToken ? false : true}><FaThumbsUp className={`${initialReaction === 'like' ? 'text-blue-500' : ''} transition-colors`} /></button>{likes > 0 ? likes : ''}</p>
            <p><button className='inline mr-2' onClick={() => handleReaction(reviewId, 'dislike')} disabled={accessToken ? false : true}><FaThumbsDown className={`${initialReaction === 'dislike' ? 'text-blue-500' : ''} transition-colors`} /></button>{dislikes > 0 ? dislikes : ''}</p>
            {isUser ?
              <>
                <p><button onClick={() => setIsEditing(true)}>Edit</button></p>
                <p><button onClick={() => handleDelete(reviewId)}>Delete</button></p>
              </>
              : ""
            }
          </div>
        </div>
      )}
    </article>
  )
}

export default Review