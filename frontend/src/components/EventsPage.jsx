import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000'

function EventsPage() {
  const [newEvent, setNewEvent] = useState({
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    location: ''
  })
  const queryClient = useQueryClient()

  const { data: events, isLoading, error } = useQuery('events', async () => {
    const response = await axios.get(`${API_URL}/events`)
    return response.data
  })

  const createEventMutation = useMutation(
    (event) => {
      // Format dates to ISO string before sending
      const formattedEvent = {
        ...event,
        start_date: new Date(event.start_date).toISOString(),
        end_date: new Date(event.end_date).toISOString()
      }
      return axios.post(`${API_URL}/events`, formattedEvent)
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('events')
        setNewEvent({ name: '', description: '', start_date: '', end_date: '', location: '' })
      },
    }
  )

  const handleSubmit = (e) => {
    e.preventDefault()
    createEventMutation.mutate(newEvent)
  }

  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Create New Event</h2>
      <form onSubmit={handleSubmit} className="mb-8">
        <input
          type="text"
          placeholder="Event Name"
          value={newEvent.name}
          onChange={(e) => setNewEvent({ ...newEvent, name: e.target.value })}
          className="w-full p-2 mb-2 border rounded"
          required
        />
        <textarea
          placeholder="Event Description"
          value={newEvent.description}
          onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })}
          className="w-full p-2 mb-2 border rounded"
          required
        />
        <input
          type="datetime-local"
          placeholder="Start Date"
          value={newEvent.start_date}
          onChange={(e) => setNewEvent({ ...newEvent, start_date: e.target.value })}
          className="w-full p-2 mb-2 border rounded"
          required
        />
        <input
          type="datetime-local"
          placeholder="End Date"
          value={newEvent.end_date}
          onChange={(e) => setNewEvent({ ...newEvent, end_date: e.target.value })}
          className="w-full p-2 mb-2 border rounded"
          required
        />
        <input
          type="text"
          placeholder="Location"
          value={newEvent.location}
          onChange={(e) => setNewEvent({ ...newEvent, location: e.target.value })}
          className="w-full p-2 mb-2 border rounded"
          required
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Create Event
        </button>
      </form>

      <h2 className="text-2xl font-semibold mb-4">Events List</h2>
      <ul>
        {events && events.map((event) => (
          <li key={event.id} className="mb-4 p-4 border rounded">
            <h3 className="text-xl font-semibold">{event.title}</h3>
            <p>{event.description}</p>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default EventsPage