import { useHospitals } from '../hooks';
import { useNotifyHospital } from '../hooks';

export default function HospitalList({ emergencyId }) {
  const { data: hospitalsResponse, isLoading, error } = useHospitals(emergencyId);
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

  // FIXED: Safely extract hospitals array from different response formats
  let hospitals = [];
  
  if (Array.isArray(hospitalsResponse)) {
    // Response is already an array
    hospitals = hospitalsResponse;
  } else if (hospitalsResponse?.hospitals && Array.isArray(hospitalsResponse.hospitals)) {
    // Response has a hospitals property
    hospitals = hospitalsResponse.hospitals;
  } else if (hospitalsResponse?.data && Array.isArray(hospitalsResponse.data)) {
    // Response has a data property
    hospitals = hospitalsResponse.data;
  } else if (hospitalsResponse?.hospital) {
    // Single hospital object
    hospitals = [hospitalsResponse.hospital];
  }

  // Show empty state if no hospitals
  if (!hospitals || hospitals.length === 0) {
    return (
      <div style={styles.container}>
        <h2 style={styles.title}>🏥 Available Hospitals</h2>
        <div style={styles.empty}>
          <p>⏳ Searching for nearby hospitals...</p>
          <p style={styles.emptySubtext}>This may take a few moments while AI agents process your request</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🏥 Available Hospitals ({hospitals.length})</h2>
      
      <div style={styles.list}>
        {hospitals.map((hospital, index) => (
          <div 
            key={hospital.id || index} 
            style={{
              ...styles.card,
              border: hospital.isRecommended ? '2px solid #4CAF50' : '1px solid #333'
            }}
          >
            {hospital.isRecommended && (
              <div style={styles.recommendedBadge}>⭐ RECOMMENDED</div>
            )}
            
            <h3 style={styles.hospitalName}>
              {hospital.name || `Hospital ${index + 1}`}
            </h3>
            
            <div style={styles.infoGrid}>
              <div style={styles.infoItem}>
                <span style={styles.infoLabel}>Distance:</span>
                <span style={styles.infoValue}>
                  {hospital.distance || 'N/A'} {hospital.distance ? 'km' : ''}
                </span>
              </div>
              
              <div style={styles.infoItem}>
                <span style={styles.infoLabel}>ETA:</span>
                <span style={styles.infoValue}>
                  {hospital.eta || hospital.estimatedArrivalTime || 'N/A'} 
                  {hospital.eta ? ' min' : ''}
                </span>
              </div>
              
              <div style={styles.infoItem}>
                <span style={styles.infoLabel}>Beds Available:</span>
                <span style={{
                  ...styles.infoValue,
                  color: (hospital.bedsAvailable || 0) > 5 ? '#4CAF50' : '#ff6600'
                }}>
                  {hospital.bedsAvailable !== undefined ? hospital.bedsAvailable : 'N/A'}
                </span>
              </div>
            </div>

            {/* Address */}
            {hospital.address && (
              <div style={styles.address}>
                📍 {hospital.address}
              </div>
            )}

            {/* Phone */}
            {hospital.phone && (
              <div style={styles.phone}>
                📞 {hospital.phone}
              </div>
            )}

            {/* Specialties */}
            {hospital.specialties && Array.isArray(hospital.specialties) && hospital.specialties.length > 0 && (
              <div style={styles.specialties}>
                <strong>Specialties:</strong> {hospital.specialties.join(', ')}
              </div>
            )}

            <button
              onClick={() => handleNotify(hospital.id || index)}
              disabled={isNotifying}
              style={{
                ...styles.notifyButton,
                opacity: isNotifying ? 0.6 : 1,
                cursor: isNotifying ? 'not-allowed' : 'pointer'
              }}
              onMouseEnter={(e) => {
                if (!isNotifying) {
                  e.currentTarget.style.backgroundColor = '#1976D2';
                }
              }}
              onMouseLeave={(e) => {
                if (!isNotifying) {
                  e.currentTarget.style.backgroundColor = '#2196F3';
                }
              }}
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
    marginBottom: '20px',
    fontSize: '24px'
  },
  placeholder: {
    color: '#888',
    textAlign: 'center',
    padding: '40px',
    fontSize: '16px'
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
    animation: 'spin 1s linear infinite',
    marginBottom: '20px'
  },
  error: {
    backgroundColor: '#ff4444',
    color: 'white',
    padding: '20px',
    borderRadius: '8px',
    textAlign: 'center',
    fontWeight: 'bold'
  },
  empty: {
    textAlign: 'center',
    padding: '40px',
    color: '#aaa'
  },
  emptySubtext: {
    fontSize: '14px',
    color: '#666',
    marginTop: '10px'
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
    position: 'relative',
    transition: 'transform 0.2s ease, box-shadow 0.2s ease'
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
  address: {
    color: '#ccc',
    fontSize: '14px',
    marginBottom: '8px',
    paddingTop: '10px',
    borderTop: '1px solid #444'
  },
  phone: {
    color: '#ccc',
    fontSize: '14px',
    marginBottom: '8px'
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
    cursor: 'pointer',
    transition: 'background-color 0.3s ease',
    marginTop: '10px'
  }
};
