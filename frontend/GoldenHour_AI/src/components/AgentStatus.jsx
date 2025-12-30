import { useAgentStatus } from '../hooks';

export default function AgentStatus({ emergencyId }) {
  const { data: agentStatus } = useAgentStatus(emergencyId);

  if (!emergencyId || !agentStatus) return null;

  const getStatusIcon = (status) => {
    switch (status) {
      case 'processing': return '⏳';
      case 'completed': return '✅';
      case 'error': return '❌';
      default: return '🤖';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'processing': return '#ffaa00';
      case 'completed': return '#4CAF50';
      case 'error': return '#ff0000';
      default: return '#666';
    }
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>🤖 AI Agents Activity</h3>
      <div style={styles.timeline}>
        <div style={styles.agent}>
          <span style={{ ...styles.icon, color: getStatusColor(agentStatus.status) }}>
            {getStatusIcon(agentStatus.status)}
          </span>
          <div style={styles.info}>
            <div style={styles.agentName}>{agentStatus.agentName}</div>
            <div style={styles.message}>{agentStatus.message}</div>
            <div style={styles.timestamp}>
              {new Date(agentStatus.timestamp).toLocaleTimeString()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: '#1a1a1a',
    padding: '15px',
    borderRadius: '8px',
    maxWidth: '800px',
    margin: '20px auto'
  },
  title: {
    color: '#2196F3',
    margin: '0 0 15px 0',
    fontSize: '18px'
  },
  timeline: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px'
  },
  agent: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
    backgroundColor: '#2a2a2a',
    padding: '12px',
    borderRadius: '8px'
  },
  icon: {
    fontSize: '24px'
  },
  info: {
    flex: 1
  },
  agentName: {
    color: '#4CAF50',
    fontWeight: 'bold',
    marginBottom: '5px'
  },
  message: {
    color: 'white',
    marginBottom: '5px'
  },
  timestamp: {
    color: '#888',
    fontSize: '12px'
  }
};
