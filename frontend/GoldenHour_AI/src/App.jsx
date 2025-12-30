import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import EmergencyForm from './components/EmergencyForm';
import TriageResults from './components/TriageResults';
import AgentStatus from './components/AgentStatus';
import HospitalList from './components/HospitalList';


const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: true,
      staleTime: 30000,
      retry: 2,
    },
  },
});


function Dashboard() {
  const [emergencyId, setEmergencyId] = useState(null);
  const [triageData, setTriageData] = useState(null);


  const handleEmergencyCreated = (id, data) => {
    setEmergencyId(id);
    setTriageData(data);
  };


  return (
    <div style={styles.dashboard}>
      <header style={styles.header}>
        <h1 style={styles.mainTitle}>⚡ Golden Hour Response Dashboard</h1>
        <p style={styles.subtitle}>AI-Powered Emergency Healthcare System</p>
      </header>


      <EmergencyForm onEmergencyCreated={handleEmergencyCreated} />
      
      <TriageResults triageData={triageData} />
      
      <AgentStatus emergencyId={emergencyId} />
      
      <HospitalList emergencyId={emergencyId} />
    </div>
  );
}


function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Dashboard />
      {/* Only show devtools in development, hidden in production */}
      {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
    </QueryClientProvider>
  );
}


const styles = {
  dashboard: {
    minHeight: '100vh',
    backgroundColor: '#0f0f0f',
    padding: '20px',
    fontFamily: 'Arial, sans-serif'
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px',
    padding: '20px',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    borderRadius: '15px'
  },
  mainTitle: {
    margin: 0,
    color: 'white',
    fontSize: '36px',
    textShadow: '2px 2px 4px rgba(0,0,0,0.3)'
  },
  subtitle: {
    margin: '10px 0 0 0',
    color: '#ddd',
    fontSize: '18px'
  }
};


export default App;
