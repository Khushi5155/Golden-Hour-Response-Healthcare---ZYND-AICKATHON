export default function TriageResults({ triageData }) {
  if (!triageData) return null;

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return '#ff0000';
      case 'high': return '#ff6600';
      case 'medium': return '#ffaa00';
      case 'low': return '#4CAF50';
      default: return '#666';
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>📊 Triage Analysis</h2>
      
      <div style={styles.grid}>
        <div style={styles.card}>
          <div style={styles.cardLabel}>Emergency ID</div>
          <div style={styles.cardValue}>{triageData.emergencyId}</div>
        </div>

        <div style={{
          ...styles.card,
          borderLeft: `4px solid ${getSeverityColor(triageData.severity)}`
        }}>
          <div style={styles.cardLabel}>Severity Level</div>
          <div style={{
            ...styles.cardValue,
            color: getSeverityColor(triageData.severity),
            textTransform: 'uppercase',
            fontWeight: 'bold'
          }}>
            {triageData.severity}
          </div>
        </div>

        <div style={styles.card}>
          <div style={styles.cardLabel}>Recommended Specialty</div>
          <div style={styles.cardValue}>{triageData.recommendedSpecialty}</div>
        </div>

        <div style={styles.card}>
          <div style={styles.cardLabel}>Estimated Response Time</div>
          <div style={styles.cardValue}>{triageData.estimatedResponseTime} min</div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: '#1a1a1a',
    padding: '20px',
    borderRadius: '10px',
    margin: '20px auto',
    maxWidth: '800px'
  },
  title: {
    color: '#4CAF50',
    marginTop: 0,
    marginBottom: '20px'
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
    gap: '15px'
  },
  card: {
    backgroundColor: '#2a2a2a',
    padding: '15px',
    borderRadius: '8px',
    border: '1px solid #333'
  },
  cardLabel: {
    color: '#888',
    fontSize: '12px',
    marginBottom: '8px',
    textTransform: 'uppercase'
  },
  cardValue: {
    color: 'white',
    fontSize: '18px',
    fontWeight: 'bold'
  }
};
