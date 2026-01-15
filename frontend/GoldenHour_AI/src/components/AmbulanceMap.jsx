import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const emergencyIcon = new L.Icon({
  iconUrl:
    'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

const hospitalIcon = new L.Icon({
  iconUrl:
    'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl:
    'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

export default function AmbulanceMap({
  emergencyLocation,
  hospitalLocation,
  needsAmbulance,
}) {
  // 🔔 Show alert after fixed time (9 minutes here)
  useEffect(() => {
    if (!needsAmbulance) return;

    const ETA_MINUTES = 9;
    const ms = ETA_MINUTES * 60 * 1000;

    const timer = setTimeout(() => {
      alert('🚑 Ambulance has reached the emergency location.');
    }, ms);

    return () => clearTimeout(timer);
  }, [needsAmbulance]);

  const normalizeCoord = (coord) => {
    if (!coord) return null;
    const latRaw = coord.lat ?? coord.latitude;
    const lngRaw = coord.lng ?? coord.longitude;
    const lat = typeof latRaw === 'string' ? parseFloat(latRaw) : latRaw;
    const lng = typeof lngRaw === 'string' ? parseFloat(lngRaw) : lngRaw;
    if (typeof lat !== 'number' || typeof lng !== 'number') return null;
    if (isNaN(lat) || isNaN(lng)) return null;
    return { lat, lng, name: coord.name };
  };

  const normalizedEmergency = normalizeCoord(emergencyLocation);
  const normalizedHospital = normalizeCoord(hospitalLocation);

  const hasCoords = (coord) =>
    coord && typeof coord.lat === 'number' && typeof coord.lng === 'number';

  if (!hasCoords(normalizedEmergency) || !hasCoords(normalizedHospital)) {
    return null;
  }

  const center = [normalizedEmergency.lat, normalizedEmergency.lng];

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🗺️ Live Route Tracking</h2>

      <div style={styles.mapWrapper}>
        <MapContainer center={center} zoom={13} style={styles.map} scrollWheelZoom>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {/* Emergency (red) */}
          <Marker position={center} icon={emergencyIcon}>
            <Popup>
              🚨 Emergency Location
              <br />
              Patient location
            </Popup>
          </Marker>

          {/* Hospital (green) */}
          <Marker
            position={[normalizedHospital.lat, normalizedHospital.lng]}
            icon={hospitalIcon}
          >
            <Popup>
              🏥 {normalizedHospital.name || hospitalLocation?.name || 'Selected Hospital'}
              <br />
              Hospital location
            </Popup>
          </Marker>
        </MapContainer>
      </div>

      {needsAmbulance && (
        <div style={styles.statusBar}>
          <div style={styles.statusLine}>🚑 Ambulance assigned — ETA: 9 min</div>
          <div style={styles.driverInfo}>
            <span style={styles.driverLabel}>Driver:</span> Rajesh Kumar •
            <span style={styles.phoneLabel}> ☎ +91 98765 43210</span>
          </div>
        </div>
      )}

      <div style={styles.legend}>
        <div style={styles.legendItem}>
          <span style={{ ...styles.legendDot, backgroundColor: '#ff4444' }}>🔴</span>
          <span>Emergency Location</span>
        </div>
        <div style={styles.legendItem}>
          <span style={{ ...styles.legendDot, backgroundColor: '#4CAF50' }}>🟢</span>
          <span>Hospital</span>
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
    marginTop: '20px',
  },
  title: {
    color: '#4CAF50',
    margin: '0 0 20px 0',
    textAlign: 'center',
  },
  mapWrapper: {
    borderRadius: '10px',
    overflow: 'hidden',
    border: '2px solid #333',
  },
  map: {
    height: '500px',
    width: '100%',
  },
  statusBar: {
    marginTop: '10px',
    padding: '12px 15px',
    backgroundColor: '#222',
    borderRadius: '8px',
    color: 'white',
    fontSize: '14px',
  },
  statusLine: {
    textAlign: 'center',
    marginBottom: '8px',
    fontWeight: '500',
  },
  driverInfo: {
    textAlign: 'center',
    fontSize: '13px',
    color: '#ddd',
  },
  driverLabel: {
    fontWeight: '600',
    color: '#4CAF50',
  },
  phoneLabel: {
    color: '#2196F3',
    fontWeight: '500',
  },
  legend: {
    display: 'flex',
    justifyContent: 'center',
    gap: '30px',
    marginTop: '15px',
    padding: '15px',
    backgroundColor: '#2a2a2a',
    borderRadius: '8px',
  },
  legendItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    color: 'white',
    fontSize: '14px',
  },
  legendDot: {
    width: '12px',
    height: '12px',
    borderRadius: '50%',
    display: 'inline-block',
  },
};
