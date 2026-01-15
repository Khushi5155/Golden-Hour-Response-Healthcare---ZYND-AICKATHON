// src/components/HospitalList.jsx

import { useEffect, useState } from "react";
import { getHospitalsForEmergency } from "../services/emergencyService";

export default function HospitalList({ emergencyId, emergencyLocation, onHospitalSelect }) {
  const [hospitalsWithDistance, setHospitalsWithDistance] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!emergencyId) return;

    const fetchHospitals = async () => {
      try {
        setLoading(true);
        setError(null);

        // Backend: { emergencyId, status, hospitals: [...] }
        const data = await getHospitalsForEmergency(emergencyId);
        const hospitals = data.hospitals || [];

        // Just to be safe, sort by distance if backend did not
        const sorted = [...hospitals].sort((a, b) => {
          if (a.distance == null) return 1;
          if (b.distance == null) return -1;
          return a.distance - b.distance;
        });

        setHospitalsWithDistance(sorted);
      } catch (err) {
        console.error("Error fetching hospitals:", err);
        setError(err.message || "Failed to load hospitals");
      } finally {
        setLoading(false);
      }
    };

    fetchHospitals();
  }, [emergencyId]);

  if (!emergencyId) return null;

  if (loading) {
    return (
      <div style={styles.container}>
        <p style={{ color: "#fff" }}>Loading hospitals...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.container}>
        <p style={{ color: "#ff4444" }}>Error: {error}</p>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h3 style={styles.title}>🏥 Available Hospitals</h3>
        <p style={styles.subtitle}>
          Showing nearby hospitals for this emergency
        </p>
      </div>

      <div style={styles.grid}>
        {hospitalsWithDistance.map((h) => (
          <button
            key={h.id}
            style={styles.card}
            onClick={() => onHospitalSelect && onHospitalSelect(h)}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "translateY(-4px)";
              e.currentTarget.style.boxShadow =
                "0 8px 20px rgba(76, 175, 80, 0.3)";
              e.currentTarget.style.borderColor = "#4CAF50";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "translateY(0)";
              e.currentTarget.style.boxShadow =
                "0 4px 12px rgba(0, 0, 0, 0.3)";
              e.currentTarget.style.borderColor = "#333";
            }}
          >
            <div style={styles.cardHeader}>
              <div style={styles.hospitalIcon}>🏥</div>
              <div style={styles.distance}>
                {h.distance != null ? `${h.distance} km` : "—"}
              </div>
            </div>

            <div style={styles.name}>{h.name}</div>

            <div style={styles.location}>
              <span style={styles.locationIcon}>📍</span>
              {h.address}
            </div>

            <div style={{ marginTop: 8, fontSize: 12, color: "#ccc" }}>
              ETA: {h.eta != null ? `${h.eta} min` : "—"}
            </div>

            {h.isRecommended && (
              <div
                style={{
                  marginTop: 6,
                  fontSize: 11,
                  color: "#4CAF50",
                  fontWeight: "bold",
                }}
              >
                ⭐ Recommended
              </div>
            )}
          </button>
        ))}
      </div>
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: "#1a1a1a",
    padding: "30px 20px",
    borderRadius: "12px",
    marginTop: "20px",
    border: "2px solid #2a2a2a",
  },
  header: {
    textAlign: "center",
    marginBottom: "25px",
  },
  title: {
    margin: 0,
    marginBottom: "8px",
    fontSize: "24px",
    color: "#4CAF50",
    fontWeight: "bold",
  },
  subtitle: {
    margin: 0,
    fontSize: "14px",
    color: "#aaa",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
    gap: "15px",
  },
  card: {
    display: "flex",
    flexDirection: "column",
    padding: "18px",
    borderRadius: "10px",
    border: "2px solid #333",
    backgroundColor: "#2a2a2a",
    cursor: "pointer",
    transition: "all 0.3s ease",
    textAlign: "left",
    boxShadow: "0 4px 12px rgba(0, 0, 0, 0.3)",
    outline: "none",
  },
  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "12px",
  },
  hospitalIcon: {
    fontSize: "28px",
  },
  distance: {
    fontSize: "12px",
    fontWeight: "bold",
    color: "#4CAF50",
    backgroundColor: "rgba(76, 175, 80, 0.15)",
    padding: "4px 10px",
    borderRadius: "12px",
  },
  name: {
    fontSize: "17px",
    fontWeight: "bold",
    color: "#fff",
    marginBottom: "8px",
  },
  location: {
    fontSize: "13px",
    color: "#bbb",
    display: "flex",
    alignItems: "center",
    gap: "6px",
  },
  locationIcon: {
    fontSize: "14px",
  },
};
