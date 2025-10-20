// Simple test script to verify frontend can connect to backend
const testFrontendBackendConnection = async () => {
  try {
    console.log('Testing frontend-backend connection...');
    
    // Simulate the API URL that the frontend would use
    const API_URL = 'http://localhost:8000/api';
    console.log('Using API URL:', API_URL);
    
    // Test the posts endpoint
    const response = await fetch(`${API_URL}/posts/`);
    console.log('Response status:', response.status);
    
    if (response.ok) {
      console.log('✅ SUCCESS: Frontend can connect to backend!');
      const data = await response.json();
      console.log('Received data:', Array.isArray(data) ? `${data.length} posts` : typeof data);
    } else {
      console.log('❌ ERROR: Received HTTP status', response.status);
      console.log('Status text:', response.statusText);
    }
  } catch (error) {
    console.log('❌ ERROR: Failed to connect to backend');
    console.log('Error message:', error.message);
    console.log('This might be due to:');
    console.log('1. Backend server not running');
    console.log('2. Incorrect API URL');
    console.log('3. Network/firewall issues');
    console.log('4. CORS configuration problems');
  }
};

// Run the test
testFrontendBackendConnection();