export default function AmbulanceSelector({ onSelect }) {
  const handleSelection = (needsAmbulance) => {
    onSelect(needsAmbulance);
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>🚑 Do you need an ambulance?</h3>
      <p style={styles.description}>
        Select whether you need ambulance pickup or can reach the hospital directly
      </p>
      
      <div style={styles.buttonContainer}>
        <button 
          onClick={() => handleSelection(true)}
          style={{...styles.button, ...styles.yesButton}}
        >
          <span style={styles.buttonIcon}>🚑</span>
          <div>
            <div style={styles.buttonTitle}>Yes, Send Ambulance</div>
            <div style={styles.buttonSubtitle}>Ambulance will pick you up</div>
          </div>
        </button>
        
        <button 
          onClick={() => handleSelection(false)}
          style={{...styles.button, ...styles.noButton}}
        >
          <span style={styles.buttonIcon}>🚗</span>
          <div>
            <div style={styles.buttonTitle}>No, I'll Go Myself</div>
            <div style={styles.buttonSubtitle}>Direct route to hospital</div>
          </div>
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: '#1a1a1a',
    padding: '30px',
    borderRadius: '10px',
    marginTop: '20px',
    textAlign: 'center'
  },
  title: {
    color: '#4CAF50',
    margin: '0 0 10px 0',
    fontSize: '24px'
  },
  description: {
    color: '#ccc',
    margin: '0 0 30px 0',
    fontSize: '14px'
  },
  buttonContainer: {
    display: 'flex',
    gap: '20px',
    justifyContent: 'center',
    flexWrap: 'wrap'
  },
  button: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
    padding: '20px 30px',
    border: 'none',
    borderRadius: '10px',
    cursor: 'pointer',
    fontSize: '16px',
    transition: 'all 0.3s ease',
    minWidth: '250px'
  },
  yesButton: {
    backgroundColor: '#ff4444',
    color: 'white'
  },
  noButton: {
    backgroundColor: '#2196F3',
    color: 'white'
  },
  buttonIcon: {
    fontSize: '32px'
  },
  buttonTitle: {
    fontWeight: 'bold',
    fontSize: '18px',
    marginBottom: '5px'
  },
  buttonSubtitle: {
    fontSize: '12px',
    opacity: 0.9
  }
};
