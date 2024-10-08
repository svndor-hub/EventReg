import { QueryClient, QueryClientProvider } from 'react-query'
import EventsPage from './components/EventsPage'
import './App.css'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold mb-4">Event Management</h1>
        <EventsPage />
      </div>
    </QueryClientProvider>
  )
}

export default App
