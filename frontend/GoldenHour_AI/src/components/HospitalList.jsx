import { useHospitals } from '../hooks';
import { useNotifyHospital } from '../hooks';

export default function HospitalList({ emergencyId }) {
  const { data: hospitals, isLoading, error } = useHospitals(emergencyId);
  const { mutate: notifyHospital, isPending: isNotifying } = useNotifyHospital();

  const handleNotify = (hospitalId) => {
    notifyHospital({ hospitalId, emergencyId });
  };

  if (!emergencyId) {
    return (
      <div style={styles.container}>
        <p style={styles.placeholder}>Submit an emergency to see available hospitals</p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div style={styles.container}>
        <div style={styles.loading}>
          <div style={styles.spinner}></div>
          <p>Finding nearest hospitals...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.container}>
        <div style={styles.error}>
          ❌ Error loading hospitals: {error.message}
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🏥 Available Hospitals ({hospitals?.length || 0})</h2>
      
      <div style={styles.list}>
        {hospitals?.map((hospital) => (
          <div 
            key={hospital.id} 
            style={{
              ...styles.card,
              border: hospital.isRecommended ? '2px solid #4CAF50' : '1px solid #333'
            }}
          >
            {hospital.isRecommended && (
              <div style={styles.recommendedBadge}>⭐ RECOMMENDED</div>
            )}
            
            <h3 style={styles.hospitalName}>{hospital.name}</h3>
            
            <div style={styles.infoGrid}>
              <div style={styles.infoItem}>
                <span style={styles.infoLabel}>Distance:</span>
                <span style={styles.infoValue}>{hospital.distance} km</span>
              </div>
              
              <div style={styles.infoItem}>
                <span style={styles.infoLabel}>ETA:</span>
                <span style={styles.infoValue}>{hospital.eta} min</span>
              </div>
              
              <div style={styles.infoItem}>
                <span style={styles.infoLabel}>Beds Available:</span>
                <span style={{
                  ...styles.infoValue,
                  color: hospital.bedsAvailable > 5 ? '#4CAF50' : '#ff6600'
                }}>
                  {hospital.bedsAvailable}
                </span>
              </div>
            </div>

            <div style={styles.specialties}>
              <strong>Specialties:</strong> {hospital.specialties.join(', ')}
            </div>

            <button
              onClick={() => handleNotify(hospital.id)}
              disabled={isNotifying}
              style={styles.notifyButton}
            >
              {isNotifying ? '📤 Notifying...' : '📢 Notify Hospital'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: '#1a1a1a',
    padding: '20px',
    borderRadius: '10px',
    maxWidth: '1200px',
    margin: '20px auto'
  },
  title: {
    color: '#4CAF50',
    marginTop: 0,
    marginBottom: '20px'
  },
  placeholder: {
    color: '#888',
    textAlign: 'center',
    padding: '40px'
  },
  loading: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '40px',
    color: 'white'
  },
  spinner: {
    border: '4px solid #333',
    borderTop: '4px solid #4CAF50',
    borderRadius: '50%',
    width: '40px',
    height: '40px',
    animation: 'spin 1s linear infinite'
  },
  error: {
    backgroundColor: '#ff4444',
    color: 'white',
    padding: '20px',
    borderRadius: '8px',
    textAlign: 'center'
  },
  list: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))',
    gap: '20px'
  },
  card: {
    backgroundColor: '#2a2a2a',
    padding: '20px',
    borderRadius: '10px',
    position: 'relative'
  },
  recommendedBadge: {
    backgroundColor: '#4CAF50',
    color: 'white',
    padding: '5px 10px',
    borderRadius: '5px',
    fontSize: '12px',
    fontWeight: 'bold',
    marginBottom: '10px',
    display: 'inline-block'
  },
  hospitalName: {
    color: 'white',
    marginTop: '10px',
    marginBottom: '15px',
    fontSize: '20px'
  },
  infoGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '10px',
    marginBottom: '15px'
  },
  infoItem: {
    display: 'flex',
    flexDirection: 'column'
  },
  infoLabel: {
    color: '#888',
    fontSize: '12px',
    marginBottom: '5px'
  },
  infoValue: {
    color: 'white',
    fontSize: '16px',
    fontWeight: 'bold'
  },
  specialties: {
    color: '#ccc',
    fontSize: '14px',
    marginBottom: '15px',
    paddingTop: '10px',
    borderTop: '1px solid #444'
  },
  notifyButton: {
    width: '100%',
    backgroundColor: '#2196F3',
    color: 'white',
    border: 'none',
    padding: '12px',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer'
  }
};
