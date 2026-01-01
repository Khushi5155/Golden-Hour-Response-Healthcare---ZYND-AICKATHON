import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { useEffect, useState } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix default marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom icons
const emergencyIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const hospitalIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const ambulanceIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

function AmbulanceTracker({ 
  emergencyLocation, 
  hospitalLocation, 
  ambulanceStartLocation, 
  needsAmbulance,
  onAmbulanceArrival 
}) {
  const map = useMap();
  const [currentPosition, setCurrentPosition] = useState(ambulanceStartLocation);
  const [arrived, setArrived] = useState(false);

  useEffect(() => {
    if (!needsAmbulance) return;

    const startLat = ambulanceStartLocation.lat;
    const startLng = ambulanceStartLocation.lng;
    const endLat = emergencyLocation.lat;
    const endLng = emergencyLocation.lng;

    const steps = 100;
    let currentStep = 0;

    const interval = setInterval(() => {
      currentStep++;
      const progress = currentStep / steps;

      const newLat = startLat + (endLat - startLat) * progress;
      const newLng = startLng + (endLng - startLng) * progress;

      setCurrentPosition({ lat: newLat, lng: newLng });
      map.setView([newLat, newLng], 13);

      if (currentStep >= steps) {
        clearInterval(interval);
        setArrived(true);
        if (onAmbulanceArrival) {
          onAmbulanceArrival();
        }
      }
    }, 100);

    return () => clearInterval(interval);
  }, [ambulanceStartLocation, emergencyLocation, needsAmbulance, map, onAmbulanceArrival]);

  return (
    <>
      {needsAmbulance && currentPosition && (
        <Marker position={[currentPosition.lat, currentPosition.lng]} icon={ambulanceIcon}>
          <Popup>
            🚑 Ambulance {arrived ? '(Arrived!)' : '(En Route)'}
          </Popup>
        </Marker>
      )}
    </>
  );
}

export default function AmbulanceMap({ 
  emergencyLocation, 
  hospitalLocation, 
  ambulanceStartLocation, 
  needsAmbulance,
  onAmbulanceArrival 
}) {
  // Validate coordinates
  const isValidCoord = (coord) => {
    return coord && 
           typeof coord.lat === 'number' && 
           typeof coord.lng === 'number' &&
           !isNaN(coord.lat) && 
           !isNaN(coord.lng) &&
           coord.lat !== 0 &&
           coord.lng !== 0;
  };

  // Debug logs
  console.log('=== AmbulanceMap Props ===');
  console.log('emergencyLocation:', emergencyLocation);
  console.log('hospitalLocation:', hospitalLocation);
  console.log('ambulanceStartLocation:', ambulanceStartLocation);
  console.log('needsAmbulance:', needsAmbulance);

  // Validate all required coordinates
  if (!isValidCoord(emergencyLocation)) {
    return (
      <div style={styles.error}>
        ❌ Error: Invalid emergency location coordinates
        <pre>{JSON.stringify(emergencyLocation, null, 2)}</pre>
      </div>
    );
  }

  if (!isValidCoord(hospitalLocation)) {
    return (
      <div style={styles.error}>
        ❌ Error: Invalid hospital location coordinates
        <pre>{JSON.stringify(hospitalLocation, null, 2)}</pre>
      </div>
    );
  }

  if (needsAmbulance && !isValidCoord(ambulanceStartLocation)) {
    return (
      <div style={styles.error}>
        ❌ Error: Invalid ambulance location coordinates
        <pre>{JSON.stringify(ambulanceStartLocation, null, 2)}</pre>
      </div>
    );
  }

  const center = [emergencyLocation.lat, emergencyLocation.lng];

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🗺️ Live Route Tracking</h2>
      
      <div style={styles.mapWrapper}>
        <MapContainer
          center={center}
          zoom={13}
          style={styles.map}
          scrollWheelZoom={true}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          <Marker position={center} icon={emergencyIcon}>
            <Popup>
              🚨 Emergency Location<br />
              Patient location
            </Popup>
          </Marker>
          
          <Marker 
            position={[hospitalLocation.lat, hospitalLocation.lng]} 
            icon={hospitalIcon}
          >
            <Popup>
              🏥 {hospitalLocation.name || 'Selected Hospital'}<br />
              Destination
            </Popup>
          </Marker>

          {needsAmbulance && ambulanceStartLocation && (
            <AmbulanceTracker
              emergencyLocation={emergencyLocation}
              hospitalLocation={hospitalLocation}
              ambulanceStartLocation={ambulanceStartLocation}
              needsAmbulance={needsAmbulance}
              onAmbulanceArrival={onAmbulanceArrival}
            />
          )}
        </MapContainer>
      </div>

      <div style={styles.legend}>
        <div style={styles.legendItem}>
          <span style={{...styles.legendDot, backgroundColor: '#ff4444'}}>🔴</span>
          <span>Emergency Location</span>
        </div>
        <div style={styles.legendItem}>
          <span style={{...styles.legendDot, backgroundColor: '#4CAF50'}}>🟢</span>
          <span>Hospital</span>
        </div>
        {needsAmbulance && (
          <div style={styles.legendItem}>
            <span style={{...styles.legendDot, backgroundColor: '#2196F3'}}>🔵</span>
            <span>Ambulance (Moving)</span>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: '#1a1a1a',
    padding: '20px',
    borderRadius: '10px',
    marginTop: '20px'
  },
  title: {
    color: '#4CAF50',
    margin: '0 0 20px 0',
    textAlign: 'center'
  },
  mapWrapper: {
    borderRadius: '10px',
    overflow: 'hidden',
    border: '2px solid #333'
  },
  map: {
    height: '500px',
    width: '100%'
  },
  legend: {
    display: 'flex',
    justifyContent: 'center',
    gap: '30px',
    marginTop: '15px',
    padding: '15px',
    backgroundColor: '#2a2a2a',
    borderRadius: '8px'
  },
  legendItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    color: 'white',
    fontSize: '14px'
  },
  legendDot: {
    width: '12px',
    height: '12px',
    borderRadius: '50%',
    display: 'inline-block'
  },
  error: {
    backgroundColor: '#ff4444',
    color: 'white',
    padding: '20px',
    borderRadius: '10px',
    marginTop: '20px',
    fontFamily: 'monospace'
  }
};
