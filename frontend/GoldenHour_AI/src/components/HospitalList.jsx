// src/components/HospitalList.jsx

import { useEffect, useState } from 'react';

// Haversine formula to calculate distance between two lat/lng points in km
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // Earth's radius in km
  const dLat = ((lat2 - lat1) * Math.PI) / 180;
  const dLon = ((lon2 - lon1) * Math.PI) / 180;
  
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((lat1 * Math.PI) / 180) *
      Math.cos((lat2 * Math.PI) / 180) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c;
  
  return distance.toFixed(1); // Return distance in km with 1 decimal
}

export default function HospitalList({ emergencyId, emergencyLocation, onHospitalSelect }) {
  const [hospitalsWithDistance, setHospitalsWithDistance] = useState([]);

  const hospitals = [
    {
      id: 1,
      name: 'Apollo Hospital',
      location: 'Sarita Vihar, New Delhi',
      latitude: 28.5355,
      longitude: 77.2670,
    },
    {
      id: 2,
      name: 'AIIMS Delhi',
      location: 'Ansari Nagar, New Delhi',
      latitude: 28.5672,
      longitude: 77.2100,
    },
    {
      id: 3,
      name: 'Fortis Hospital',
      location: 'Sector 62, Noida',
      latitude: 28.6280,
      longitude: 77.3700,
    },
    {
      id: 4,
      name: 'Max Super Specialty Hospital',
      location: 'Patparganj, East Delhi',
      latitude: 28.6290,
      longitude: 77.2973,
    },
    {
      id: 5,
      name: 'Yatharth Hospital',
      location: 'Sector 110, Noida',
      latitude: 28.5250,
      longitude: 77.3890,
    },
    {
      id: 6,
      name: 'Kailash Hospital',
      location: 'Sector 71, Noida',
      latitude: 28.5763,
      longitude: 77.3803,
    },
    {
      id: 7,
      name: 'Metro Hospital',
      location: 'Sector 11, Noida',
      latitude: 28.5813,
      longitude: 77.3240,
    },
    {
      id: 8,
      name: 'Sharda Hospital',
      location: 'Greater Noida',
      latitude: 28.4647,
      longitude: 77.4938,
    },
    {
      id: 9,
      name: 'Max Hospital',
      location: 'Vaishali, Ghaziabad',
      latitude: 28.6490,
      longitude: 77.3410,
    },
  ];

  useEffect(() => {
    console.log('HospitalList mounted. emergencyId =', emergencyId);
    console.log('Emergency location:', emergencyLocation);

    // Calculate distances if emergency location is available
    if (emergencyLocation && emergencyLocation.lat && emergencyLocation.lng) {
      const hospitalsWithDist = hospitals.map((h) => ({
        ...h,
        distance: calculateDistance(
          emergencyLocation.lat,
          emergencyLocation.lng,
          h.latitude,
          h.longitude
        ),
      }));

      // Sort by distance (nearest first)
      hospitalsWithDist.sort((a, b) => parseFloat(a.distance) - parseFloat(b.distance));

      setHospitalsWithDistance(hospitalsWithDist);
    } else {
      // If no emergency location, show hospitals without distance
      setHospitalsWithDistance(hospitals.map((h) => ({ ...h, distance: '—' })));
    }
  }, [emergencyId, emergencyLocation]);

  if (!emergencyId) {
    return null;
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h3 style={styles.title}>🏥 Available Hospitals</h3>
        <p style={styles.subtitle}>
          {emergencyLocation?.lat && emergencyLocation?.lng
            ? 'Sorted by distance from emergency location'
            : 'Select the nearest hospital to dispatch ambulance'}
        </p>
      </div>

      <div style={styles.grid}>
        {hospitalsWithDistance.map((h) => (
          <button
            key={h.id}
            style={styles.card}
            onClick={() => onHospitalSelect(h)}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 8px 20px rgba(76, 175, 80, 0.3)';
              e.currentTarget.style.borderColor = '#4CAF50';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.3)';
              e.currentTarget.style.borderColor = '#333';
            }}
          >
            <div style={styles.cardHeader}>
              <div style={styles.hospitalIcon}>🏥</div>
              <div style={styles.distance}>
                {h.distance === '—' ? h.distance : `${h.distance} km`}
              </div>
            </div>
            <div style={styles.name}>{h.name}</div>
            <div style={styles.location}>
              <span style={styles.locationIcon}>📍</span>
              {h.location}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: '#1a1a1a',
    padding: '30px 20px',
    borderRadius: '12px',
    marginTop: '20px',
    border: '2px solid #2a2a2a',
  },
  header: {
    textAlign: 'center',
    marginBottom: '25px',
  },
  title: {
    margin: 0,
    marginBottom: '8px',
    fontSize: '24px',
    color: '#4CAF50',
    fontWeight: 'bold',
  },
  subtitle: {
    margin: 0,
    fontSize: '14px',
    color: '#aaa',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '15px',
  },
  card: {
    display: 'flex',
    flexDirection: 'column',
    padding: '18px',
    borderRadius: '10px',
    border: '2px solid #333',
    backgroundColor: '#2a2a2a',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    textAlign: 'left',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
    outline: 'none',
  },
  cardHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px',
  },
  hospitalIcon: {
    fontSize: '28px',
  },
  distance: {
    fontSize: '12px',
    fontWeight: 'bold',
    color: '#4CAF50',
    backgroundColor: 'rgba(76, 175, 80, 0.15)',
    padding: '4px 10px',
    borderRadius: '12px',
  },
  name: {
    fontSize: '17px',
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: '8px',
  },
  location: {
    fontSize: '13px',
    color: '#bbb',
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
  },
  locationIcon: {
    fontSize: '14px',
  },
};
