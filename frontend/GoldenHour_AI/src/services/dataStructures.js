/**
 * EMERGENCY REQUEST - What the form sends to backend
 * 
 * Example:
 * {
 *   patientName: "Rahul Sharma",
 *   age: 45,
 *   vitals: {
 *     bloodPressure: "140/90",
 *     heartRate: 95,
 *     oxygenLevel: 92
 *   },
 *   symptoms: "Chest pain, difficulty breathing",
 *   location: { 
 *     lat: 28.7041, 
 *     lng: 77.1025 
 *   }
 * }
 */

/**
 * TRIAGE RESPONSE - What backend returns after analysis
 * 
 * Example:
 * {
 *   emergencyId: "emer_abc123",
 *   severity: "critical",
 *   recommendedSpecialty: "Cardiology",
 *   estimatedResponseTime: 15
 * }
 */

/**
 * HOSPITAL DATA - List of hospitals from routing agent
 * 
 * Example:
 * {
 *   id: "hosp_001",
 *   name: "Apollo Hospital",
 *   location: { lat: 28.7041, lng: 77.1025 },
 *   distance: 5.2,
 *   eta: 12,
 *   bedsAvailable: 8,
 *   specialties: ["Cardiology", "Emergency"],
 *   isRecommended: true
 * }
 */

/**
 * AGENT UPDATE - Real-time status from WebSocket
 * 
 * Example:
 * {
 *   agentName: "routing_agent",
 *   status: "processing",
 *   message: "Finding nearest hospitals...",
 *   timestamp: "2025-12-30T16:14:00Z"
 * }
 */
