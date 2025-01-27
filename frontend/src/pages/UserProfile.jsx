import React, { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import LoadingPage from './LoadingPage'
import Badge from '../components/Badge'
import api from '../api'

// TODO: Do this eventually

const UserProfile = () => {

  const [username, setUsername] = useState('');
  const [badges, setBadges] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const res = await api.get('api/user/profile/');

        if (res.status === 200) {
          setUsername(res.data[0]['username']);
        }
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    const fetchBadges = async () => {
      try {
        const res = await api.get('api/user/badge/');

        if (res.status === 200) {
          setBadges(res.data || []);
          console.log(res.data)
        }
      } catch (error) {
        console.error("Error fetching badges", error);
        
      }
    }

    fetchBadges();
  }, []);

  if (loading) {
    return <LoadingPage />;
  }

  return (
    <>
      <Navbar />
      <main>
        <h1 className='text-3xl font-bold text-red-500'>User Profile</h1>
        <h1>Username: {username}</h1>
        <section className='w-90 flex flex-col gap-4 mx-6 p-6 border-2 border-black rounded-lg'>
          <h1 className='text-3xl font-bold'>Badges</h1>
          <article className="flex flex-wrap gap-4">
            {badges.map((badge, index) => (
              <Badge key={index} badge={badge} />
            ))}
          </article>
        </section>
      </main>
    </>
  )
}

export default UserProfile